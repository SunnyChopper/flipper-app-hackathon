from app.config import settings
from app.models.listing import Listing


class EbayClient:
    """Fetch eBay listings. Uses mock data until EBAY_APP_ID is set."""

    BROWSE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

    async def search(self, query: str, limit: int = 8) -> list[Listing]:
        if not settings.ebay_app_id:
            return [
                Listing(
                    id="ebay-mock-1",
                    source="ebay",
                    external_id="v1|mock|1",
                    title=f"{query} — local auction find" if query else "Dyson V11 Outsize, battery weak",
                    description="Powers on. Battery holds about 8 minutes. Includes wand and floor head.",
                    price=89,
                    url="https://www.ebay.com/itm/mock-dyson",
                    image_url="https://images.unsplash.com/photo-1558317374-067fb5f30001?w=800",
                    location="Austin, TX",
                    raw={"mock": True, "query": query},
                )
            ]

        # Wire Browse API here with an application token from EBAY_APP_ID / EBAY_CERT_ID.
        raise NotImplementedError("Live eBay Browse search is not wired yet. Keep using the mock path for the hackathon demo.")


ebay_client = EbayClient()
