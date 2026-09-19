from fastapi import APIRouter

from app.api.deals import router as deals_router
from app.api.health import router as health_router
from app.api.ingest import router as ingest_router
from app.api.searches import router as searches_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(deals_router)
api_router.include_router(ingest_router)
api_router.include_router(searches_router)
