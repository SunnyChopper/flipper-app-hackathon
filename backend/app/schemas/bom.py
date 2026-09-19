from app.schemas.base import CamelModel


class DefectiveComponentResponse(CamelModel):
    bom_item_id: str
    component_id: str
    component_name: str
    required_skill_slug: str
    required_skill_display_name: str
    avg_replacement_cost: float
    salvage_resale_value: float
    harvest_liquidity_score: int


class RepairSkillResponse(CamelModel):
    slug: str
    display_name: str
    category: str


class RepairSkillSummaryResponse(RepairSkillResponse):
    user_has_skill: bool


class RepairSkillListResponse(CamelModel):
    items: list[RepairSkillResponse]
