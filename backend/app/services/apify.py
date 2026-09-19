from __future__ import annotations

import asyncio
import logging
from typing import Any
from urllib.parse import quote

import httpx

from app.config import settings
from app.models.listing import Listing
from app.models.sources import FacebookMarketplaceItem
from app.services.listing_mapper import listing_from_facebook

logger = logging.getLogger(__name__)

APIFY_BASE = "https://api.apify.com/v2"


class ApifyClient:
    """Run Apify actors and read dataset items. Used by marketplace adapters."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token if token is not None else settings.apify_token

    @property
    def enabled(self) -> bool:
        return bool(self.token)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def run_and_get_items(
        self,
        actor_id: str,
        run_input: dict[str, Any],
        timeout_seconds: int | None = None,
    ) -> list[dict[str, Any]]:
        timeout = timeout_seconds or settings.apify_run_timeout_seconds
        encoded_actor = quote(actor_id, safe="~")
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, read=60.0)) as client:
            start = await client.post(
                f"{APIFY_BASE}/acts/{encoded_actor}/runs",
                headers=self._headers(),
                params={"waitForFinish": min(55, timeout)},
                json=run_input,
            )
            if start.is_error:
                raise RuntimeError(f"Apify start failed ({start.status_code}): {start.text[:400]}")
            run = start.json().get("data") or {}
            run_id = run.get("id")
            if not run_id:
                raise RuntimeError("Apify run did not return an id")

            deadline = asyncio.get_event_loop().time() + timeout
            status = run.get("status", "RUNNING")
            dataset_id = run.get("defaultDatasetId")
            while status in {"READY", "RUNNING"}:
                if asyncio.get_event_loop().time() > deadline:
                    raise TimeoutError(f"Apify run {run_id} exceeded {timeout}s")
                await asyncio.sleep(3)
                poll = await client.get(
                    f"{APIFY_BASE}/actor-runs/{run_id}",
                    headers=self._headers(),
                )
                poll.raise_for_status()
                run = poll.json().get("data") or {}
                status = run.get("status", status)
                dataset_id = run.get("defaultDatasetId") or dataset_id

            if status != "SUCCEEDED":
                raise RuntimeError(f"Apify run {run_id} ended with status {status}")
            if not dataset_id:
                return []

            items = await client.get(
                f"{APIFY_BASE}/datasets/{dataset_id}/items",
                headers=self._headers(),
                params={"format": "json", "clean": "true"},
            )
            if items.is_error:
                raise RuntimeError(f"Apify dataset fetch failed ({items.status_code}): {items.text[:400]}")
            payload = items.json()
            return payload if isinstance(payload, list) else []


apify_client = ApifyClient()


class FacebookMarketplaceClient:
    """Collect Facebook Marketplace listings via Apify. Mocks until APIFY_TOKEN is set."""

    def __init__(self, client: ApifyClient | None = None) -> None:
        self.client = client or apify_client

    async def search(
        self,
        query: str,
        location: str = "united-states",
        limit: int = 8,
    ) -> list[Listing]:
        if not self.client.enabled:
            return self._mock_listings(query, location)

        slug = _marketplace_slug(location)
        encoded_query = quote(query or "vacuum")
        start_url = f"https://www.facebook.com/marketplace/{slug}/search/?query={encoded_query}"
        run_input = {
            "startUrls": [{"url": start_url}],
            "resultsLimit": limit,
            "includeListingDetails": True,
        }
        try:
            rows = await self.client.run_and_get_items(settings.apify_facebook_actor, run_input)
        except Exception:
            logger.exception("Apify Facebook Marketplace run failed")
            raise

        listings: list[Listing] = []
        for row in rows:
            try:
                item = FacebookMarketplaceItem.model_validate(row)
            except Exception:
                logger.debug("Skipping unreadable Facebook row", extra={"row_keys": list(row)})
                continue
            listing = listing_from_facebook(item)
            if listing:
                listings.append(listing)
        return listings[:limit]

    def _mock_listings(self, query: str, location: str) -> list[Listing]:
        title = query or "KitchenAid mixer, bowl dented, runs great"
        return [
            Listing(
                id="fb-mock-1",
                source="facebook",
                external_id="fb-mock-1",
                title=title if "kitchen" in title.lower() else f"{title} — local pickup",
                description="Seller wants gone today. Item powers on. Minor cosmetic wear.",
                price=65,
                url="https://www.facebook.com/marketplace/item/mock-kitchenaid",
                image_url="https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800",
                location=location,
                seller_name="Neighborhood seller",
                raw={"mock": True, "actor": settings.apify_facebook_actor},
            ),
            Listing(
                id="fb-mock-2",
                source="facebook",
                external_id="fb-mock-2",
                title=f"{query or 'DeWalt drill'} — missing charger, batteries included",
                description="Two packs take a charge. No charger in the box.",
                price=40,
                url="https://www.facebook.com/marketplace/item/mock-dewalt",
                image_url="https://images.unsplash.com/photo-1504148455328-c376907d081c?w=800",
                location=location,
                seller_name="Tool dump",
                raw={"mock": True, "actor": settings.apify_facebook_actor},
            ),
        ]


def _marketplace_slug(location: str) -> str:
    slug = location.strip().lower().replace("_", "-")
    slug = slug.replace(" ", "")
    return slug or "united-states"


facebook_marketplace = FacebookMarketplaceClient()
