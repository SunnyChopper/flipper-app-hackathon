from fastapi import APIRouter

from app.repositories.memory_store import DEMO_USER
from app.schemas.profile import ProfileResponse, UpdateProfileRequest
from app.services.profile_service import profile_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileResponse)
def get_profile() -> ProfileResponse:
    return profile_service.get_profile(DEMO_USER)


@router.put("", response_model=ProfileResponse)
def update_profile(payload: UpdateProfileRequest) -> ProfileResponse:
    return profile_service.update_profile(DEMO_USER, payload)
