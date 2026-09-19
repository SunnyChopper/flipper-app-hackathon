from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.domain.entities import UserDeal
from app.repositories.memory_store import MemoryStore, memory_store


class DealRepository:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or memory_store

    def get(self, user_id: str, listing_id: str) -> UserDeal | None:
        return self.store.user_deal_for(user_id, listing_id)

    def list_for_user(self, user_id: str, status: str | None = None) -> list[UserDeal]:
        deals = [deal for deal in self.store.user_deals.values() if deal.user_id == user_id]
        if status:
            deals = [deal for deal in deals if deal.status == status]
        return sorted(deals, key=lambda deal: deal.updated_at, reverse=True)

    def upsert(self, user_id: str, listing_id: str, status: str, notes: str | None) -> UserDeal:
        now = datetime.now(UTC)
        existing = self.store.user_deal_for(user_id, listing_id)
        if existing:
            existing.status = status
            existing.notes = notes
            existing.updated_at = now
            return existing
        deal = UserDeal(
            id=str(uuid4()),
            user_id=user_id,
            listing_id=listing_id,
            status=status,
            notes=notes,
            created_at=now,
            updated_at=now,
        )
        return self.store.upsert_user_deal(deal)

    def delete(self, user_id: str, listing_id: str) -> UserDeal | None:
        return self.store.delete_user_deal(user_id, listing_id)
