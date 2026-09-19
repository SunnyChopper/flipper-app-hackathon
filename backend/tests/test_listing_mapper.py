from app.models.sources import FacebookMarketplaceItem
from app.services.listing_mapper import listing_from_facebook


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
