from fastapi import APIRouter, Body, HTTPException, Query

from app.models.deal import Deal
from app.models.ingest import IngestRequest
from app.services.ingest import ingest_pipeline

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("", response_model=list[Deal])
async def ingest_marketplaces(payload: IngestRequest | None = Body(default=None)) -> list[Deal]:
    try:
        return await ingest_pipeline.run(payload or IngestRequest())
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/ebay", response_model=list[Deal])
async def ingest_ebay(
    query: str = Query(default="dyson vacuum"),
    limit: int = Query(default=8, ge=1, le=50),
) -> list[Deal]:
    try:
        return await ingest_pipeline.run(IngestRequest(query=query, limit=limit, sources=["ebay"]))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/facebook", response_model=list[Deal])
async def ingest_facebook(
    query: str = Query(default="kitchenaid mixer"),
    location: str = Query(default="united-states"),
    limit: int = Query(default=8, ge=1, le=50),
) -> list[Deal]:
    try:
        return await ingest_pipeline.run(
            IngestRequest(query=query, location=location, limit=limit, sources=["facebook"])
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
