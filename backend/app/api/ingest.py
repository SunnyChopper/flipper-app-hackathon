from fastapi import APIRouter

from app.models.deal import Deal
from app.services.apify import facebook_marketplace
from app.services.ebay import ebay_client
from app.services.store import deal_store

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("/ebay", response_model=list[Deal])
async def ingest_ebay(query: str = "dyson vacuum") -> list[Deal]:
    listings = await ebay_client.search(query)
    return [await deal_store.ingest(listing) for listing in listings]


@router.post("/facebook", response_model=list[Deal])
async def ingest_facebook(query: str = "kitchenaid mixer") -> list[Deal]:
    listings = await facebook_marketplace.search(query)
    return [await deal_store.ingest(listing) for listing in listings]
