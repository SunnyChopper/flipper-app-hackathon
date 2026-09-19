from __future__ import annotations

from fastapi import HTTPException

from app.repositories.deal_repository import DealRepository
from app.repositories.listing_repository import ListingRepository
from app.schemas.deal import SaveDealRequest, SavedDealItemResponse, SavedDealListResponse, UserDealResponse
from app.services.opportunity_mapper import to_user_deal_summary
from app.services.opportunity_service import OpportunityService, opportunity_service


class DealService:
    def __init__(
        self,
        deals: DealRepository | None = None,
        listings: ListingRepository | None = None,
        opportunities: OpportunityService | None = None,
    ) -> None:
        self.deals = deals or DealRepository()
        self.listings = listings or ListingRepository()
        self.opportunities = opportunities or opportunity_service

    def list_deals(self, user_id: str, status: str | None = None) -> SavedDealListResponse:
        items: list[SavedDealItemResponse] = []
        for deal in self.deals.list_for_user(user_id, status=status):
            summary = self.opportunities.summary_for_listing(user_id, deal.listing_id)
            if not summary:
                continue
            items.append(
                SavedDealItemResponse(
                    user_deal=to_user_deal_summary(deal),
                    opportunity=summary,
                )
            )
        return SavedDealListResponse(items=items)

    def upsert_deal(self, user_id: str, listing_id: str, payload: SaveDealRequest) -> UserDealResponse:
        if not self.listings.get(listing_id):
            raise HTTPException(status_code=404, detail="Listing not found")
        deal = self.deals.upsert(user_id, listing_id, payload.status, payload.notes)
        return UserDealResponse(
            id=deal.id,
            listing_id=deal.listing_id,
            status=deal.status,  # type: ignore[arg-type]
            notes=deal.notes,
            created_at=deal.created_at,
            updated_at=deal.updated_at,
        )

    def delete_deal(self, user_id: str, listing_id: str) -> None:
        deleted = self.deals.delete(user_id, listing_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Saved deal not found")


deal_service = DealService()
