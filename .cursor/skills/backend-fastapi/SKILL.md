---
name: backend-fastapi
description: Build and change the Deal Sniper FastAPI backend — routes, marketplace ingestion, listing normalization, and deal scoring. Use when working in backend/, FastAPI, Python APIs, eBay, Apify, or scoring endpoints.
---

# Backend FastAPI

## Do this

1. Read `backend/AGENTS.md` and the existing service before adding a new module.
2. Put HTTP in `app/api/`. Put marketplace and scoring logic in `app/services/`.
3. Keep response models in `app/models/`. The frontend depends on `Deal`.
4. Preserve mock fallbacks when `APIFY_TOKEN` or `OPENAI_API_KEY` are empty.

## Deal pipeline

`listing (ebay.py / apify.py) → analyzer.normalize → deal_scorer.score → store / API`

Do not skip normalization. Do not compute profit in route handlers.

## Adding an endpoint

Register new routers in `app/api/__init__.py`.
