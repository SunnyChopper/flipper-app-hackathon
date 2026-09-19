from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.data.ids import (
    BOM_IPHONE_BATTERY,
    BOM_IPHONE_SCREEN,
    BOM_MBA_DISPLAY,
    BOM_PS5_HDMI,
    BOM_PS5_PSU,
    COMP_HDMI_BOARD,
    COMP_IPHONE_1,
    COMP_IPHONE_2,
    COMP_IPHONE_3,
    COMP_IPHONE_BATTERY,
    COMP_MBA_1,
    COMP_MBA_2,
    COMP_MBA_3,
    COMP_MBA_DISPLAY,
    COMP_OLED_SCREEN,
    COMP_PS5_1,
    COMP_PS5_2,
    COMP_PS5_3,
    COMP_PS5_PSU,
    DEMO_USER_ID,
    LISTING_IPHONE_BATTERY,
    LISTING_IPHONE_CRACKED,
    LISTING_MBA_PARTS,
    LISTING_MBA_SCREEN,
    LISTING_PS5_HDMI,
    LISTING_PS5_NOPOWER,
    PROD_IPHONE,
    PROD_MBA,
    PROD_PS5,
)
from app.domain.entities import (
    CatalogProduct,
    Component,
    Listing,
    ProductBOMItem,
    ProductMarketComp,
    Profile,
    RepairSkill,
    UserSkill,
)
from app.services.valuation_service import listing_economics


def _ts(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp).replace(tzinfo=UTC)


REPAIR_SKILLS = [
    RepairSkill("screen_swap", "Screen / Display Replacement", "electronics"),
    RepairSkill("battery_replacement", "Battery Replacement", "electronics"),
    RepairSkill("board_level_repair", "Board-Level Repair", "electronics"),
]

CATALOG_PRODUCTS = [
    CatalogProduct(
        id=PROD_IPHONE,
        brand="Apple",
        model="iPhone 13",
        variant="128GB Unlocked",
        category="smartphones",
        estimated_working_market_value=425,
        valuation_confidence_score=0.92,
        last_valuation_at=_ts("2026-09-19T10:00:00"),
    ),
    CatalogProduct(
        id=PROD_PS5,
        brand="Sony",
        model="PlayStation 5",
        variant="Disc Edition",
        category="gaming_consoles",
        estimated_working_market_value=370,
        valuation_confidence_score=0.88,
        last_valuation_at=_ts("2026-09-19T10:00:00"),
    ),
    CatalogProduct(
        id=PROD_MBA,
        brand="Apple",
        model="MacBook Air M1",
        variant="256GB",
        category="laptops",
        estimated_working_market_value=680,
        valuation_confidence_score=0.85,
        last_valuation_at=_ts("2026-09-19T10:00:00"),
    ),
]

COMPONENTS = [
    Component(COMP_OLED_SCREEN, "OLED Screen Assembly"),
    Component(COMP_IPHONE_BATTERY, "iPhone Battery"),
    Component(COMP_HDMI_BOARD, "HDMI Board"),
    Component(COMP_PS5_PSU, "Power Supply Unit"),
    Component(COMP_MBA_DISPLAY, "MacBook Display Assembly"),
]

BOM_ITEMS = [
    ProductBOMItem(BOM_IPHONE_SCREEN, PROD_IPHONE, COMP_OLED_SCREEN, "screen_swap", 90, 35, 5),
    ProductBOMItem(BOM_IPHONE_BATTERY, PROD_IPHONE, COMP_IPHONE_BATTERY, "battery_replacement", 45, 28, 4),
    ProductBOMItem(BOM_PS5_HDMI, PROD_PS5, COMP_HDMI_BOARD, "board_level_repair", 70, 32, 3),
    ProductBOMItem(BOM_PS5_PSU, PROD_PS5, COMP_PS5_PSU, "board_level_repair", 55, 30, 4),
    ProductBOMItem(BOM_MBA_DISPLAY, PROD_MBA, COMP_MBA_DISPLAY, "screen_swap", 180, 90, 5),
]

