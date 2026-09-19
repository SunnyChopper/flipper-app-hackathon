from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth import get_current_user_id
from app.schemas.profile import CreateSearchRequest, SavedSearchResponse
from app.services.profile_service import profile_service

router = APIRouter(prefix="/searches", tags=["searches"])


@router.get("", response_model=list[SavedSearchResponse])
def list_searches(user_id: Annotated[str, Depends(get_current_user_id)]) -> list[SavedSearchResponse]:
    return profile_service.list_searches(user_id)


@router.post("", response_model=SavedSearchResponse)
def create_search(
    payload: CreateSearchRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> SavedSearchResponse:
    return profile_service.create_search(user_id, payload)
