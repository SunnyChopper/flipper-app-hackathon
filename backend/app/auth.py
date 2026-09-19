from __future__ import annotations

from typing import Annotated

import httpx
from fastapi import Header, HTTPException, status

from app.config import settings
from app.repositories.memory_store import DEMO_USER
from app.repositories.profile_repository import ProfileRepository

_profiles = ProfileRepository()


def _bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, value = authorization.partition(" ")
    if scheme.lower() != "bearer" or not value.strip():
        return None
    return value.strip()


def _user_id_from_supabase(token: str) -> str:
    url = settings.supabase_url.rstrip("/") + "/auth/v1/user"
    headers = {
        "Authorization": f"Bearer {token}",
        "apikey": settings.supabase_service_role_key,
    }
    try:
        response = httpx.get(url, headers=headers, timeout=8.0)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not verify session",
        ) from exc
    if response.status_code >= 400:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    user_id = response.json().get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    return str(user_id)


def get_current_user_id(
    authorization: Annotated[str | None, Header()] = None,
) -> str:
    token = _bearer_token(authorization)
    if not token or not settings.supabase_enabled:
        return DEMO_USER
    user_id = _user_id_from_supabase(token)
    _profiles.ensure_profile(user_id)
    return user_id