MARKET_COMPS = [
    ProductMarketComp(COMP_IPHONE_1, PROD_IPHONE, "ebay_sold", 410, 15, "used_working", "2026-09-17", "https://www.ebay.com/itm/mock-iphone-comp-1"),
    ProductMarketComp(COMP_IPHONE_2, PROD_IPHONE, "ebay_sold", 399, 12, "used_working", "2026-09-14", "https://www.ebay.com/itm/mock-iphone-comp-2"),
    ProductMarketComp(COMP_IPHONE_3, PROD_IPHONE, "ebay_sold", 430, 0, "used_working", "2026-09-10", "https://www.ebay.com/itm/mock-iphone-comp-3"),
    ProductMarketComp(COMP_PS5_1, PROD_PS5, "ebay_sold", 355, 15, "used_working", "2026-09-16", "https://www.ebay.com/itm/mock-ps5-comp-1"),
    ProductMarketComp(COMP_PS5_2, PROD_PS5, "ebay_sold", 349, 20, "used_working", "2026-09-12", "https://www.ebay.com/itm/mock-ps5-comp-2"),
    ProductMarketComp(COMP_PS5_3, PROD_PS5, "ebay_sold", 380, 0, "used_working", "2026-09-08", "https://www.ebay.com/itm/mock-ps5-comp-3"),
    ProductMarketComp(COMP_MBA_1, PROD_MBA, "ebay_sold", 650, 20, "used_working", "2026-09-15", "https://www.ebay.com/itm/mock-mba-comp-1"),
    ProductMarketComp(COMP_MBA_2, PROD_MBA, "ebay_sold", 680, 15, "used_working", "2026-09-11", "https://www.ebay.com/itm/mock-mba-comp-2"),
    ProductMarketComp(COMP_MBA_3, PROD_MBA, "ebay_sold", 640, 25, "used_working", "2026-09-07", "https://www.ebay.com/itm/mock-mba-comp-3"),
]


def _listing(
    *,
    listing_id: str,
    source: str,
    external_id: str,
    url: str,
    title: str,
    description: str,
    price: float,
    shipping_cost: float,
    condition: str,
    image_urls: list[str],
    listed_at: datetime,
    created_at: datetime,
    product: CatalogProduct,
    defective_bom_ids: list[str],
    required_skills: list[str],
) -> Listing:
    product_bom = [item for item in BOM_ITEMS if item.product_id == product.id]
    _replacement, restorer, harvest = listing_economics(
        working_market_value=product.estimated_working_market_value,
        price=price,
        shipping_cost=shipping_cost,
        bom_items=product_bom,
        defective_bom_ids=defective_bom_ids,
    )
    return Listing(
        id=listing_id,
        source=source,
        external_id=external_id,
        url=url,
        title=title,
        description=description,
        price=price,
        shipping_cost=shipping_cost,
        condition=condition,
        image_urls=image_urls,
        listed_at=listed_at,
        created_at=created_at,
        matched_product_id=product.id,
        detected_defective_bom_ids=defective_bom_ids,
        required_repair_skills=required_skills,
        projected_restorer_net=restorer,
        projected_harvest_yield=harvest,
    )


