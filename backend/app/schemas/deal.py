from datetime import datetime

from app.schemas.base import CamelModel
from app.schemas.common import UserDealStatus
from app.schemas.opportunity import OpportunitySummaryResponse, UserDealSummaryResponse


class SaveDealRequest(CamelModel):
    status: UserDealStatus = "saved"
    notes: str | None = None


class UserDealResponse(CamelModel):
    id: str
    listing_id: str
    status: UserDealStatus
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class SavedDealItemResponse(CamelModel):
    user_deal: UserDealSummaryResponse
    opportunity: OpportunitySummaryResponse


class SavedDealListResponse(CamelModel):
    items: list[SavedDealItemResponse]
