from __future__ import annotations

from typing import Any

from app.config import settings


def get_supabase_client(url: str | None = None, key: str | None = None) -> Any:
    resolved_url = settings.supabase_url if url is None else url
    resolved_key = settings.supabase_service_role_key if key is None else key
    if not resolved_url or not resolved_key:
        return None
    from supabase import create_client

    return create_client(resolved_url, resolved_key)
