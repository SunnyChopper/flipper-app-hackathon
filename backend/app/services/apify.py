from app.config import settings
from app.models.listing import Listing


class FacebookMarketplaceClient:
    """Collect Facebook Marketplace data via Apify. Mocks until APIFY_TOKEN is set."""

    async def search(self, query: str, location: str = "united-states") -> list[Listing]:
        if not settings.apify_token:
            return [
                Listing(
                    id="fb-mock-1",
                    source="facebook",
                    external_id="fb-mock-1",
                    title=query or "KitchenAid mixer, bowl dented, runs great",
                    description="Red tilt-head mixer. Small dent in bowl. Seller wants gone today.",
                    price=65,
                    url="https://www.facebook.com/marketplace/item/mock-kitchenaid",
                    image_url="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800",
                    location=location,
                    raw={"mock": True, "actor": "facebook-marketplace"},
                )
            ]

        # Call an Apify Marketplace actor with settings.apify_token, then map items to Listing.
        raise NotImplementedError("Live Apify Facebook Marketplace runs are not wired yet.")


facebook_marketplace = FacebookMarketplaceClient()
