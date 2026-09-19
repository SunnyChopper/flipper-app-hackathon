from __future__ import annotations

from uuid import uuid4

from app.data.ids import DEMO_USER_ID
from app.data.seed import build_seed
from app.domain.entities import (
    CatalogProduct,
    Component,
    Listing,
    ProductBOMItem,
    ProductMarketComp,
    Profile,
    RepairSkill,
    SavedSearch,
    UserDeal,
    UserSkill,
)


class MemoryStore:
    """In-memory stand-in for the contract tables.

    Local demo and tests run without Supabase. Method names stay stable so a
    Postgres-backed repository can replace this later.
    """

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        seed = build_seed()
        self.repair_skills: dict[str, RepairSkill] = {item.slug: item for item in seed.repair_skills}
        self.products: dict[str, CatalogProduct] = {item.id: item for item in seed.catalog_products}
        self.components: dict[str, Component] = {item.id: item for item in seed.components}
        self.bom_items: dict[str, ProductBOMItem] = {item.id: item for item in seed.bom_items}
        self.market_comps: dict[str, ProductMarketComp] = {item.id: item for item in seed.market_comps}
        self.listings: dict[str, Listing] = {item.id: item for item in seed.listings}
        self.profiles: dict[str, Profile] = {seed.profile.id: seed.profile}
        self.user_skills: list[UserSkill] = list(seed.user_skills)
        self.user_deals: dict[str, UserDeal] = {}
        self.searches: dict[str, SavedSearch] = {}

    def upsert_listing(self, listing: Listing) -> Listing:
        for existing in list(self.listings.values()):
            if existing.source == listing.source and existing.external_id == listing.external_id:
                listing.id = existing.id
                self.listings[existing.id] = listing
                return listing
        self.listings[listing.id] = listing
        return listing

    def user_deal_for(self, user_id: str, listing_id: str) -> UserDeal | None:
        for deal in self.user_deals.values():
            if deal.user_id == user_id and deal.listing_id == listing_id:
                return deal
        return None

    def upsert_user_deal(self, deal: UserDeal) -> UserDeal:
        existing = self.user_deal_for(deal.user_id, deal.listing_id)
        if existing:
            existing.status = deal.status
            existing.notes = deal.notes
            existing.updated_at = deal.updated_at
            return existing
        if not deal.id:
            deal.id = str(uuid4())
        self.user_deals[deal.id] = deal
        return deal

    def delete_user_deal(self, user_id: str, listing_id: str) -> UserDeal | None:
        deal = self.user_deal_for(user_id, listing_id)
        if not deal:
            return None
        self.user_deals.pop(deal.id, None)
        return deal

    def replace_user_skills(self, user_id: str, skill_slugs: list[str]) -> None:
        self.user_skills = [skill for skill in self.user_skills if skill.user_id != user_id]
        self.user_skills.extend(UserSkill(user_id=user_id, skill_slug=slug) for slug in skill_slugs)


memory_store = MemoryStore()
DEMO_USER = DEMO_USER_ID
