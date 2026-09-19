import asyncio

from app.config import settings
from app.main import app
from app.models.ingest import IngestRequest
from app.models.listing import Listing
from app.repositories.memory_store import memory_store
from app.services.crawler import CATEGORY_QUERIES, CrawlScheduler, crawl_scheduler
from app.services.ebay import ebay_client
from app.services.ingest import ingest_pipeline
from fastapi.testclient import TestClient


def test_planned_categories_cover_requested_buckets(monkeypatch):
    monkeypatch.setattr(settings, "crawl_categories", "phones,tvs,electronics,other")
    scheduler = CrawlScheduler()
    assert scheduler.planned_categories() == ["phones", "tvs", "electronics", "other"]
    queries = [query for _category, query in scheduler.planned_queries()]
    assert "iphone cracked" in queries
    assert "tv for parts" in queries
    assert "laptop for parts" in queries
    assert "power tools for parts" in queries
    assert set(CATEGORY_QUERIES) == {"phones", "tvs", "electronics", "other"}


def test_tick_rotates_one_category_at_a_time():
    first = asyncio.run(crawl_scheduler.tick())
    second = asyncio.run(crawl_scheduler.tick())
    assert {item.category for item in first} == {"phones"}
    assert {item.category for item in second} == {"tvs"}
    assert all(item.error is None for item in first + second)
    assert sum(item.inserted for item in first) >= 1


def test_persist_skips_duplicate_source_and_url():
    request = IngestRequest(query="iphone", sources=["ebay"], limit=2)
    first = asyncio.run(ingest_pipeline.persist(request))
    count_after_first = len(memory_store.listings)
    second = asyncio.run(ingest_pipeline.persist(request))

    assert first.inserted
    assert not first.skipped
    assert not first.rejected
    assert not second.inserted
    assert len(second.skipped) == len(first.inserted)
    assert len(memory_store.listings) == count_after_first


def test_persist_rejects_working_listings(monkeypatch):
    async def fake_search(query: str, limit: int = 8) -> list[Listing]:
        return [
            Listing(
                id="good",
                source="ebay",
                external_id="working-iphone",
                title="iPhone 13 unlocked like new",
                description="Works perfectly. Excellent condition.",
                price=300,
                url="https://www.ebay.com/itm/working-iphone",
                condition_label="Used",
            ),
            Listing(
                id="bad",
                source="ebay",
                external_id="broken-iphone",
                title="iPhone 13 cracked screen",
                description="Does not work. Sold for parts.",
                price=80,
                url="https://www.ebay.com/itm/broken-iphone",
                condition_label="For parts or not working",
            ),
        ]

    monkeypatch.setattr(ebay_client, "search", fake_search)
    result = asyncio.run(ingest_pipeline.persist(IngestRequest(query="iphone", sources=["ebay"])))
    assert [row.external_id for row in result.rejected] == ["working-iphone"]
    assert len(result.inserted) == 1
    assert result.inserted[0].external_id == "broken-iphone"


def test_health_reports_crawl_status():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    body = response.json()
    assert "crawl" in body
    assert body["crawl"]["intervalSeconds"] == settings.crawl_interval_seconds
    assert set(body["crawl"]) >= {
        "enabled",
        "intervalSeconds",
        "running",
        "lastCategory",
        "lastInserted",
        "lastSkipped",
        "lastRejected",
        "nextCategory",
    }
