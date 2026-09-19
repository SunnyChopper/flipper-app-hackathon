from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": "deal-sniper-api",
        "supabase": settings.supabase_enabled,
        "ebay": bool(settings.ebay_app_id),
        "apify": bool(settings.apify_token),
        "llm": bool(settings.openai_api_key),
    }
