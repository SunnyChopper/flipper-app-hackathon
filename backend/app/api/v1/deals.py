from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from app.auth import get_current_user_id
from app.schemas.common import UserDealStatus
from app.schemas.deal import SaveDealRequest, SavedDealListResponse, UserDealResponse
from app.services.deal_service import deal_service

router = APIRouter(prefix="/deals", tags=["deals"])


@router.get("", response_model=SavedDealListResponse)
def list_deals(
    user_id: Annotated[str, Depends(get_current_user_id)],
    status: UserDealStatus | None = Query(default=None),
) -> SavedDealListResponse:
    return deal_service.list_deals(user_id, status=status)


@router.put("/{listing_id}", response_model=UserDealResponse)
def upsert_deal(
    listing_id: str,
    payload: SaveDealRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> UserDealResponse:
    return deal_service.upsert_deal(user_id, listing_id, payload)


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deal(
    listing_id: str,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> Response:
    deal_service.delete_deal(user_id, listing_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
