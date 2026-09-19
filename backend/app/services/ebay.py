from __future__ import annotations

import logging

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

    async def search(self, query: str, limit: int = 8) -> list[Listing]:
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
        label = query or "Dyson V11 Outsize, battery weak"
        return [
            Listing(
                id="ebay-mock-1",
                source="ebay",
                external_id="v1|mock|1",
                title=f"{label} — local auction find" if query else label,
                description="Powers on. Battery holds about 8 minutes. Includes wand and floor head.",
                price=89,
                url="https://www.ebay.com/itm/mock-dyson",
                image_url="https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800",
                location="Austin, TX",
                condition_label="Used",
                seller_name="mock-seller",
                shipping_cost=12.0,
                raw={"mock": True, "actor": settings.apify_ebay_actor, "query": query},
            ),
            Listing(
                id="ebay-mock-2",
                source="ebay",
                external_id="v1|mock|2",
                title=f"{query or 'iPhone 13'} cracked back glass, Face ID works",
                description="Unlocked. Screen is fine. Back glass spidered. Battery 87%.",
                price=140,
                url="https://www.ebay.com/itm/mock-iphone",
                image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800",
                location="Dallas, TX",
                condition_label="For parts or not working",
                seller_name="mock-phones",
                shipping_cost=0.0,
                raw={"mock": True, "actor": settings.apify_ebay_actor, "query": query},
            ),
        ]


ebay_client = EbayClient()
