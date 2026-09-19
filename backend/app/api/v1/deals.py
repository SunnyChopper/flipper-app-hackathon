from __future__ import annotations

from fastapi import APIRouter, Query, Response, status

from app.repositories.memory_store import DEMO_USER
from app.schemas.common import UserDealStatus
from app.schemas.deal import SaveDealRequest, SavedDealListResponse, UserDealResponse
from app.services.deal_service import deal_service

router = APIRouter(prefix="/deals", tags=["deals"])


@router.get("", response_model=SavedDealListResponse)
def list_deals(status: UserDealStatus | None = Query(default=None)) -> SavedDealListResponse:
    return deal_service.list_deals(DEMO_USER, status=status)


@router.put("/{listing_id}", response_model=UserDealResponse)
def upsert_deal(listing_id: str, payload: SaveDealRequest) -> UserDealResponse:
    return deal_service.upsert_deal(DEMO_USER, listing_id, payload)


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deal(listing_id: str) -> Response:
    deal_service.delete_deal(DEMO_USER, listing_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
