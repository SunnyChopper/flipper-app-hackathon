from app.models.listing import Listing
from app.services.condition_filter import looks_broken_or_poor


def _listing(**overrides: object) -> Listing:
    payload = {
        "id": "listing-1",
        "source": "ebay",
        "external_id": "1",
        "title": "iPhone 13",
        "description": "Works great",
        "price": 200,
        "url": "https://www.ebay.com/itm/1",
        "condition_label": "Used",
    }
    payload.update(overrides)
    return Listing.model_validate(payload)


def test_keeps_for_parts_and_cracked_listings():
    assert looks_broken_or_poor(
        _listing(title="iPhone 13 for parts", condition_label="For parts or not working")
    )
    assert looks_broken_or_poor(
        _listing(title="Samsung TV", description="No picture, sold as-is for repair", condition_label="Used")
    )
    assert looks_broken_or_poor(_listing(title="Laptop cracked screen", condition_label="Damaged"))
    assert looks_broken_or_poor(_listing(title="iPad", description="Heavy wear", condition_label="Used - Fair"))


def test_rejects_working_and_like_new_listings():
    assert not looks_broken_or_poor(_listing(title="iPhone 13 unlocked", description="Works perfectly"))
    assert not looks_broken_or_poor(
        _listing(title="OLED TV like new", description="Excellent condition", condition_label="Used")
    )
    assert not looks_broken_or_poor(
        _listing(title="Brand new iPad", description="Never used", condition_label="New")
    )
