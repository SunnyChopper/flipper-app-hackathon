from __future__ import annotations

from app.domain.entities import CatalogProduct, Listing, ProductBOMItem, ProductMarketComp, UserDeal
from app.schemas.bom import DefectiveComponentResponse, RepairSkillSummaryResponse
from app.schemas.catalog_product import CatalogProductDetailResponse, CatalogProductSummaryResponse
from app.schemas.listing import ListingDetailResponse
from app.schemas.market_comp import MarketCompSummaryResponse
from app.schemas.opportunity import (
    OpportunityFinancialsResponse,
    OpportunitySummaryResponse,
    UserDealSummaryResponse,
)
from app.services.scoring_service import score_opportunity
from app.services.valuation_service import (
    listing_economics,
    product_display_name,
    roi_percent,
)


def to_product_summary(product: CatalogProduct) -> CatalogProductSummaryResponse:
    return CatalogProductSummaryResponse(
        id=product.id,
        brand=product.brand,
        model=product.model,
        variant=product.variant,
        category=product.category,
        display_name=product_display_name(product),
        estimated_working_market_value=product.estimated_working_market_value,
        valuation_confidence_score=product.valuation_confidence_score,
    )


def to_product_detail(product: CatalogProduct) -> CatalogProductDetailResponse:
    return CatalogProductDetailResponse(
        **to_product_summary(product).model_dump(),
        last_valuation_at=product.last_valuation_at,
    )


def to_listing_detail(listing: Listing) -> ListingDetailResponse:
    return ListingDetailResponse(
        id=listing.id,
        source=listing.source,  # type: ignore[arg-type]
        external_id=listing.external_id,
        url=listing.url,
        title=listing.title,
        description=listing.description,
        price=listing.price,
        shipping_cost=listing.shipping_cost,
        condition=listing.condition,
        image_urls=listing.image_urls,
        listed_at=listing.listed_at,
        created_at=listing.created_at,
        projected_restorer_net=listing.projected_restorer_net,
        projected_harvest_yield=listing.projected_harvest_yield,
    )


def to_market_comp(comp: ProductMarketComp) -> MarketCompSummaryResponse:
    return MarketCompSummaryResponse(
        id=comp.id,
        source=comp.source,
        sold_price=comp.sold_price,
        shipping_price=comp.shipping_price,
        total_price=round(comp.sold_price + comp.shipping_price, 2),
        item_condition=comp.item_condition,
        sold_date=comp.sold_date,
        listing_url=comp.listing_url,
    )


def to_user_deal_summary(deal: UserDeal) -> UserDealSummaryResponse:
    return UserDealSummaryResponse(
        id=deal.id,
        listing_id=deal.listing_id,
        status=deal.status,  # type: ignore[arg-type]
        notes=deal.notes,
        created_at=deal.created_at,
        updated_at=deal.updated_at,
    )


def financials_for(
    listing: Listing,
    product: CatalogProduct | None,
    bom_items: list[ProductBOMItem],
) -> OpportunityFinancialsResponse:
    working = product.estimated_working_market_value if product else 0.0
    replacement, restorer, harvest = listing_economics(
        working_market_value=working,
        price=listing.price,
        shipping_cost=listing.shipping_cost,
        bom_items=bom_items,
        defective_bom_ids=listing.detected_defective_bom_ids,
    )
    total_acq = round(listing.price + listing.shipping_cost + replacement, 2)
    return OpportunityFinancialsResponse(
        purchase_price=listing.price,
        shipping_cost=listing.shipping_cost,
        total_replacement_cost=replacement,
        total_acquisition_and_repair_cost=total_acq,
        estimated_working_market_value=working,
        projected_restorer_net=restorer,
        projected_harvest_yield=harvest,
        roi_percent=roi_percent(restorer, total_acq),
    )


def to_opportunity_summary(
    listing: Listing,
    product: CatalogProduct | None,
    deal: UserDeal | None,
    estimated_repair_cost: float,
    persona: str | None = None,
) -> OpportunitySummaryResponse:
    total_acq = round(listing.price + listing.shipping_cost + estimated_repair_cost, 2)
    restorer = listing.projected_restorer_net
    score = score_opportunity(
        projected_restorer_net=restorer,
        total_acquisition_and_repair_cost=total_acq,
        projected_harvest_yield=listing.projected_harvest_yield,
        product=product,
        persona=persona,
    )
    return OpportunitySummaryResponse(
        listing_id=listing.id,
        source=listing.source,  # type: ignore[arg-type]
        title=listing.title,
        description=listing.description,
        url=listing.url,
        price=listing.price,
        shipping_cost=listing.shipping_cost,
        image_url=listing.image_urls[0] if listing.image_urls else None,
        condition=listing.condition,
        listed_at=listing.listed_at,
        product=to_product_summary(product) if product else None,
        required_repair_skills=list(listing.required_repair_skills),
        projected_restorer_net=restorer,
        projected_harvest_yield=listing.projected_harvest_yield,
        estimated_repair_cost=estimated_repair_cost,
        deal_score=score.total,
        user_deal_status=deal.status if deal else None,  # type: ignore[arg-type]
    )
