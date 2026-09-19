from uuid import uuid4

from app.models.deal import Deal, DealFilters
from app.models.listing import Listing, NormalizedProduct
from app.models.search import SavedSearch, SavedSearchCreate
from app.services.analyzer import analyzer
from app.services.deal_scorer import deal_scorer


def _listing(
    listing_id: str,
    source: str,
    title: str,
    price: float,
    url: str,
    image_url: str,
    location: str,
    description: str,
) -> Listing:
    return Listing(
        id=listing_id,
        source=source,  # type: ignore[arg-type]
        external_id=listing_id,
        title=title,
        description=description,
        price=price,
        url=url,
        image_url=image_url,
        location=location,
        raw={"seed": True},
    )


SEED_LISTINGS = [
    _listing(
        "seed-dyson",
        "ebay",
        "Dyson V11 Outsize, battery weak, otherwise clean",
        89,
        "https://www.ebay.com/itm/mock-dyson",
        "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=900",
        "Austin, TX",
        "Runs. Battery dies fast. Wand and floor head included.",
    ),
    _listing(
        "seed-kitchenaid",
        "facebook",
        "KitchenAid stand mixer, bowl dented, motor strong",
        65,
        "https://www.facebook.com/marketplace/item/mock-kitchenaid",
        "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=900",
        "Chicago, IL",
        "Red tilt-head. Small dent in bowl. Seller wants it gone today.",
    ),
    _listing(
        "seed-iphone",
        "ebay",
        "iPhone 13 128GB, cracked back glass, Face ID works",
        140,
        "https://www.ebay.com/itm/mock-iphone",
        "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=900",
        "Dallas, TX",
        "Unlocked. Screen is fine. Back glass spidered. Battery 87%.",
    ),
    _listing(
        "seed-dewalt",
        "facebook",
        "DeWalt 20V drill + 2 batteries, missing charger",
        40,
        "https://www.facebook.com/marketplace/item/mock-dewalt",
        "https://images.unsplash.com/photo-1504148455328-c376907d081c?w=900",
        "Denver, CO",
        "Both packs take a charge. No charger in the box.",
    ),
]


class DealStore:
    """In-memory store for the hackathon demo.

    Swap list methods for Supabase table reads when SUPABASE_URL is configured.
    Keep the public method names so API routes do not change.
    """

    def __init__(self) -> None:
        self.deals: dict[str, Deal] = {}
        self.searches: dict[str, SavedSearch] = {}
        self._seed()

    def _seed(self) -> None:
        for listing in SEED_LISTINGS:
            product = analyzer._heuristic_normalize(listing)
            deal = deal_scorer.score(listing, product)
            self.deals[listing.id] = deal

        demo = SavedSearch(
            id="search-tools",
            name="Cordless tools under $50",
            query="dewalt milwaukee makita",
            filters={"max_risk": 60, "min_profit": 40},
            notify=True,
        )
        self.searches[demo.id] = demo

    def list_deals(self, filters: DealFilters) -> list[Deal]:
        deals = list(self.deals.values())
        query = (filters.q or "").strip().lower()
        if query:
            deals = [
                deal
                for deal in deals
                if query in deal.listing.title.lower() or query in deal.product.category.lower()
            ]
        if filters.source:
            deals = [deal for deal in deals if deal.listing.source == filters.source]
        if filters.min_profit is not None:
            deals = [deal for deal in deals if deal.score.net_profit >= filters.min_profit]
        if filters.max_risk is not None:
            deals = [deal for deal in deals if deal.score.risk_score <= filters.max_risk]
        if filters.min_score is not None:
            deals = [deal for deal in deals if deal.score.overall_score >= filters.min_score]
        return sorted(deals, key=lambda deal: deal.score.overall_score, reverse=True)

    def get_deal(self, deal_id: str) -> Deal | None:
        return self.deals.get(deal_id)

    async def ingest(self, listing: Listing) -> Deal:
        product: NormalizedProduct = await analyzer.normalize(listing)
        deal = deal_scorer.score(listing, product)
        self.deals[listing.id] = deal
        return deal

    def list_searches(self, user_id: str = "demo-user") -> list[SavedSearch]:
        return [search for search in self.searches.values() if search.user_id == user_id]

    def save_search(self, payload: SavedSearchCreate) -> SavedSearch:
        search = SavedSearch(id=str(uuid4()), **payload.model_dump())
        self.searches[search.id] = search
        return search


deal_store = DealStore()
