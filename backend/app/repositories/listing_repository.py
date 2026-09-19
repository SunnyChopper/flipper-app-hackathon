from __future__ import annotations

from app.domain.entities import CatalogProduct, Listing, UserDeal
from app.repositories.mappers import catalog_product_from_row, listing_from_row, user_deal_from_row
from app.repositories.memory_store import MemoryStore, memory_store
from app.services.supabase_client import get_supabase_client


class ListingRepository:
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

    def list_with_product_and_deal(self, user_id: str) -> list[tuple[Listing, CatalogProduct | None, UserDeal | None]]:
        if self.client:
            listings = [listing_from_row(row) for row in self._select("listings")]
            products = {
                product.id: product
                for product in (catalog_product_from_row(row) for row in self._select("catalog_products"))
            }
            deals = {
                deal.listing_id: deal
                for deal in (
                    user_deal_from_row(row)
                    for row in self._select("user_deals", user_id=user_id)
                )
            }
            return [
                (
                    listing,
                    products.get(listing.matched_product_id) if listing.matched_product_id else None,
                    deals.get(listing.id),
                )
                for listing in listings
            ]

        rows: list[tuple[Listing, CatalogProduct | None, UserDeal | None]] = []
        for listing in self.store.listings.values():
            product = self.store.products.get(listing.matched_product_id) if listing.matched_product_id else None
            deal = self.store.user_deal_for(user_id, listing.id)
            rows.append((listing, product, deal))
        return rows

    def get(self, listing_id: str) -> Listing | None:
        if self.client:
            rows = self._select("listings", id=listing_id)
            return listing_from_row(rows[0]) if rows else None
        return self.store.listings.get(listing_id)

    def _select(self, table: str, **eq: str) -> list[dict]:
        query = self.client.table(table).select("*")
        for column, value in eq.items():
            query = query.eq(column, value)
        result = query.execute()
        return list(result.data or [])
