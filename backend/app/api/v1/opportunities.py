from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query

from app.repositories.memory_store import DEMO_USER
from app.schemas.common import MarketplaceSource, OpportunitySort
from app.schemas.opportunity import OpportunityDetailResponse, OpportunityListResponse
from app.services.opportunity_service import OpportunityFilters, opportunity_service

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("", response_model=OpportunityListResponse)
def list_opportunities(
    q: str | None = None,
    source: MarketplaceSource | None = None,
    category: str | None = None,
    condition: str | None = None,
    persona: str | None = None,
    min_profit: Annotated[float | None, Query(alias="minProfit")] = None,
    min_roi: Annotated[float | None, Query(alias="minRoi")] = None,
    max_price: Annotated[float | None, Query(alias="maxPrice")] = None,
    required_skill: Annotated[str | None, Query(alias="requiredSkill")] = None,
    sort: OpportunitySort = OpportunitySort.score_desc,
    page: int = Query(1, ge=1),
    page_size: Annotated[int, Query(alias="pageSize", ge=1, le=100)] = 20,
) -> OpportunityListResponse:
    filters = OpportunityFilters(
        q=q,
        source=source,
        category=category,
        condition=condition,
        persona=persona,
        min_profit=min_profit,
        min_roi=min_roi,
        max_price=max_price,
        required_skill=required_skill,
        sort=sort,
        page=page,
        page_size=page_size,
    )
    return opportunity_service.list_opportunities(DEMO_USER, filters)


@router.get("/{listing_id}", response_model=OpportunityDetailResponse)
def get_opportunity(listing_id: str) -> OpportunityDetailResponse:
    return opportunity_service.get_opportunity(DEMO_USER, listing_id)
