from __future__ import annotations

from app.domain.entities import CatalogProduct, Listing, UserDeal
from app.repositories.memory_store import MemoryStore, memory_store


class ListingRepository:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or memory_store

    def list_with_product_and_deal(self, user_id: str) -> list[tuple[Listing, CatalogProduct | None, UserDeal | None]]:
        rows: list[tuple[Listing, CatalogProduct | None, UserDeal | None]] = []
        for listing in self.store.listings.values():
            product = self.store.products.get(listing.matched_product_id) if listing.matched_product_id else None
            deal = self.store.user_deal_for(user_id, listing.id)
            rows.append((listing, product, deal))
        return rows

    def get(self, listing_id: str) -> Listing | None:
        return self.store.listings.get(listing_id)
