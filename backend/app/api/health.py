from fastapi import APIRouter

from app.config import settings
from app.services.crawler import crawl_scheduler

router = APIRouter(tags=["health"])


@router.get("/")
def root() -> dict[str, str]:
    return {
        "service": "deal-sniper-api",
        "docs": "/docs",
        "health": "/health",
    }


@router.get("/health")
def health() -> dict[str, object]:
    status = crawl_scheduler.status
    return {
        "status": "ok",
        "service": "deal-sniper-api",
        "supabase": settings.supabase_enabled,
        "ebay": bool(settings.apify_token),
        "apify": bool(settings.apify_token),
        "llm": bool(settings.openai_api_key),
        "crawl": {
            "enabled": status.enabled,
            "intervalSeconds": status.interval_seconds,
            "running": status.running,
            "lastCategory": status.last_category,
            "lastQuery": status.last_query,
            "lastInserted": status.last_inserted,
            "lastSkipped": status.last_skipped,
            "lastRejected": status.last_rejected,
            "lastError": status.last_error,
            "lastRunAt": status.last_run_at,
            "nextCategory": status.next_category,
        },
    }
