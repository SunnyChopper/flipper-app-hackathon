import pytest
from fastapi.testclient import TestClient

from app.auth import _profiles
from app.config import settings
from app.main import app
from app.repositories.memory_store import memory_store
from app.services.apify import apify_client
from app.services.crawler import crawl_scheduler
from app.services.deal_service import deal_service
from app.services.ingest import ingest_pipeline
from app.services.opportunity_service import opportunity_service
from app.services.profile_service import profile_service


def _use_memory() -> None:
    opportunity_service.listings.client = None
    opportunity_service.products.client = None
    opportunity_service.profiles.client = None
    opportunity_service.deals.client = None
    deal_service.deals.client = None
    deal_service.listings.client = None
    profile_service.profiles.client = None
    ingest_pipeline.listings.client = None
    _profiles.client = None


@pytest.fixture(autouse=True)
def reset_store(monkeypatch):
    monkeypatch.setattr(settings, "supabase_url", "")
    monkeypatch.setattr(settings, "supabase_service_role_key", "")
    monkeypatch.setattr(settings, "apify_token", "")
    monkeypatch.setattr(settings, "crawl_enabled", False)
    monkeypatch.setattr(apify_client, "token", "")
    crawl_scheduler._cursor = 0
    crawl_scheduler.status.last_error = None
    _use_memory()
    memory_store.reset()
    yield
    memory_store.reset()
    _use_memory()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
