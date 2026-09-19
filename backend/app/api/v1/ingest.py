from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from app.auth import get_current_user_id
from app.models.ingest import IngestRequest
from app.schemas.opportunity import OpportunityListResponse
from app.services.crawler import crawl_scheduler
from app.services.ingest import ingest_pipeline

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=OpportunityListResponse)
async def ingest_marketplaces(
    user_id: Annotated[str, Depends(get_current_user_id)],
    payload: IngestRequest | None = Body(default=None),
) -> OpportunityListResponse:
    try:
        return await ingest_pipeline.run(payload or IngestRequest(), user_id=user_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/tick")
async def run_crawl_tick(_user_id: Annotated[str, Depends(get_current_user_id)]) -> dict[str, object]:
    try:
        results = await crawl_scheduler.tick()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {
        "results": [
            {
                "category": item.category,
                "query": item.query,
                "inserted": item.inserted,
                "skipped": item.skipped,
                "rejected": item.rejected,
                "error": item.error,
            }
            for item in results
        ],
        "status": crawl_scheduler.status.__dict__,
    }
