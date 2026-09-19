from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from app.auth import get_current_user_id
from app.models.ingest import IngestRequest
from app.schemas.opportunity import OpportunityListResponse
from app.services.ingest import ingest_pipeline

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("", response_model=OpportunityListResponse)
async def ingest_marketplaces(
    user_id: Annotated[str, Depends(get_current_user_id)],
    payload: IngestRequest | None = Body(default=None),
) -> OpportunityListResponse:
    try:
        return await ingest_pipeline.run(payload or IngestRequest(), user_id=user_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/ebay", response_model=OpportunityListResponse)
async def ingest_ebay(
    user_id: Annotated[str, Depends(get_current_user_id)],
    query: str = Query(default="iphone 13"),
    limit: int = Query(default=8, ge=1, le=50),
) -> OpportunityListResponse:
    try:
        return await ingest_pipeline.run(
            IngestRequest(query=query, limit=limit, sources=["ebay"]),
            user_id=user_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/facebook", response_model=OpportunityListResponse)
async def ingest_facebook(
    user_id: Annotated[str, Depends(get_current_user_id)],
    query: str = Query(default="iphone 13"),
    location: str = Query(default="united-states"),
    limit: int = Query(default=8, ge=1, le=50),
) -> OpportunityListResponse:
    try:
        return await ingest_pipeline.run(
            IngestRequest(
                query=query,
                location=location,
                limit=limit,
                sources=["facebook_marketplace"],
            ),
            user_id=user_id,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
