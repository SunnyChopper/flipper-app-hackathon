from __future__ import annotations

from app.domain.entities import Profile, RepairSkill, SavedSearch, UserSkill
from app.repositories.memory_store import MemoryStore, memory_store


class ProfileRepository:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or memory_store

    def get_profile(self, user_id: str) -> Profile | None:
        return self.store.profiles.get(user_id)

    def upsert_profile(self, profile: Profile) -> Profile:
        self.store.profiles[profile.id] = profile
        return profile

    def skills_for_user(self, user_id: str) -> list[RepairSkill]:
        slugs = {skill.skill_slug for skill in self.store.user_skills if skill.user_id == user_id}
        return [skill for slug, skill in self.store.repair_skills.items() if slug in slugs]

    def user_skill_slugs(self, user_id: str) -> set[str]:
        return {skill.skill_slug for skill in self.store.user_skills if skill.user_id == user_id}

    def replace_skills(self, user_id: str, skill_slugs: list[str]) -> list[UserSkill]:
        self.store.replace_user_skills(user_id, skill_slugs)
        return [skill for skill in self.store.user_skills if skill.user_id == user_id]

    def all_repair_skills(self) -> list[RepairSkill]:
        return list(self.store.repair_skills.values())

    def list_searches(self, user_id: str) -> list[SavedSearch]:
        return [search for search in self.store.searches.values() if search.user_id == user_id]

    def save_search(self, search: SavedSearch) -> SavedSearch:
        self.store.searches[search.id] = search
        return search
