from __future__ import annotations

import asyncio
import logging

from app.config import settings
from app.data.ids import DEMO_USER_ID
from app.models.ingest import IngestRequest
from app.models.listing import Listing as ScrapedListing
from app.repositories.memory_store import memory_store
from app.repositories.product_repository import ProductRepository
from app.schemas.opportunity import OpportunityListResponse
from app.services.apify import facebook_marketplace
from app.services.catalog_match import to_domain_listing
from app.services.ebay import ebay_client
from app.services.opportunity_service import opportunity_service

logger = logging.getLogger(__name__)


class IngestPipeline:
    """Apify listings → catalog match + valuation → memory store → Opportunity DTOs."""

    def __init__(self) -> None:
        self.products = ProductRepository()

    async def collect(self, request: IngestRequest) -> list[ScrapedListing]:
        limit = min(request.limit, max(1, settings.apify_max_items))
        allowed = {_normalize_source(source) for source in settings.ingest_source_list}
        requested = {_normalize_source(source) for source in request.sources}
        sources = requested & allowed if allowed else requested
        if not sources:
            sources = allowed

        jobs: list[tuple[str, asyncio.Task[list[ScrapedListing]]]] = []
        if "ebay" in sources:
            jobs.append(
                (
                    "ebay",
                    asyncio.create_task(ebay_client.search(request.query, limit=limit)),
                )
            )
        if "facebook" in sources:
            jobs.append(
                (
                    "facebook",
                    asyncio.create_task(
                        facebook_marketplace.search(
                            request.query,
                            location=request.location,
                            limit=limit,
                        )
                    ),
                )
            )

        listings: list[ScrapedListing] = []
        errors: list[str] = []
        for source, task in jobs:
            try:
                listings.extend(await task)
            except Exception as exc:
                logger.exception("Ingest collect failed for %s", source)
                errors.append(f"{source}: {exc}")
        if not listings and errors:
            raise RuntimeError("; ".join(errors))
        return listings

    async def run(self, request: IngestRequest, user_id: str | None = None) -> OpportunityListResponse:
        scraped = await self.collect(request)
        owner = user_id or DEMO_USER_ID
        items = []
        for row in scraped:
            domain = to_domain_listing(row, self.products)
            stored = memory_store.upsert_listing(domain)
            summary = opportunity_service.summary_for_listing(owner, stored.id)
            if summary:
                items.append(summary)
        return OpportunityListResponse(items=items, page=1, page_size=len(items), total=len(items))


def _normalize_source(source: str) -> str:
    if source == "facebook_marketplace":
        return "facebook"
    return source


ingest_pipeline = IngestPipeline()
