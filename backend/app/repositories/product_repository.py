from __future__ import annotations

from app.domain.entities import (
    CatalogProduct,
    Component,
    ProductBOMItem,
    ProductMarketComp,
    RepairSkill,
)
from app.repositories.memory_store import MemoryStore, memory_store


class ProductRepository:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or memory_store

    def get(self, product_id: str | None) -> CatalogProduct | None:
        if not product_id:
            return None
        return self.store.products.get(product_id)

    def bom_for_product(self, product_id: str) -> list[ProductBOMItem]:
        return [item for item in self.store.bom_items.values() if item.product_id == product_id]

    def bom_by_ids(self, bom_ids: list[str]) -> list[ProductBOMItem]:
        return [self.store.bom_items[bom_id] for bom_id in bom_ids if bom_id in self.store.bom_items]

    def component(self, component_id: str) -> Component | None:
        return self.store.components.get(component_id)

    def comps_for_product(self, product_id: str) -> list[ProductMarketComp]:
        return [comp for comp in self.store.market_comps.values() if comp.product_id == product_id]

    def skill(self, slug: str) -> RepairSkill | None:
        return self.store.repair_skills.get(slug)

    def all_skills(self) -> list[RepairSkill]:
        return list(self.store.repair_skills.values())
