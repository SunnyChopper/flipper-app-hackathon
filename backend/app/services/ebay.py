from __future__ import annotations

import logging
import re

from app.config import settings
from app.models.listing import Listing
from app.models.sources import EbayApifyItem
from app.services.apify import apify_client
from app.services.listing_mapper import listing_from_ebay

logger = logging.getLogger(__name__)


class EbayClient:
    """Collect eBay listings via Apify. Mocks until APIFY_TOKEN is set."""

    def __init__(self) -> None:
        self.client = apify_client

    async def search(self, query: str, limit: int = 20) -> list[Listing]:
        if not self.client.enabled:
            return self._mock_listings(query)

        run_input = {
            "searchQueries": [query or "vacuum"],
            "marketplace": settings.ebay_marketplace_id,
            "maxItems": limit,
            "includeProductDetails": False,
            "soldListings": False,
            "proxyConfiguration": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"],
            },
        }
        try:
            rows = await self.client.run_and_get_items(settings.apify_ebay_actor, run_input)
        except Exception:
            logger.exception("Apify eBay run failed")
            raise

        listings: list[Listing] = []
        for row in rows:
            try:
                item = EbayApifyItem.model_validate(row)
            except Exception:
                logger.debug("Skipping unreadable eBay row", extra={"row_keys": list(row)})
                continue
            listing = listing_from_ebay(item)
            if listing:
                listings.append(listing)
        return listings[:limit]

    def _mock_listings(self, query: str) -> list[Listing]:
        slug = _query_slug(query)
        label = query or "Dyson V11 for parts"
        return [
            Listing(
                id=f"ebay-mock-{slug}-1",
                source="ebay",
                external_id=f"ebay-mock-{slug}-1",
                title=f"{label} — cracked housing, needs repair",
                description="Does not work. Housing is cracked. Sold as-is for parts or repair.",
                price=89,
                url=f"https://www.ebay.com/itm/mock-{slug}-1",
                image_url="https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800",
                location="Austin, TX",
                condition_label="For parts or not working",
                seller_name="mock-seller",
                shipping_cost=12.0,
                raw={"mock": True, "actor": settings.apify_ebay_actor, "query": query},
            ),
            Listing(
                id=f"ebay-mock-{slug}-2",
                source="ebay",
                external_id=f"ebay-mock-{slug}-2",
                title=f"{query or 'iPhone 13'} cracked back glass, Face ID works",
                description="Unlocked. Screen is fine. Back glass spidered. Battery 87%.",
                price=140,
                url=f"https://www.ebay.com/itm/mock-{slug}-2",
                image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
                location="Dallas, TX",
                condition_label="For parts or not working",
                seller_name="mock-phones",
                shipping_cost=0.0,
                raw={"mock": True, "actor": settings.apify_ebay_actor, "query": query},
            ),
        ]


def _query_slug(query: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (query or "item").lower()).strip("-") or "item"


ebay_client = EbayClient()
