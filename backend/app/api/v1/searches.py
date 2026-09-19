from fastapi import APIRouter

from app.repositories.memory_store import DEMO_USER
from app.schemas.profile import CreateSearchRequest, SavedSearchResponse
from app.services.profile_service import profile_service

router = APIRouter(prefix="/searches", tags=["searches"])


@router.get("", response_model=list[SavedSearchResponse])
def list_searches() -> list[SavedSearchResponse]:
    return profile_service.list_searches(DEMO_USER)


@router.post("", response_model=SavedSearchResponse)
def create_search(payload: CreateSearchRequest) -> SavedSearchResponse:
    return profile_service.create_search(DEMO_USER, payload)
