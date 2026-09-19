from app.schemas.base import CamelModel
from app.schemas.bom import RepairSkillResponse
from app.schemas.common import Persona


class ProfileResponse(CamelModel):
    id: str
    persona: Persona
    min_profit_margin_usd: float
    min_roi_percent: float
    skills: list[RepairSkillResponse]


class UpdateProfileRequest(CamelModel):
    persona: Persona
    min_profit_margin_usd: float
    min_roi_percent: float
    skill_slugs: list[str]


class CreateSearchRequest(CamelModel):
    name: str
    query: str = ""
    filters: dict = {}
    notify: bool = True


class SavedSearchResponse(CamelModel):
    id: str
    name: str
    query: str
    filters: dict
    notify: bool
    created_at: str | None = None
