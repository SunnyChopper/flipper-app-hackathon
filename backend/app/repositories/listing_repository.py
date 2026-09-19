from __future__ import annotations

import logging

from app.domain.entities import CatalogProduct, Listing, UserDeal
from app.repositories.mappers import catalog_product_from_row, listing_from_row, listing_to_row, user_deal_from_row
from app.repositories.memory_store import MemoryStore, memory_store
from app.services.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)


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

    def insert_if_new(self, listing: Listing) -> tuple[Listing, bool]:
        """Insert a listing or skip when (source, external_id) or url already exists."""
        if self.client:
            return self._insert_remote_if_new(listing)
        return self.store.insert_listing_if_new(listing)

    def _insert_remote_if_new(self, listing: Listing) -> tuple[Listing, bool]:
        duplicate = self._find_remote_duplicate(listing)
        if duplicate:
            return duplicate, False
        row = listing_to_row(listing)
        try:
            result = self.client.table("listings").insert(row).execute()
        except Exception as exc:
            if _is_unique_violation(exc):
                existing = self._find_remote_duplicate(listing)
                if existing:
                    return existing, False
                logger.info("Skipped duplicate listing %s/%s", listing.source, listing.external_id)
                return listing, False
            raise
        inserted = (result.data or [row])[0]
        return listing_from_row(inserted), True

    def _find_remote_duplicate(self, listing: Listing) -> Listing | None:
        by_source = self._select(
            "listings",
            source=listing.source,
            external_id=listing.external_id,
        )
        if by_source:
            return listing_from_row(by_source[0])
        by_url = self._select("listings", url=listing.url)
        if by_url:
            return listing_from_row(by_url[0])
        return None

    def _select(self, table: str, **eq: str) -> list[dict]:
        query = self.client.table(table).select("*")
        for column, value in eq.items():
            query = query.eq(column, value)
        result = query.execute()
        return list(result.data or [])


def _is_unique_violation(exc: Exception) -> bool:
    code = getattr(exc, "code", None)
    if code == "23505":
        return True
    details = exc.args[0] if exc.args else None
    if isinstance(details, dict) and details.get("code") == "23505":
        return True
    text = str(getattr(exc, "message", "") or exc)
    return "23505" in text or "duplicate key" in text.lower()
