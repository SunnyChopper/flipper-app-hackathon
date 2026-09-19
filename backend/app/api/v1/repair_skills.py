from fastapi import APIRouter

from app.schemas.bom import RepairSkillListResponse
from app.services.profile_service import profile_service

router = APIRouter(prefix="/repair-skills", tags=["repair-skills"])


@router.get("", response_model=RepairSkillListResponse)
def list_repair_skills() -> RepairSkillListResponse:
    return profile_service.list_repair_skills()
