from datetime import UTC, datetime

from app.data.ids import LISTING_IPHONE_CRACKED, PROD_IPHONE
from app.domain.entities import Listing
from app.repositories.listing_repository import ListingRepository
from app.repositories.mappers import listing_to_row


class UniqueViolation(Exception):
    code = "23505"


class FakeQuery:
    def __init__(self, rows: list[dict]):
        self._rows = rows
        self._pending: dict | None = None
        self._filtered = list(rows)

    def select(self, *_args, **_kwargs):
        self._filtered = list(self._rows)
        return self

    def insert(self, row: dict):
        self._pending = row
        return self

    def eq(self, column: str, value: object):
        self._filtered = [row for row in self._filtered if str(row.get(column)) == str(value)]
        return self

    def limit(self, count: int):
        self._filtered = self._filtered[:count]
        return self

    def execute(self):
        if self._pending is not None:
            row = self._pending
            self._pending = None
            for existing in self._rows:
                if existing.get("source") == row.get("source") and existing.get("external_id") == row.get(
                    "external_id"
                ):
                    raise UniqueViolation("duplicate key value violates unique constraint")
                if existing.get("url") == row.get("url"):
                    raise UniqueViolation("duplicate key value violates unique constraint")
            self._rows.append(row)
            return type("Result", (), {"data": [row]})()
        return type("Result", (), {"data": self._filtered})()


class FakeClient:
    def __init__(self, tables: dict[str, list[dict]]):
        self._tables = tables

    def table(self, name: str) -> FakeQuery:
        if name not in self._tables:
            self._tables[name] = []
        return FakeQuery(self._tables[name])


def test_listing_repository_reads_from_supabase_when_client_is_provided():
    client = FakeClient(
        {
            "listings": [
                {
                    "id": LISTING_IPHONE_CRACKED,
                    "source": "facebook_marketplace",
                    "external_id": "fb-iphone-13-cracked",
                    "url": "https://example.com/listing",
                    "title": "iPhone 13 cracked",
                    "description": "Works",
                    "price": "220.00",
                    "shipping_cost": "0",
                    "condition": "damaged",
                    "image_urls": [],
                    "created_at": "2026-09-19T12:03:00Z",
                    "listed_at": "2026-09-19T12:00:00Z",
                    "matched_product_id": PROD_IPHONE,
                    "detected_defective_bom_ids": [],
                    "required_repair_skills": ["screen_swap"],
                    "projected_restorer_net": "115.00",
                    "projected_harvest_yield": "-192.00",
                }
            ],
            "catalog_products": [
                {
                    "id": PROD_IPHONE,
                    "brand": "Apple",
                    "model": "iPhone 13",
                    "variant": "128GB Unlocked",
                    "category": "smartphones",
                    "estimated_working_market_value": "425.00",
                    "valuation_confidence_score": "0.920",
                    "last_valuation_at": "2026-09-19T10:00:00Z",
                }
            ],
            "user_deals": [],
        }
    )

    repo = ListingRepository(client=client)
    listing = repo.get(LISTING_IPHONE_CRACKED)
    assert listing is not None
    assert listing.title == "iPhone 13 cracked"
    assert listing.price == 220.0

    rows = repo.list_with_product_and_deal("00000000-0000-4000-8000-000000000001")
    assert len(rows) == 1
    joined_listing, product, deal = rows[0]
    assert joined_listing.id == LISTING_IPHONE_CRACKED
    assert product is not None
    assert product.brand == "Apple"
    assert deal is None


def test_insert_if_new_skips_duplicate_source_external_id_and_url():
    existing = {
        "id": LISTING_IPHONE_CRACKED,
        "source": "facebook_marketplace",
        "external_id": "fb-iphone-13-cracked",
        "url": "https://example.com/listing",
        "title": "iPhone 13 cracked",
        "description": "Works",
        "price": "220.00",
        "shipping_cost": "0",
        "condition": "damaged",
        "image_urls": [],
        "created_at": "2026-09-19T12:03:00Z",
        "listed_at": "2026-09-19T12:00:00Z",
        "matched_product_id": PROD_IPHONE,
        "detected_defective_bom_ids": [],
        "required_repair_skills": ["screen_swap"],
        "projected_restorer_net": "115.00",
        "projected_harvest_yield": "-192.00",
    }
    client = FakeClient({"listings": [existing]})
    repo = ListingRepository(client=client)

    now = datetime(2026, 9, 19, 13, 0, tzinfo=UTC)
    same_id = Listing(
        id="99999999-9999-4999-8999-999999999999",
        source="facebook_marketplace",
        external_id="fb-iphone-13-cracked",
        url="https://example.com/listing-new",
        title="Duplicate by source",
        price=10,
        shipping_cost=0,
        condition="used_fair",
        image_urls=[],
        created_at=now,
        projected_restorer_net=0,
        projected_harvest_yield=0,
    )
    stored, inserted = repo.insert_if_new(same_id)
    assert inserted is False
    assert stored.id == LISTING_IPHONE_CRACKED

    same_url = Listing(
        id="88888888-8888-4888-8888-888888888888",
        source="ebay",
        external_id="other-external",
        url="https://example.com/listing",
        title="Duplicate by url",
        price=10,
        shipping_cost=0,
        condition="used_fair",
        image_urls=[],
        created_at=now,
        projected_restorer_net=0,
        projected_harvest_yield=0,
    )
    stored_url, inserted_url = repo.insert_if_new(same_url)
    assert inserted_url is False
    assert stored_url.url == "https://example.com/listing"
    assert len(client._tables["listings"]) == 1

    fresh = Listing(
        id="77777777-7777-4777-8777-777777777777",
        source="ebay",
        external_id="brand-new-listing",
        url="https://example.com/brand-new",
        title="Fresh listing",
        price=99,
        shipping_cost=5,
        condition="used_fair",
        image_urls=["https://example.com/img.jpg"],
        created_at=now,
        projected_restorer_net=20,
        projected_harvest_yield=0,
    )
    stored_new, inserted_new = repo.insert_if_new(fresh)
    assert inserted_new is True
    assert stored_new.title == "Fresh listing"
    assert len(client._tables["listings"]) == 2
    assert listing_to_row(fresh)["url"] == "https://example.com/brand-new"
