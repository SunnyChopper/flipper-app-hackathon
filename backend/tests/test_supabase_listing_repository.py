from app.data.ids import LISTING_IPHONE_CRACKED, PROD_IPHONE
from app.repositories.listing_repository import ListingRepository


class FakeQuery:
    def __init__(self, rows: list[dict]):
        self._rows = list(rows)

    def select(self, *_args, **_kwargs):
        return self

    def eq(self, column: str, value: object):
        self._rows = [row for row in self._rows if str(row.get(column)) == str(value)]
        return self

    def limit(self, count: int):
        self._rows = self._rows[:count]
        return self

    def execute(self):
        return type("Result", (), {"data": self._rows})()


class FakeClient:
    def __init__(self, tables: dict[str, list[dict]]):
        self._tables = tables

    def table(self, name: str) -> FakeQuery:
        return FakeQuery(self._tables.get(name, []))


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
