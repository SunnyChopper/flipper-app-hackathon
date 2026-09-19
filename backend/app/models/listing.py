from typing import Any, Literal

from pydantic import BaseModel, Field


Marketplace = Literal["ebay", "facebook"]


class Listing(BaseModel):
    """Canonical marketplace listing. Adapters map eBay / Apify payloads into this shape."""

    id: str
    source: Marketplace
    external_id: str
    title: str
    description: str = ""
    price: float
    currency: str = "USD"
    url: str
    image_url: str | None = None
    location: str | None = None
    condition_label: str | None = None
    seller_name: str | None = None
    shipping_cost: float | None = None
    is_sold: bool = False
    raw: dict[str, Any] = Field(default_factory=dict, exclude=True)


class NormalizedProduct(BaseModel):
    listing_id: str
    brand: str | None = None
    model: str | None = None
    category: str = "unknown"
    condition: str = "used"
    normalized_title: str
    attributes: dict[str, Any] = Field(default_factory=dict)
