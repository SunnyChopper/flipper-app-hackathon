from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException

from app.domain.entities import CatalogProduct, Listing, UserDeal
from app.repositories.deal_repository import DealRepository
from app.repositories.listing_repository import ListingRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.profile_repository import ProfileRepository
from app.schemas.bom import DefectiveComponentResponse, RepairSkillSummaryResponse
from app.schemas.common import OpportunitySort
from app.schemas.opportunity import OpportunityDetailResponse, OpportunityListResponse, OpportunitySummaryResponse
from app.services.opportunity_mapper import (
    financials_for,
    to_listing_detail,
    to_market_comp,
    to_opportunity_summary,
    to_product_detail,
    to_user_deal_summary,
)
from app.services.scoring_service import score_opportunity
from app.services.valuation_service import roi_percent, total_replacement_cost


@dataclass
class OpportunityFilters:
    q: str | None = None
    source: str | None = None
    category: str | None = None
    condition: str | None = None
    persona: str | None = None
    min_profit: float | None = None
    min_roi: float | None = None
    max_price: float | None = None
    required_skill: str | None = None
    sort: OpportunitySort = OpportunitySort.score_desc
    page: int = 1
    page_size: int = 20


class OpportunityService:
    def __init__(
        self,
        listings: ListingRepository | None = None,
        products: ProductRepository | None = None,
        profiles: ProfileRepository | None = None,
        deals: DealRepository | None = None,
    ) -> None:
        self.listings = listings or ListingRepository()
        self.products = products or ProductRepository()
        self.profiles = profiles or ProfileRepository()
        self.deals = deals or DealRepository()

    def _repair_cost(self, listing: Listing) -> float:
        bom = self.products.bom_by_ids(listing.detected_defective_bom_ids)
        return total_replacement_cost(bom, listing.detected_defective_bom_ids)

    def _summary(
        self,
        listing: Listing,
        product: CatalogProduct | None,
        deal: UserDeal | None,
        persona: str | None,
    ) -> OpportunitySummaryResponse:
        return to_opportunity_summary(
            listing,
            product,
            deal,
            estimated_repair_cost=self._repair_cost(listing),
            persona=persona,
        )

    def list_opportunities(self, user_id: str, filters: OpportunityFilters) -> OpportunityListResponse:
        rows = self.listings.list_with_product_and_deal(user_id)
        needle = (filters.q or "").strip().lower()
        matched: list[tuple[Listing, CatalogProduct | None, UserDeal | None, OpportunitySummaryResponse]] = []

        for listing, product, deal in rows:
            summary = self._summary(listing, product, deal, filters.persona)
            if needle:
                haystack = " ".join(
                    [
                        listing.title,
                        listing.description or "",
                        product.brand if product else "",
                        product.model if product else "",
                        product.category if product else "",
                        product.variant if product and product.variant else "",
                    ]
                ).lower()
                if not _query_matches(haystack, needle):
                    continue
            if filters.source and listing.source != filters.source:
                continue
            if filters.category and filters.category != "all":
                if not product or product.category != filters.category:
                    continue
            if filters.condition and listing.condition != filters.condition:
                continue
            if filters.min_profit is not None and listing.projected_restorer_net < filters.min_profit:
                continue
            if filters.max_price is not None and listing.price > filters.max_price:
                continue
            if filters.required_skill and filters.required_skill not in listing.required_repair_skills:
                continue
            if filters.min_roi is not None:
                total_acq = listing.price + listing.shipping_cost + summary.estimated_repair_cost
                if roi_percent(listing.projected_restorer_net, total_acq) < filters.min_roi:
                    continue
            matched.append((listing, product, deal, summary))

        def sort_key(row: tuple[Listing, CatalogProduct | None, UserDeal | None, OpportunitySummaryResponse]):
            listing, _product, _deal, summary = row
            if filters.sort == OpportunitySort.profit_desc:
                return listing.projected_restorer_net
            if filters.sort == OpportunitySort.roi_desc:
                total_acq = listing.price + listing.shipping_cost + summary.estimated_repair_cost
                return roi_percent(listing.projected_restorer_net, total_acq)
            if filters.sort == OpportunitySort.price_asc:
                return -listing.price
            if filters.sort == OpportunitySort.newest:
                listed = listing.listed_at or listing.created_at
                return listed.timestamp()
            return float(summary.deal_score)

        matched.sort(key=sort_key, reverse=True)
        total = len(matched)
        start = (filters.page - 1) * filters.page_size
        page_rows = matched[start : start + filters.page_size]
        return OpportunityListResponse(
            items=[row[3] for row in page_rows],
            page=filters.page,
            page_size=filters.page_size,
            total=total,
        )

    def get_opportunity(self, user_id: str, listing_id: str) -> OpportunityDetailResponse:
        listing = self.listings.get(listing_id)
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")

        product = self.products.get(listing.matched_product_id)
        deal = self.deals.get(user_id, listing_id)
        product_bom = self.products.bom_for_product(product.id) if product else []
        financials = financials_for(listing, product, product_bom)
        score = score_opportunity(
            projected_restorer_net=financials.projected_restorer_net,
            total_acquisition_and_repair_cost=financials.total_acquisition_and_repair_cost,
            projected_harvest_yield=financials.projected_harvest_yield,
            product=product,
        )
        user_slugs = self.profiles.user_skill_slugs(user_id)

        defects: list[DefectiveComponentResponse] = []
        for bom_id in listing.detected_defective_bom_ids:
            bom_item = next((item for item in product_bom if item.id == bom_id), None)
            if not bom_item:
                continue
            component = self.products.component(bom_item.component_id)
            skill = self.products.skill(bom_item.required_skill_slug)
            defects.append(
                DefectiveComponentResponse(
                    bom_item_id=bom_item.id,
                    component_id=bom_item.component_id,
                    component_name=component.name if component else "Unknown component",
                    required_skill_slug=bom_item.required_skill_slug,
                    required_skill_display_name=skill.display_name if skill else bom_item.required_skill_slug,
                    avg_replacement_cost=bom_item.avg_replacement_cost,
                    salvage_resale_value=bom_item.salvage_resale_value,
                    harvest_liquidity_score=bom_item.harvest_liquidity_score,
                )
            )

        required_skills: list[RepairSkillSummaryResponse] = []
        for slug in listing.required_repair_skills:
            skill = self.products.skill(slug)
            if not skill:
                continue
            required_skills.append(
                RepairSkillSummaryResponse(
                    slug=skill.slug,
                    display_name=skill.display_name,
                    category=skill.category,
                    user_has_skill=slug in user_slugs,
                )
            )

        comps = self.products.comps_for_product(product.id) if product else []
        return OpportunityDetailResponse(
            listing=to_listing_detail(listing),
            product=to_product_detail(product) if product else None,
            defects=defects,
            required_skills=required_skills,
            market_comps=[to_market_comp(comp) for comp in comps],
            financials=financials,
            deal_score=score,
            user_deal=to_user_deal_summary(deal) if deal else None,
        )

    def summary_for_listing(self, user_id: str, listing_id: str) -> OpportunitySummaryResponse | None:
        listing = self.listings.get(listing_id)
        if not listing:
            return None
        product = self.products.get(listing.matched_product_id)
        deal = self.deals.get(user_id, listing_id)
        return self._summary(listing, product, deal, None)


opportunity_service = OpportunityService()

QUERY_ALIASES = {
    "tvs": "tv",
    "television": "tv",
    "televisions": "tv",
}


def _query_matches(haystack: str, needle: str) -> bool:
    if needle in haystack:
        return True
    tokens = [QUERY_ALIASES.get(part, part) for part in needle.split() if part]
    return bool(tokens) and all(token in haystack for token in tokens)
