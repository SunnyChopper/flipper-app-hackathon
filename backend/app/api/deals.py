from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from app.models.deal import Deal, DealFilters
from app.services.store import deal_store

router = APIRouter(prefix="/api/deals", tags=["deals"])

Source = Literal["ebay", "facebook"]


@router.get("", response_model=list[Deal])
def list_deals(
    q: str | None = Query(default=None),
    source: Source | None = Query(default=None),
    min_profit: float | None = Query(default=None),
    max_risk: int | None = Query(default=None),
    min_score: int | None = Query(default=None),
) -> list[Deal]:
    filters = DealFilters(
        q=q,
        source=source,
        min_profit=min_profit,
        max_risk=max_risk,
        min_score=min_score,
    )
    return deal_store.list_deals(filters)


@router.get("/{deal_id}", response_model=Deal)
def get_deal(deal_id: str) -> Deal:
    deal = deal_store.get_deal(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal
