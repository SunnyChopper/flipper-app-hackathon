from __future__ import annotations

from datetime import UTC, datetime

from app.domain.entities import Profile, RepairSkill, SavedSearch, UserSkill
from app.repositories.mappers import profile_from_row, repair_skill_from_row, saved_search_from_row
from app.repositories.memory_store import MemoryStore, memory_store
from app.services.supabase_client import get_supabase_client


class ProfileRepository:
    def __init__(self, store: MemoryStore | None = None, client=None) -> None:
        self.store = store or memory_store
        self._client = client
        self._client_bound = client is not None

    @property
    def client(self):
        if not self._client_bound:
            self._client = get_supabase_client()
            self._client_bound = True
        return self._client

    @client.setter
    def client(self, value) -> None:
        self._client = value
        self._client_bound = True

    def get_profile(self, user_id: str) -> Profile | None:
        if self.client:
            rows = self._select("profiles", id=user_id)
            return profile_from_row(rows[0]) if rows else None
        return self.store.profiles.get(user_id)

    def ensure_profile(self, user_id: str) -> Profile:
        existing = self.get_profile(user_id)
        if existing:
            return existing
        profile = Profile(
            id=user_id,
            persona="restorer",
            min_profit_margin_usd=100,
            min_roi_percent=20,
        )
        self.upsert_profile(profile)
        self.replace_skills(user_id, ["screen_swap", "battery_replacement"])
        return profile

    def upsert_profile(self, profile: Profile) -> Profile:
        if self.client:
            self.client.table("profiles").upsert(
                {
                    "id": profile.id,
                    "persona": profile.persona,
                    "min_profit_margin_usd": profile.min_profit_margin_usd,
                    "min_roi_percent": profile.min_roi_percent,
                    "updated_at": datetime.now(UTC).isoformat(),
                }
            ).execute()
            return profile
        self.store.profiles[profile.id] = profile
        return profile

    def skills_for_user(self, user_id: str) -> list[RepairSkill]:
        slugs = self.user_skill_slugs(user_id)
        if self.client:
            return [skill for skill in self.all_repair_skills() if skill.slug in slugs]
        return [skill for slug, skill in self.store.repair_skills.items() if slug in slugs]

    def user_skill_slugs(self, user_id: str) -> set[str]:
        if self.client:
            return {str(row["skill_slug"]) for row in self._select("user_skills", user_id=user_id)}
        return {skill.skill_slug for skill in self.store.user_skills if skill.user_id == user_id}

    def replace_skills(self, user_id: str, skill_slugs: list[str]) -> list[UserSkill]:
        if self.client:
            self.client.table("user_skills").delete().eq("user_id", user_id).execute()
            if skill_slugs:
                self.client.table("user_skills").insert(
                    [{"user_id": user_id, "skill_slug": slug} for slug in skill_slugs]
                ).execute()
            return [UserSkill(user_id=user_id, skill_slug=slug) for slug in skill_slugs]
        self.store.replace_user_skills(user_id, skill_slugs)
        return [skill for skill in self.store.user_skills if skill.user_id == user_id]

    def all_repair_skills(self) -> list[RepairSkill]:
        if self.client:
            return [repair_skill_from_row(row) for row in self._select("repair_skills")]
        return list(self.store.repair_skills.values())

    def list_searches(self, user_id: str) -> list[SavedSearch]:
        if self.client:
            return [saved_search_from_row(row) for row in self._select("saved_searches", user_id=user_id)]
        return [search for search in self.store.searches.values() if search.user_id == user_id]

    def save_search(self, search: SavedSearch) -> SavedSearch:
        if self.client:
            self.client.table("saved_searches").insert(
                {
                    "id": search.id,
                    "user_id": search.user_id,
                    "name": search.name,
                    "query": search.query,
                    "filters": search.filters,
                    "notify": search.notify,
                    "created_at": search.created_at.isoformat(),
                }
            ).execute()
            return search
        self.store.searches[search.id] = search
        return search

    def _select(self, table: str, **eq: str) -> list[dict]:
        query = self.client.table(table).select("*")
        for column, value in eq.items():
            query = query.eq(column, value)
        result = query.execute()
        return list(result.data or [])
