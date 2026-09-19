from app.data.ids import BOM_IPHONE_SCREEN, PROD_IPHONE, COMP_OLED_SCREEN
from app.repositories.product_repository import ProductRepository
from tests.test_supabase_listing_repository import FakeClient


def test_bom_by_ids_skips_empty_without_query():
    repo = ProductRepository(client=object())
    assert repo.bom_by_ids([]) == []


def test_bom_by_ids_caches_supabase_rows():
    client = FakeClient(
        {
            "product_bom_items": [
                {
                    "id": BOM_IPHONE_SCREEN,
                    "product_id": PROD_IPHONE,
                    "component_id": COMP_OLED_SCREEN,
                    "required_skill_slug": "screen_swap",
                    "avg_replacement_cost": 90,
                    "salvage_resale_value": 20,
                    "harvest_liquidity_score": 8,
                }
            ]
        }
    )
    repo = ProductRepository(client=client)
    first = repo.bom_by_ids([BOM_IPHONE_SCREEN])
    second = repo.bom_by_ids([BOM_IPHONE_SCREEN])
    assert [item.id for item in first] == [BOM_IPHONE_SCREEN]
    assert [item.id for item in second] == [BOM_IPHONE_SCREEN]
    assert first[0].avg_replacement_cost == 90
