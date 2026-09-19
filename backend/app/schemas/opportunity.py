from datetime import datetime

from app.schemas.base import CamelModel
from app.schemas.bom import DefectiveComponentResponse, RepairSkillSummaryResponse
from app.schemas.catalog_product import CatalogProductDetailResponse, CatalogProductSummaryResponse
from app.schemas.common import MarketplaceSource, UserDealStatus
from app.schemas.listing import ListingDetailResponse
from app.schemas.market_comp import MarketCompSummaryResponse


class DealScoreResponse(CamelModel):
    total: int
    restorer_score: int
    harvester_score: int
    valuation_confidence: float


class OpportunityFinancialsResponse(CamelModel):
    purchase_price: float
    shipping_cost: float
    total_replacement_cost: float
    total_acquisition_and_repair_cost: float
    estimated_working_market_value: float
    projected_restorer_net: float
    projected_harvest_yield: float
    roi_percent: float


class OpportunitySummaryResponse(CamelModel):
    listing_id: str
    source: MarketplaceSource
    title: str
    description: str | None = None
    url: str
    price: float
    shipping_cost: float
    image_url: str | None = None
    condition: str
    listed_at: datetime | None = None
    product: CatalogProductSummaryResponse | None = None
    required_repair_skills: list[str]
    projected_restorer_net: float
    projected_harvest_yield: float
    estimated_repair_cost: float
    deal_score: int
    user_deal_status: UserDealStatus | None = None


class OpportunityListResponse(CamelModel):
    items: list[OpportunitySummaryResponse]
    page: int
    page_size: int
    total: int


class UserDealSummaryResponse(CamelModel):
    id: str
    listing_id: str | None = None
    status: UserDealStatus
    notes: str | None = None
    created_at: datetime
    updated_at: datetime | None = None


class OpportunityDetailResponse(CamelModel):
    listing: ListingDetailResponse
    product: CatalogProductDetailResponse | None = None
    defects: list[DefectiveComponentResponse]
    required_skills: list[RepairSkillSummaryResponse]
    market_comps: list[MarketCompSummaryResponse]
    financials: OpportunityFinancialsResponse
    deal_score: DealScoreResponse
    user_deal: UserDealSummaryResponse | None = None