def build_listings() -> list[Listing]:
    iphone, ps5, mba = CATALOG_PRODUCTS
    iphone_img = "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80"
    ps5_img = "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=900&q=80"
    mba_img = "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80"
    return [
        _listing(
            listing_id=LISTING_IPHONE_CRACKED,
            source="facebook_marketplace",
            external_id="fb-iphone-13-cracked",
            url="https://www.facebook.com/marketplace/item/mock-iphone-cracked",
            title="iPhone 13 128GB cracked screen works fine",
            description="Screen damaged but everything else works.",
            price=220,
            shipping_cost=0,
            condition="damaged",
            image_urls=[
                iphone_img,
                "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=900&q=80",
            ],
            listed_at=_ts("2026-09-19T12:00:00"),
            created_at=_ts("2026-09-19T12:03:00"),
            product=iphone,
            defective_bom_ids=[BOM_IPHONE_SCREEN],
            required_skills=["screen_swap"],
        ),
        _listing(
            listing_id=LISTING_IPHONE_BATTERY,
            source="ebay",
            external_id="ebay-iphone-13-battery",
            url="https://www.ebay.com/itm/mock-iphone-battery",
            title="iPhone 13 128GB swollen battery Face ID works",
            description="Unlocked. Screen is fine. Battery is swollen and needs replacement.",
            price=155,
            shipping_cost=10,
            condition="used_fair",
            image_urls=[iphone_img],
            listed_at=_ts("2026-09-19T08:30:00"),
            created_at=_ts("2026-09-19T08:32:00"),
            product=iphone,
            defective_bom_ids=[BOM_IPHONE_BATTERY],
            required_skills=["battery_replacement"],
        ),
        _listing(
            listing_id=LISTING_PS5_NOPOWER,
            source="ebay",
            external_id="ebay-ps5-nopower",
            url="https://www.ebay.com/itm/mock-ps5-nopower",
            title="PS5 Disc Edition won't power on",
            description="No lights. HDMI port looks intact. Sold as-is for parts or repair.",
            price=120,
            shipping_cost=18,
            condition="for_parts",
            image_urls=[
                ps5_img,
                "https://images.unsplash.com/photo-1607853202273-797f1c22a38e?auto=format&fit=crop&w=900&q=80",
            ],
            listed_at=_ts("2026-09-19T07:00:00"),
            created_at=_ts("2026-09-19T07:05:00"),
            product=ps5,
            defective_bom_ids=[BOM_PS5_PSU],
            required_skills=["board_level_repair"],
        ),
        _listing(
            listing_id=LISTING_PS5_HDMI,
            source="facebook_marketplace",
            external_id="fb-ps5-hdmi",
            url="https://www.facebook.com/marketplace/item/mock-ps5-hdmi",
            title="PS5 Disc Edition no picture HDMI issue",
            description="Console powers on. Fans spin. No video output.",
            price=145,
            shipping_cost=0,
            condition="damaged",
            image_urls=[ps5_img],
            listed_at=_ts("2026-09-18T21:00:00"),
            created_at=_ts("2026-09-18T21:04:00"),
            product=ps5,
            defective_bom_ids=[BOM_PS5_HDMI],
            required_skills=["board_level_repair"],
        ),
        _listing(
            listing_id=LISTING_MBA_SCREEN,
            source="facebook_marketplace",
            external_id="fb-mba-screen",
            url="https://www.facebook.com/marketplace/item/mock-mba-screen",
            title="MacBook Air M1 screen damage cosmetic wear",
            description="Screen damage, cosmetic wear on lid. Keyboard appears complete.",
            price=300,
            shipping_cost=0,
            condition="damaged",
            image_urls=[
                mba_img,
                "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
            ],
            listed_at=_ts("2026-09-19T03:00:00"),
            created_at=_ts("2026-09-19T03:06:00"),
            product=mba,
            defective_bom_ids=[BOM_MBA_DISPLAY],
            required_skills=["screen_swap"],
        ),
        _listing(
            listing_id=LISTING_MBA_PARTS,
            source="ebay",
            external_id="ebay-mba-parts",
            url="https://www.ebay.com/itm/mock-mba-parts",
            title="MacBook Air M1 256GB for parts cracked display",
            description="Activation lock off. Display is cracked. Logic board not tested.",
            price=190,
            shipping_cost=25,
            condition="for_parts",
            image_urls=[mba_img],
            listed_at=_ts("2026-09-18T16:00:00"),
            created_at=_ts("2026-09-18T16:10:00"),
            product=mba,
            defective_bom_ids=[BOM_MBA_DISPLAY],
            required_skills=["screen_swap"],
        ),
    ]


DEMO_PROFILE = Profile(
    id=DEMO_USER_ID,
    persona="restorer",
    min_profit_margin_usd=100,
    min_roi_percent=20,
)

DEMO_USER_SKILLS = [
    UserSkill(DEMO_USER_ID, "screen_swap"),
    UserSkill(DEMO_USER_ID, "battery_replacement"),
]


@dataclass
class SeedData:
    repair_skills: list[RepairSkill] = field(default_factory=list)
    catalog_products: list[CatalogProduct] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)
    bom_items: list[ProductBOMItem] = field(default_factory=list)
    market_comps: list[ProductMarketComp] = field(default_factory=list)
    listings: list[Listing] = field(default_factory=list)
    profile: Profile = field(default_factory=lambda: DEMO_PROFILE)
    user_skills: list[UserSkill] = field(default_factory=list)


def build_seed() -> SeedData:
    return SeedData(
        repair_skills=list(REPAIR_SKILLS),
        catalog_products=list(CATALOG_PRODUCTS),
        components=list(COMPONENTS),
        bom_items=list(BOM_ITEMS),
        market_comps=list(MARKET_COMPS),
        listings=build_listings(),
        profile=DEMO_PROFILE,
        user_skills=list(DEMO_USER_SKILLS),
    )
