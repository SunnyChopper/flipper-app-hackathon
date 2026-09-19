from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException

from app.domain.entities import Profile, SavedSearch
from app.repositories.profile_repository import ProfileRepository
from app.schemas.bom import RepairSkillListResponse, RepairSkillResponse
from app.schemas.profile import (
    CreateSearchRequest,
    ProfileResponse,
    SavedSearchResponse,
    UpdateProfileRequest,
)


class ProfileService:
    def __init__(self, profiles: ProfileRepository | None = None) -> None:
        self.profiles = profiles or ProfileRepository()

    def get_profile(self, user_id: str) -> ProfileResponse:
        profile = self.profiles.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        skills = [
            RepairSkillResponse(slug=skill.slug, display_name=skill.display_name, category=skill.category)
            for skill in self.profiles.skills_for_user(user_id)
        ]
        return ProfileResponse(
            id=profile.id,
            persona=profile.persona,  # type: ignore[arg-type]
            min_profit_margin_usd=profile.min_profit_margin_usd,
            min_roi_percent=profile.min_roi_percent,
            skills=skills,
        )

    def update_profile(self, user_id: str, payload: UpdateProfileRequest) -> ProfileResponse:
        known = {skill.slug for skill in self.profiles.all_repair_skills()}
        unknown = [slug for slug in payload.skill_slugs if slug not in known]
        if unknown:
            raise HTTPException(status_code=400, detail=f"Unknown repair skills: {', '.join(unknown)}")
        profile = Profile(
            id=user_id,
            persona=payload.persona,
            min_profit_margin_usd=payload.min_profit_margin_usd,
            min_roi_percent=payload.min_roi_percent,
        )
        self.profiles.upsert_profile(profile)
        self.profiles.replace_skills(user_id, payload.skill_slugs)
        return self.get_profile(user_id)

    def list_repair_skills(self) -> RepairSkillListResponse:
        items = [
            RepairSkillResponse(slug=skill.slug, display_name=skill.display_name, category=skill.category)
            for skill in self.profiles.all_repair_skills()
        ]
        return RepairSkillListResponse(items=items)

    def list_searches(self, user_id: str) -> list[SavedSearchResponse]:
        return [
            SavedSearchResponse(
                id=search.id,
                name=search.name,
                query=search.query,
                filters=search.filters,
                notify=search.notify,
                created_at=search.created_at.isoformat(),
            )
            for search in self.profiles.list_searches(user_id)
        ]

    def create_search(self, user_id: str, payload: CreateSearchRequest) -> SavedSearchResponse:
        search = SavedSearch(
            id=str(uuid4()),
            user_id=user_id,
            name=payload.name,
            query=payload.query,
            filters=payload.filters,
            notify=payload.notify,
            created_at=datetime.now(UTC),
        )
        saved = self.profiles.save_search(search)
        return SavedSearchResponse(
            id=saved.id,
            name=saved.name,
            query=saved.query,
            filters=saved.filters,
            notify=saved.notify,
            created_at=saved.created_at.isoformat(),
        )


profile_service = ProfileService()
