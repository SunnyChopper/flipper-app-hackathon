from datetime import datetime

from app.schemas.base import CamelModel


class CatalogProductSummaryResponse(CamelModel):
    id: str
    brand: str
    model: str
    variant: str | None = None
    category: str
    display_name: str
    estimated_working_market_value: float
    valuation_confidence_score: float


class CatalogProductDetailResponse(CatalogProductSummaryResponse):
    last_valuation_at: datetime | None = None
