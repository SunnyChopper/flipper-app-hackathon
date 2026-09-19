from __future__ import annotations

from app.domain.entities import (
    CatalogProduct,
    Component,
    ProductBOMItem,
    ProductMarketComp,
    RepairSkill,
)
from app.repositories.mappers import (
    bom_item_from_row,
    catalog_product_from_row,
    component_from_row,
    market_comp_from_row,
    repair_skill_from_row,
)
from app.repositories.memory_store import MemoryStore, memory_store
from app.services.supabase_client import get_supabase_client


class ProductRepository:
    def __init__(self, store: MemoryStore | None = None, client=None) -> None:
        self.store = store or memory_store
        self._client = client
        self._client_bound = client is not None
        self._bom_cache: list[ProductBOMItem] | None = None

    @property
    def client(self):
        if not self._client_bound:
            self._client = get_supabase_client()
            self._client_bound = True
        return self._client

    @client.setter
    def client(self, value) -> None:
        self._client = value
        self._client_bound = True
        self._bom_cache = None

    def get(self, product_id: str | None) -> CatalogProduct | None:
        if not product_id:
            return None
        if self.client:
            rows = self._select("catalog_products", id=product_id)
            return catalog_product_from_row(rows[0]) if rows else None
        return self.store.products.get(product_id)

    def bom_for_product(self, product_id: str) -> list[ProductBOMItem]:
        if self.client:
            return [item for item in self._all_bom_items() if item.product_id == product_id]
        return [item for item in self.store.bom_items.values() if item.product_id == product_id]

    def bom_by_ids(self, bom_ids: list[str]) -> list[ProductBOMItem]:
        if not bom_ids:
            return []
        wanted = set(bom_ids)
        if self.client:
            return [item for item in self._all_bom_items() if item.id in wanted]
        return [self.store.bom_items[bom_id] for bom_id in bom_ids if bom_id in self.store.bom_items]

    def _all_bom_items(self) -> list[ProductBOMItem]:
        if self._bom_cache is None:
            self._bom_cache = [bom_item_from_row(row) for row in self._select("product_bom_items")]
        return self._bom_cache

    def component(self, component_id: str) -> Component | None:
        if self.client:
            rows = self._select("components", id=component_id)
            return component_from_row(rows[0]) if rows else None
        return self.store.components.get(component_id)

    def comps_for_product(self, product_id: str) -> list[ProductMarketComp]:
        if self.client:
            return [market_comp_from_row(row) for row in self._select("product_market_comps", product_id=product_id)]
        return [comp for comp in self.store.market_comps.values() if comp.product_id == product_id]

    def skill(self, slug: str) -> RepairSkill | None:
        if self.client:
            rows = self._select("repair_skills", slug=slug)
            return repair_skill_from_row(rows[0]) if rows else None
        return self.store.repair_skills.get(slug)

    def all_skills(self) -> list[RepairSkill]:
        if self.client:
            return [repair_skill_from_row(row) for row in self._select("repair_skills")]
        return list(self.store.repair_skills.values())

    def _select(self, table: str, **eq: str) -> list[dict]:
        query = self.client.table(table).select("*")
        for column, value in eq.items():
            query = query.eq(column, value)
        result = query.execute()
        return list(result.data or [])
