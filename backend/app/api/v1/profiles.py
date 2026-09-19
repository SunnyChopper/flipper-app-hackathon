from fastapi import APIRouter, Depends
from typing import Annotated

from app.auth import get_current_user_id
from app.schemas.profile import ProfileResponse, UpdateProfileRequest
from app.services.profile_service import profile_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileResponse)
def get_profile(user_id: Annotated[str, Depends(get_current_user_id)]) -> ProfileResponse:
    return profile_service.get_profile(user_id)


@router.put("", response_model=ProfileResponse)
def update_profile(
    payload: UpdateProfileRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> ProfileResponse:
    return profile_service.update_profile(user_id, payload)
