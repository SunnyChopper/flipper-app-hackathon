from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/")
def root() -> dict[str, str]:
    return {
        "service": "deal-sniper-api",
        "docs": "/docs",
        "health": "/health",
    }


@router.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": "deal-sniper-api",
        "supabase": settings.supabase_enabled,
        "ebay": bool(settings.apify_token),
        "apify": bool(settings.apify_token),
        "llm": bool(settings.openai_api_key),
    }
