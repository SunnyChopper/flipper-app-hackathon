from __future__ import annotations

from datetime import datetime

from app.domain.entities import (
    CatalogProduct,
    Component,
    Listing,
    ProductBOMItem,
    ProductMarketComp,
    Profile,
    RepairSkill,
    SavedSearch,
    UserDeal,
)


def as_float(value: object, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    return float(value)


def as_str_list(value: object) -> list[str]:
    if not value:
        return []
    return [str(item) for item in value]  # type: ignore[union-attr]


def as_datetime(value: object) -> datetime | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def listing_from_row(row: dict) -> Listing:
    created_at = as_datetime(row.get("created_at"))
    if created_at is None:
        raise ValueError("listing created_at is required")
    return Listing(
        id=str(row["id"]),
        source=str(row["source"]),
        external_id=str(row["external_id"]),
        url=str(row["url"]),
        title=str(row["title"]),
        price=as_float(row.get("price")),
        shipping_cost=as_float(row.get("shipping_cost")),
        condition=str(row.get("condition") or "used_fair"),
        image_urls=as_str_list(row.get("image_urls")),
        created_at=created_at,
        projected_restorer_net=as_float(row.get("projected_restorer_net")),
        projected_harvest_yield=as_float(row.get("projected_harvest_yield")),
        description=str(row["description"]) if row.get("description") is not None else None,
        listed_at=as_datetime(row.get("listed_at")),
        matched_product_id=str(row["matched_product_id"]) if row.get("matched_product_id") else None,
        detected_defective_bom_ids=as_str_list(row.get("detected_defective_bom_ids")),
        required_repair_skills=as_str_list(row.get("required_repair_skills")),
    )


def catalog_product_from_row(row: dict) -> CatalogProduct:
    return CatalogProduct(
        id=str(row["id"]),
        brand=str(row["brand"]),
        model=str(row["model"]),
        variant=str(row["variant"]) if row.get("variant") else None,
        category=str(row["category"]),
        estimated_working_market_value=as_float(row.get("estimated_working_market_value")),
        valuation_confidence_score=as_float(row.get("valuation_confidence_score")),
        last_valuation_at=as_datetime(row.get("last_valuation_at")),
    )


def user_deal_from_row(row: dict) -> UserDeal:
    created_at = as_datetime(row.get("created_at"))
    updated_at = as_datetime(row.get("updated_at"))
    if created_at is None or updated_at is None:
        raise ValueError("user deal timestamps are required")
    return UserDeal(
        id=str(row["id"]),
        user_id=str(row["user_id"]),
        listing_id=str(row["listing_id"]),
        status=str(row["status"]),
        created_at=created_at,
        updated_at=updated_at,
        notes=str(row["notes"]) if row.get("notes") is not None else None,
    )


def repair_skill_from_row(row: dict) -> RepairSkill:
    return RepairSkill(
        slug=str(row["slug"]),
        display_name=str(row["display_name"]),
        category=str(row["category"]),
    )


def profile_from_row(row: dict) -> Profile:
    return Profile(
        id=str(row["id"]),
        persona=str(row.get("persona") or "restorer"),
        min_profit_margin_usd=as_float(row.get("min_profit_margin_usd"), 100),
        min_roi_percent=as_float(row.get("min_roi_percent"), 20),
    )


def bom_item_from_row(row: dict) -> ProductBOMItem:
    return ProductBOMItem(
        id=str(row["id"]),
        product_id=str(row["product_id"]),
        component_id=str(row["component_id"]),
        required_skill_slug=str(row["required_skill_slug"]),
        avg_replacement_cost=as_float(row.get("avg_replacement_cost")),
        salvage_resale_value=as_float(row.get("salvage_resale_value")),
        harvest_liquidity_score=int(as_float(row.get("harvest_liquidity_score"), 1)),
    )


def component_from_row(row: dict) -> Component:
    return Component(id=str(row["id"]), name=str(row["name"]))


def market_comp_from_row(row: dict) -> ProductMarketComp:
    sold_date = row.get("sold_date")
    if hasattr(sold_date, "isoformat"):
        sold_date = sold_date.isoformat()
    return ProductMarketComp(
        id=str(row["id"]),
        product_id=str(row["product_id"]),
        source=str(row["source"]),
        sold_price=as_float(row.get("sold_price")),
        shipping_price=as_float(row.get("shipping_price")),
        item_condition=str(row["item_condition"]),
        sold_date=str(sold_date),
        listing_url=str(row["listing_url"]),
    )


def saved_search_from_row(row: dict) -> SavedSearch:
    created_at = as_datetime(row.get("created_at"))
    if created_at is None:
        raise ValueError("saved search created_at is required")
    filters = row.get("filters") or {}
    if not isinstance(filters, dict):
        filters = {}
    return SavedSearch(
        id=str(row["id"]),
        user_id=str(row["user_id"]),
        name=str(row["name"]),
        query=str(row.get("query") or ""),
        filters=filters,
        notify=bool(row.get("notify", True)),
        created_at=created_at,
    )
