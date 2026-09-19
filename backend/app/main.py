from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import settings
from app.services.crawler import crawl_scheduler


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await crawl_scheduler.start()
    try:
        yield
    finally:
        await crawl_scheduler.stop()


app = FastAPI(
    title="Deal Sniper API",
    description="Marketplace orchestration, normalization, and deal scoring.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
