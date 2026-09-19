from __future__ import annotations

from app.domain.entities import CatalogProduct, ProductBOMItem


def product_display_name(product: CatalogProduct) -> str:
    parts = [product.brand, product.model]
    if product.variant:
        parts.append(product.variant)
    return " ".join(parts)


def total_replacement_cost(
    bom_items: list[ProductBOMItem],
    defective_bom_ids: list[str],
) -> float:
    defective = set(defective_bom_ids)
    return round(sum(item.avg_replacement_cost for item in bom_items if item.id in defective), 2)


def intact_salvage_value(
    bom_items: list[ProductBOMItem],
    defective_bom_ids: list[str],
) -> float:
    defective = set(defective_bom_ids)
    return round(sum(item.salvage_resale_value for item in bom_items if item.id not in defective), 2)


def projected_restorer_net(
    working_market_value: float,
    price: float,
    shipping_cost: float,
    replacement_cost: float,
) -> float:
    return round(working_market_value - price - shipping_cost - replacement_cost, 2)


def projected_harvest_yield(
    salvage_value: float,
    price: float,
    shipping_cost: float,
) -> float:
    return round(salvage_value - price - shipping_cost, 2)


def roi_percent(restorer_net: float, total_acquisition_and_repair_cost: float) -> float:
    if total_acquisition_and_repair_cost <= 0:
        return 0.0
    return round((restorer_net / total_acquisition_and_repair_cost) * 100, 1)


def listing_economics(
    *,
    working_market_value: float,
    price: float,
    shipping_cost: float,
    bom_items: list[ProductBOMItem],
    defective_bom_ids: list[str],
) -> tuple[float, float, float]:
    replacement = total_replacement_cost(bom_items, defective_bom_ids)
    restorer = projected_restorer_net(working_market_value, price, shipping_cost, replacement)
    harvest = projected_harvest_yield(
        intact_salvage_value(bom_items, defective_bom_ids),
        price,
        shipping_cost,
    )
    return replacement, restorer, harvest
