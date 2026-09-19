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
        lowered = title.lower()
        brand = next((name for name in ("dyson", "kitchenaid", "apple", "sony", "dewalt") if name in lowered), None)
        condition = "for_parts" if any(word in lowered for word in ("parts", "broken", "not working")) else "used"
        damage = [hint for hint in DAMAGE_HINTS if hint in lowered]
        cleaned = re.sub(r"\s+", " ", title).strip()
        return NormalizedProduct(
            listing_id=listing.id,
            brand=brand.title() if brand else None,
            model=None,
            category=self._guess_category(lowered),
            condition=condition,
            normalized_title=cleaned,
            attributes={"damage_hints": damage, "source": listing.source},
        )

    def _guess_category(self, text: str) -> str:
        if any(word in text for word in ("iphone", "macbook", "ipad")):
            return "electronics"
        if any(word in text for word in ("mixer", "vacuum", "blender", "dyson", "kitchenaid")):
            return "home"
        if any(word in text for word in ("dewalt", "milwaukee", "tool")):
            return "tools"
        return "general"


analyzer = Analyzer()
