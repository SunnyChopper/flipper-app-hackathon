from fastapi import APIRouter

from app.api.v1.deals import router as deals_router
from app.api.v1.ingest import router as ingest_router
from app.api.v1.opportunities import router as opportunities_router
from app.api.v1.profiles import router as profiles_router
from app.api.v1.repair_skills import router as repair_skills_router
from app.api.v1.searches import router as searches_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(opportunities_router)
v1_router.include_router(ingest_router)
v1_router.include_router(deals_router)
v1_router.include_router(profiles_router)
v1_router.include_router(repair_skills_router)
v1_router.include_router(searches_router)
