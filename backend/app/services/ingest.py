from __future__ import annotations

import asyncio
import logging

from app.models.deal import Deal
from app.models.ingest import IngestRequest
from app.models.listing import Listing
from app.services.apify import facebook_marketplace
from app.services.ebay import ebay_client
from app.services.store import deal_store

logger = logging.getLogger(__name__)


class IngestPipeline:
    """listing (Apify eBay + Facebook) → analyzer.normalize → deal_scorer.score → store."""

    async def collect(self, request: IngestRequest) -> list[Listing]:
        jobs: list[tuple[str, asyncio.Task[list[Listing]]]] = []
        if "ebay" in request.sources:
            jobs.append(
                (
                    "ebay",
                    asyncio.create_task(ebay_client.search(request.query, limit=request.limit)),
                )
            )
        if "facebook" in request.sources:
            jobs.append(
                (
                    "facebook",
                    asyncio.create_task(
                        facebook_marketplace.search(
                            request.query,
                            location=request.location,
                            limit=request.limit,
                        )
                    ),
                )
            )

        listings: list[Listing] = []
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

    async def run(self, request: IngestRequest) -> list[Deal]:
        listings = await self.collect(request)
        deals: list[Deal] = []
        for listing in listings:
            deals.append(await deal_store.ingest(listing))
        return deals


ingest_pipeline = IngestPipeline()
