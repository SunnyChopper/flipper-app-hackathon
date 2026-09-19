from __future__ import annotations

from datetime import UTC, datetime
from uuid import NAMESPACE_URL, uuid5

from app.data.ids import PROD_IPHONE, PROD_MBA, PROD_PS5
from app.domain.entities import CatalogProduct, Listing, ProductBOMItem
from app.models.listing import Listing as ScrapedListing
from app.repositories.product_repository import ProductRepository
from app.services.valuation_service import listing_economics

PRODUCT_HINTS: list[tuple[str, tuple[str, ...]]] = [
    (PROD_IPHONE, ("iphone 13", "iphone13")),
    (PROD_PS5, ("playstation 5", "play station 5", "ps5")),
    (PROD_MBA, ("macbook air", "mba m1")),
]

SKILL_HINTS: dict[str, tuple[str, ...]] = {
    "screen_swap": ("screen", "display", "crack", "cracked", "glass"),
    "battery_replacement": ("battery", "swollen"),
    "board_level_repair": (
        "hdmi",
        "no power",
        "won't power",
        "wont power",
        "no picture",
        "no video",
        "board",
        "not turning",
        "for parts",
    ),
}


def to_domain_listing(scraped: ScrapedListing, products: ProductRepository) -> Listing:
    source = "facebook_marketplace" if scraped.source == "facebook" else "ebay"
    blob = f"{scraped.title} {scraped.description} {scraped.condition_label or ''}".lower()
    product = _match_product(blob, products)
    bom = products.bom_for_product(product.id) if product else []
    defective_ids = _defective_bom_ids(blob, bom)
    skills = sorted({item.required_skill_slug for item in bom if item.id in defective_ids})
    shipping = scraped.shipping_cost or 0.0
    working_value = product.estimated_working_market_value if product else round(scraped.price * 1.35, 2)
    _replacement, restorer, harvest = listing_economics(
        working_market_value=working_value,
        price=scraped.price,
        shipping_cost=shipping,
        bom_items=bom,
        defective_bom_ids=defective_ids,
    )
    image_urls = [scraped.image_url] if scraped.image_url else []
    now = datetime.now(UTC)
    return Listing(
        id=str(uuid5(NAMESPACE_URL, f"{source}:{scraped.external_id}")),
        source=source,
        external_id=scraped.external_id,
        url=scraped.url,
        title=scraped.title,
        price=scraped.price,
        shipping_cost=shipping,
        condition=_condition(blob, scraped.condition_label),
        image_urls=image_urls,
        created_at=now,
        listed_at=now,
        description=scraped.description or None,
        matched_product_id=product.id if product else None,
        detected_defective_bom_ids=defective_ids,
        required_repair_skills=skills,
        projected_restorer_net=restorer,
        projected_harvest_yield=harvest,
    )


def _match_product(blob: str, products: ProductRepository) -> CatalogProduct | None:
    for product_id, hints in PRODUCT_HINTS:
        if any(hint in blob for hint in hints):
            return products.get(product_id)
    return None


def _defective_bom_ids(blob: str, bom: list[ProductBOMItem]) -> list[str]:
    matched: list[str] = []
    for item in bom:
        hints = SKILL_HINTS.get(item.required_skill_slug, ())
        if any(hint in blob for hint in hints):
            matched.append(item.id)
    return matched


def _condition(blob: str, condition_label: str | None) -> str:
    label = (condition_label or "").lower()
    if ("activation lock" in blob or "icloud lock" in blob) and "unlock" not in blob:
        return "locked"
    if "part" in label or "not working" in label or "for_parts" in blob or "for parts" in blob:
        return "for_parts"
    if any(word in blob for word in ("crack", "dent", "damage", "swollen", "broken", "no power", "no picture")):
        return "damaged"
    return "used_fair"
