from app.schemas.base import CamelModel


class MarketCompSummaryResponse(CamelModel):
    id: str
    source: str
    sold_price: float
    shipping_price: float
    total_price: float
    item_condition: str
    sold_date: str
    listing_url: str
