from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from app.config import settings
from app.models.ingest import IngestRequest
from app.services.ingest import ingest_pipeline

logger = logging.getLogger(__name__)

CATEGORY_QUERIES: dict[str, list[str]] = {
    "phones": ["iphone cracked", "iphone for parts", "samsung phone not working"],
    "tvs": ["tv for parts", "tv no picture"],
    "electronics": ["laptop cracked screen", "laptop for parts", "headphones broken"],
    "other": ["dyson not working", "kitchenaid broken", "power tools for parts"],
}


@dataclass
class CrawlTickResult:
    category: str
    query: str
    inserted: int = 0
    skipped: int = 0
    rejected: int = 0
    error: str | None = None


@dataclass
class CrawlStatus:
    enabled: bool = False
    interval_seconds: int = 60
    running: bool = False
    last_category: str | None = None
    last_query: str | None = None
    last_inserted: int = 0
    last_skipped: int = 0
    last_rejected: int = 0
    last_error: str | None = None
    last_run_at: str | None = None
    next_category: str | None = None


class CrawlScheduler:
    """Rotate category searches every minute and persist only new listings."""

    def __init__(self) -> None:
        self._task: asyncio.Task[None] | None = None
        self._stop = asyncio.Event()
        self._tick_lock = asyncio.Lock()
        self._cursor = 0
        self.status = CrawlStatus()

    def planned_queries(self) -> list[tuple[str, str]]:
        return [(category, query) for category in self.planned_categories() for query in CATEGORY_QUERIES[category]]

    def planned_categories(self) -> list[str]:
        wanted = [part.strip() for part in settings.crawl_categories.split(",") if part.strip()]
        return [name for name in wanted if name in CATEGORY_QUERIES] or list(CATEGORY_QUERIES)

    async def start(self) -> None:
        self.status.enabled = settings.crawl_enabled
        self.status.interval_seconds = settings.crawl_interval_seconds
        categories = self.planned_categories()
        self.status.next_category = categories[0] if categories else None
        if not settings.crawl_enabled:
            logger.info("Marketplace crawler disabled")
            return
        if self._task and not self._task.done():
            return
        self._stop = asyncio.Event()
        self._task = asyncio.create_task(self._loop(), name="marketplace-crawler")
        logger.info(
            "Marketplace crawler started (every %ss, categories=%s)",
            settings.crawl_interval_seconds,
            settings.crawl_categories,
        )

    async def stop(self) -> None:
        self._stop.set()
        task = self._task
        self._task = None
        if task:
            await task

    async def _loop(self) -> None:
        await self.tick()
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=max(1, settings.crawl_interval_seconds))
                break
            except TimeoutError:
                await self.tick()

    async def tick(self) -> list[CrawlTickResult]:
        if self._tick_lock.locked():
            logger.info("Skipping crawl tick; previous category run is still in progress")
            return []
        async with self._tick_lock:
            return await self._run_category_tick()

    async def _run_category_tick(self) -> list[CrawlTickResult]:
        categories = self.planned_categories()
        if not categories:
            return []
        category = categories[self._cursor % len(categories)]
        self._cursor += 1
        queries = [(category, query) for query in CATEGORY_QUERIES[category]]

        self.status.running = True
        self.status.last_error = None
        results: list[CrawlTickResult] = []
        try:
            for name, query in queries:
                result = await self._ingest_query(name, query)
                results.append(result)
        finally:
            inserted = sum(item.inserted for item in results)
            skipped = sum(item.skipped for item in results)
            rejected = sum(item.rejected for item in results)
            error = next((item.error for item in results if item.error), None)
            self.status.running = False
            self.status.last_category = category
            self.status.last_query = ", ".join(query for _name, query in queries)
            self.status.last_inserted = inserted
            self.status.last_skipped = skipped
            self.status.last_rejected = rejected
            self.status.last_error = error
            self.status.last_run_at = datetime.now(UTC).isoformat()
            remaining = self.planned_categories()
            self.status.next_category = remaining[self._cursor % len(remaining)] if remaining else None
            logger.info(
                "Crawl tick finished category=%s inserted=%s skipped=%s rejected=%s error=%s",
                category,
                inserted,
                skipped,
                rejected,
                error,
            )
        return results

    async def _ingest_query(self, category: str, query: str) -> CrawlTickResult:
        request = IngestRequest(query=query, limit=settings.apify_max_items)
        try:
            persisted = await ingest_pipeline.persist(request)
        except Exception as exc:
            logger.exception("Crawl query failed category=%s query=%s", category, query)
            return CrawlTickResult(category=category, query=query, error=str(exc))
        return CrawlTickResult(
            category=category,
            query=query,
            inserted=len(persisted.inserted),
            skipped=len(persisted.skipped),
            rejected=len(persisted.rejected),
        )


crawl_scheduler = CrawlScheduler()
