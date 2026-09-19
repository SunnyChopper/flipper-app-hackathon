from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.domain.entities import UserDeal
from app.repositories.mappers import user_deal_from_row
from app.repositories.memory_store import MemoryStore, memory_store
from app.services.supabase_client import get_supabase_client


class DealRepository:
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

    def get(self, user_id: str, listing_id: str) -> UserDeal | None:
        if self.client:
            rows = self._select(user_id=user_id, listing_id=listing_id)
            return user_deal_from_row(rows[0]) if rows else None
        return self.store.user_deal_for(user_id, listing_id)

    def list_for_user(self, user_id: str, status: str | None = None) -> list[UserDeal]:
        if self.client:
            deals = [user_deal_from_row(row) for row in self._select(user_id=user_id)]
        else:
            deals = [deal for deal in self.store.user_deals.values() if deal.user_id == user_id]
        if status:
            deals = [deal for deal in deals if deal.status == status]
        return sorted(deals, key=lambda deal: deal.updated_at, reverse=True)

    def upsert(self, user_id: str, listing_id: str, status: str, notes: str | None) -> UserDeal:
        now = datetime.now(UTC)
        existing = self.get(user_id, listing_id)
        if self.client:
            payload = {
                "id": existing.id if existing else str(uuid4()),
                "user_id": user_id,
                "listing_id": listing_id,
                "status": status,
                "notes": notes,
                "created_at": (existing.created_at if existing else now).isoformat(),
                "updated_at": now.isoformat(),
            }
            result = self.client.table("user_deals").upsert(payload, on_conflict="user_id,listing_id").execute()
            rows = list(result.data or [])
            return user_deal_from_row(rows[0] if rows else payload)
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
        existing = self.get(user_id, listing_id)
        if not existing:
            return None
        if self.client:
            self.client.table("user_deals").delete().eq("user_id", user_id).eq("listing_id", listing_id).execute()
            return existing
        return self.store.delete_user_deal(user_id, listing_id)

    def _select(self, **eq: str) -> list[dict]:
        query = self.client.table("user_deals").select("*")
        for column, value in eq.items():
            query = query.eq(column, value)
        result = query.execute()
        return list(result.data or [])
