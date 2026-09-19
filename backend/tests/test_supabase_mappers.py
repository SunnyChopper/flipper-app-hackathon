from app.data.ids import LISTING_IPHONE_CRACKED, PROD_IPHONE
from app.repositories.mappers import catalog_product_from_row, listing_from_row, user_deal_from_row


def test_listing_from_row_coerces_numeric_and_array_fields():
    listing = listing_from_row(
        {
            "id": LISTING_IPHONE_CRACKED,
            "source": "facebook_marketplace",
            "external_id": "fb-iphone-13-cracked",
            "url": "https://www.facebook.com/marketplace/item/mock-iphone-cracked",
            "title": "iPhone 13 128GB cracked screen works fine",
            "description": "Screen damaged but everything else works.",
            "price": "220.00",
            "shipping_cost": "0",
            "condition": "damaged",
            "image_urls": ["https://example.com/iphone.jpg"],
            "created_at": "2026-09-19T12:03:00Z",
            "listed_at": "2026-09-19T12:00:00Z",
            "matched_product_id": PROD_IPHONE,
            "detected_defective_bom_ids": ["51111111-1111-4111-8111-111111111111"],
            "required_repair_skills": ["screen_swap"],
            "projected_restorer_net": "115.00",
            "projected_harvest_yield": "-192.00",
        }
    )

    assert listing.id == LISTING_IPHONE_CRACKED
    assert listing.price == 220.0
    assert listing.shipping_cost == 0.0
    assert listing.projected_restorer_net == 115.0
    assert listing.projected_harvest_yield == -192.0
    assert listing.required_repair_skills == ["screen_swap"]
    assert listing.matched_product_id == PROD_IPHONE
    assert listing.listed_at is not None
    assert listing.listed_at.year == 2026


def test_catalog_product_from_row_coerces_decimals():
    product = catalog_product_from_row(
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
    )

    assert product.estimated_working_market_value == 425.0
    assert product.valuation_confidence_score == 0.92


def test_user_deal_from_row_maps_status_and_timestamps():
    deal = user_deal_from_row(
        {
            "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
            "user_id": "00000000-0000-4000-8000-000000000001",
            "listing_id": LISTING_IPHONE_CRACKED,
            "status": "saved",
            "notes": None,
            "created_at": "2026-09-19T12:00:00Z",
            "updated_at": "2026-09-19T12:05:00Z",
        }
    )

    assert deal.status == "saved"
    assert deal.listing_id == LISTING_IPHONE_CRACKED
    assert deal.notes is None
