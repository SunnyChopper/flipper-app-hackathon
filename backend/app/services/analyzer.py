import re

from app.config import settings
from app.models.listing import Listing, NormalizedProduct

DAMAGE_HINTS = ("dent", "scratch", "crack", "broken", "battery", "stain", "missing")


class Analyzer:
    """Turn messy marketplace titles into structured product records.

    When OPENAI_API_KEY is present, swap `_heuristic_normalize` for an LLM/vision call.
    Keep the return type as NormalizedProduct either way.
    """

    async def normalize(self, listing: Listing) -> NormalizedProduct:
        if settings.openai_api_key:
            # Call the LLM / vision API, then map JSON into NormalizedProduct.
            return self._heuristic_normalize(listing)
        return self._heuristic_normalize(listing)

    def _heuristic_normalize(self, listing: Listing) -> NormalizedProduct:
        title = listing.title
        blob = f"{listing.title} {listing.description} {listing.condition_label or ''}".lower()
        brand = next((name for name in ("dyson", "kitchenaid", "apple", "sony", "dewalt") if name in blob), None)
        condition = self._guess_condition(blob, listing.condition_label)
        damage = [hint for hint in DAMAGE_HINTS if hint in blob]
        cleaned = re.sub(r"\s+", " ", title).strip()
        return NormalizedProduct(
            listing_id=listing.id,
            brand=brand.title() if brand else None,
            model=None,
            category=self._guess_category(blob),
            condition=condition,
            normalized_title=cleaned,
            attributes={
                "damage_hints": damage,
                "source": listing.source,
                "condition_label": listing.condition_label,
                "seller_name": listing.seller_name,
            },
        )

    def _guess_condition(self, text: str, condition_label: str | None) -> str:
        label = (condition_label or "").lower()
        if "part" in label or "not working" in label:
            return "for_parts"
        if any(word in text for word in ("parts", "broken", "not working")):
            return "for_parts"
        if "new" in label:
            return "new"
        return "used"

    def _guess_category(self, text: str) -> str:
        if any(word in text for word in ("iphone", "macbook", "ipad")):
            return "electronics"
        if any(word in text for word in ("mixer", "vacuum", "blender", "dyson", "kitchenaid")):
            return "home"
        if any(word in text for word in ("dewalt", "milwaukee", "tool")):
            return "tools"
        return "general"


analyzer = Analyzer()
