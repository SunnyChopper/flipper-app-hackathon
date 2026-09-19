from __future__ import annotations

import logging
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)
_schema_ready: bool | None = None  # reset on reload after migrations


def get_supabase_client(url: str | None = None, key: str | None = None) -> Any:
    global _schema_ready
    if _schema_ready is False:
        return None
    resolved_url = settings.supabase_url if url is None else url
    resolved_key = settings.supabase_service_role_key if key is None else key
    if not resolved_url or not resolved_key:
        return None
    from supabase import create_client

    client = create_client(resolved_url, resolved_key)
    if url is None and key is None and _schema_ready is None:
        if not _has_core_tables(client):
            logger.warning("Supabase is missing core tables; using the in-memory store for local demo")
            _schema_ready = False
            return None
        _schema_ready = True
    return client


def _has_core_tables(client: Any) -> bool:
    try:
        client.table("listings").select("id").limit(1).execute()
    except Exception as exc:
        if _is_missing_schema(exc):
            return False
        raise
    return True


def _is_missing_schema(exc: Exception) -> bool:
    text = str(exc)
    return "PGRST205" in text or "schema cache" in text.lower()
