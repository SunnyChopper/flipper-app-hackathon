from typing import Literal

from pydantic import BaseModel, Field

from app.models.listing import Listing, NormalizedProduct


class ScoreBreakdown(BaseModel):
    estimated_resale: float
    repair_estimate: float
    fees_estimate: float
    net_profit: float
    profit_margin: float
    risk_score: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)
    rationale: str


class Deal(BaseModel):
    listing: Listing
    product: NormalizedProduct
    score: ScoreBreakdown


class DealFilters(BaseModel):
    q: str | None = None
    source: Literal["ebay", "facebook"] | None = None
    min_profit: float | None = None
    max_risk: int | None = None
    min_score: int | None = None
