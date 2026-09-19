from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RepairSkill:
    slug: str
    display_name: str
    category: str


@dataclass
class Profile:
    id: str
    persona: str
    min_profit_margin_usd: float
    min_roi_percent: float


@dataclass
class UserSkill:
    user_id: str
    skill_slug: str


@dataclass
class CatalogProduct:
    id: str
    brand: str
    model: str
    variant: str | None
    category: str
    estimated_working_market_value: float
    valuation_confidence_score: float
    last_valuation_at: datetime | None = None


@dataclass
class ProductMarketComp:
    id: str
    product_id: str
    source: str
    sold_price: float
    shipping_price: float
    item_condition: str
    sold_date: str
    listing_url: str


@dataclass
class Component:
    id: str
    name: str


@dataclass
class ProductBOMItem:
    id: str
    product_id: str
    component_id: str
    required_skill_slug: str
    avg_replacement_cost: float
    salvage_resale_value: float
    harvest_liquidity_score: int


@dataclass
class Listing:
    id: str
    source: str
    external_id: str
    url: str
    title: str
    price: float
    shipping_cost: float
    condition: str
    image_urls: list[str]
    created_at: datetime
    projected_restorer_net: float
    projected_harvest_yield: float
    description: str | None = None
    listed_at: datetime | None = None
    matched_product_id: str | None = None
    detected_defective_bom_ids: list[str] = field(default_factory=list)
    required_repair_skills: list[str] = field(default_factory=list)


@dataclass
class UserDeal:
    id: str
    user_id: str
    listing_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    notes: str | None = None


@dataclass
class SavedSearch:
    id: str
    user_id: str
    name: str
    query: str
    filters: dict
    notify: bool
    created_at: datetime
