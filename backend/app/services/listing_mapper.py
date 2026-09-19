from __future__ import annotations

import re
from typing import Any

from app.models.listing import Listing
from app.models.sources import (
    EbayApifyItem,
    EbayImage,
    EbayItemLocation,
    EbaySeller,
    FacebookMarketplaceItem,
    MoneyAmount,
)

ITM_ID = re.compile(r"/itm/(?:[^/]*?/)?(\d{6,})")


def parse_money(value: MoneyAmount | str | float | int | None) -> tuple[float | None, str]:
    if value is None:
        return None, "USD"
    if isinstance(value, (int, float)):
        return float(value), "USD"
    if isinstance(value, str):
        return _float_from_text(value), "USD"
    amount = value.amount if value.amount is not None else value.value
    currency = value.currency or "USD"
    if amount is None and value.formatted_amount:
        return _float_from_text(value.formatted_amount), currency
    if amount is None:
        return None, currency
    if isinstance(amount, (int, float)):
        return float(amount), currency
    return _float_from_text(str(amount)), currency


def _float_from_text(text: str) -> float | None:
    lowered = text.lower()
    if "free" in lowered:
        return 0.0
    cleaned = re.sub(r"[^\d.]", "", text)
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def compact_raw(source: str, extra: dict[str, Any]) -> dict[str, Any]:
    return {"source": source, **{key: value for key, value in extra.items() if value is not None}}


def listing_from_facebook(item: FacebookMarketplaceItem) -> Listing | None:
    external_id = str(item.id) if item.id is not None else None
    title = item.marketplace_listing_title or item.title or item.custom_title
    price, currency = parse_money(item.listing_price if item.listing_price is not None else item.price)
    url = item.listingUrl or (f"https://www.facebook.com/marketplace/item/{external_id}" if external_id else None)
    if not external_id or not title or price is None or not url:
        return None
    if item.is_hidden:
        return None

    location = _facebook_location(item)
    image_url = None
    if item.primary_listing_photo:
        if item.primary_listing_photo.image and item.primary_listing_photo.image.uri:
            image_url = item.primary_listing_photo.image.uri
        else:
            image_url = item.primary_listing_photo.uri

    description = (item.description or item.redacted_description or "").strip()
    seller = item.marketplace_listing_seller.name if item.marketplace_listing_seller else None

    return Listing(
        id=f"facebook-{external_id}",
        source="facebook",
        external_id=str(external_id),
        title=title.strip(),
        description=description,
        price=price,
        currency=currency,
        url=url,
        image_url=image_url,
        location=location,
        seller_name=seller,
        is_sold=item.is_sold or item.is_pending,
        raw=compact_raw(
            "facebook",
            {
                "category_id": item.marketplace_listing_category_id,
                "delivery_types": item.delivery_types,
                "is_live": item.is_live,
                "is_pending": item.is_pending,
                "is_sold": item.is_sold,
            },
        ),
    )


def listing_from_ebay(item: EbayApifyItem) -> Listing | None:
    url = item.url or item.itemUrl or item.itemWebUrl or item.link
    external_id = _ebay_external_id(item, url)
    title = (item.title or "").strip()
    price, currency = parse_money(item.price)
    if price is None:
        price, currency = parse_money(item.formattedPrice)
    if item.currency:
        currency = item.currency
    if not external_id or not title or price is None or not url:
        return None

    shipping, _ = parse_money(item.shippingCost if item.shippingCost is not None else item.shipping)
    seller = _ebay_seller_name(item.seller)
    image_url = _ebay_image(item)

    return Listing(
        id=f"ebay-{external_id}",
        source="ebay",
        external_id=external_id,
        title=title,
        description=(item.description or item.shortDescription or "").strip(),
        price=price,
        currency=currency,
        url=url,
        image_url=image_url,
        location=_ebay_location(item),
        condition_label=item.condition,
        seller_name=seller,
        shipping_cost=shipping,
        raw=compact_raw(
            "ebay",
            {
                "buying_format": item.buyingFormat,
                "feedback": item.sellerFeedbackPercent,
                "marketplace": item.marketplace,
                "sponsored": item.isSponsored,
                "actor": "apify",
            },
        ),
    )


def _ebay_external_id(item: EbayApifyItem, url: str | None) -> str | None:
    if item.itemId is not None:
        return str(item.itemId)
    if item.id is not None:
        return str(item.id)
    if url:
        match = ITM_ID.search(url)
        if match:
            return match.group(1)
    return None


def _ebay_image(item: EbayApifyItem) -> str | None:
    if item.imageUrl:
        return item.imageUrl
    if isinstance(item.image, str):
        return item.image
    if isinstance(item.image, EbayImage):
        return item.image.imageUrl
    if item.images:
        return item.images[0]
    return item.thumbnail


def _ebay_seller_name(seller: EbaySeller | str | None) -> str | None:
    if seller is None:
        return None
    if isinstance(seller, str):
        return seller
    return seller.username


def _ebay_location(item: EbayApifyItem) -> str | None:
    if isinstance(item.itemLocation, str) and item.itemLocation.strip():
        return item.itemLocation.strip()
    if isinstance(item.itemLocation, EbayItemLocation):
        parts = [part for part in (item.itemLocation.city, item.itemLocation.stateOrProvince) if part]
        if parts:
            return ", ".join(parts)
        return item.itemLocation.country
    if item.location:
        return item.location
    return None


def _facebook_location(item: FacebookMarketplaceItem) -> str | None:
    loc = item.location
    if not loc:
        return None
    if loc.reverse_geocode:
        geo = loc.reverse_geocode
        if geo.city_page and geo.city_page.display_name:
            return geo.city_page.display_name
        parts = [part for part in (geo.city, geo.state) if part]
        if parts:
            return ", ".join(parts)
    parts = [part for part in (loc.city, loc.state) if part]
    return ", ".join(parts) or None
