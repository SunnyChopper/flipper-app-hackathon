from datetime import datetime

from app.schemas.base import CamelModel
from app.schemas.common import MarketplaceSource


class ListingDetailResponse(CamelModel):
    id: str
    source: MarketplaceSource
    external_id: str
    url: str
    title: str
    description: str | None = None
    price: float
    shipping_cost: float
    condition: str
    image_urls: list[str]
    listed_at: datetime | None = None
    created_at: datetime
    projected_restorer_net: float
    projected_harvest_yield: float
