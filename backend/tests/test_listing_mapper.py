from app.models.sources import EbayApifyItem, FacebookMarketplaceItem
from app.services.listing_mapper import listing_from_ebay, listing_from_facebook


def test_facebook_mapper_accepts_apify_detail_payload():
    item = FacebookMarketplaceItem.model_validate(
        {
            "id": "123",
            "listingUrl": "https://www.facebook.com/marketplace/item/123",
            "marketplace_listing_title": "iPhone 13 cracked screen",
            "listing_price": {"amount": "80", "formatted_amount": "$80"},
            "primary_listing_photo": {
                "__typename": "Photo",
                "id": "p1",
                "photo_image_url": "https://example.com/p.jpg",
            },
            "location": {
                "reverse_geocode": {
                    "city": "Austin",
                    "state": "TX",
                    "city_page": {"display_name": "Austin, TX", "id": "1"},
                }
            },
            "isHidden": False,
            "isLive": True,
            "isPending": False,
            "isSold": False,
            "description": {"text": "Does not work. Cracked screen."},
            "condition": "Used - Fair",
        }
    )

    listing = listing_from_facebook(item)
    assert listing is not None
    assert listing.source == "facebook"
    assert listing.title == "iPhone 13 cracked screen"
    assert listing.price == 80
    assert listing.image_url == "https://example.com/p.jpg"
    assert listing.description == "Does not work. Cracked screen."
    assert listing.location == "Austin, TX"
    assert listing.condition_label == "Used - Fair"
    assert listing.currency == "USD"


def test_ebay_mapper_keeps_usd_and_drops_foreign_prices():
    usd = EbayApifyItem.model_validate(
        {
            "itemId": "111",
            "title": "iPhone 13 cracked screen for parts",
            "url": "https://www.ebay.com/itm/111",
            "price": 80,
            "currency": "USD",
            "formattedPrice": "$80.00",
            "shipping": "Free shipping",
            "condition": "For parts or not working",
        }
    )
    listing = listing_from_ebay(usd)
    assert listing is not None
    assert listing.currency == "USD"
    assert listing.price == 80

    zar = EbayApifyItem.model_validate(
        {
            "itemId": "222",
            "title": "iPhone 13 cracked screen for parts",
            "url": "https://www.ebay.com/itm/222",
            "price": 4063.1,
            "currency": "USD",
            "formattedPrice": "ZAR 4,063.10",
            "shipping": "+ZAR 661.80 delivery",
            "condition": "For parts or not working",
        }
    )
    assert listing_from_ebay(zar) is None


def test_facebook_mapper_drops_non_usd_prices():
    item = FacebookMarketplaceItem.model_validate(
        {
            "id": "999",
            "listingUrl": "https://www.facebook.com/marketplace/item/999",
            "marketplace_listing_title": "iPhone 13 cracked",
            "listing_price": {"amount": "80", "currency": "EUR", "formatted_amount": "€80"},
        }
    )
    assert listing_from_facebook(item) is None
