---
name: deal-sniper-architecture
description: Deal Sniper monorepo architecture — React frontend, FastAPI backend, Supabase, eBay/Apify ingestion, and LLM analysis. Use when starting work, choosing where code belongs, or changing cross-package flow.
---

# Deal Sniper architecture

## Packages

- `frontend/` React + Vite, deploy to Vercel
- `backend/` FastAPI, deploy to Render
- `supabase/` Postgres + Auth + Realtime

Read the folder `AGENTS.md` before editing that package.

## Data flow

1. `backend` pulls eBay / Facebook listings
2. `analyzer` normalizes title/description (optional vision)
3. `deal_scorer` estimates resale, repairs, fees, profit, risk
4. Rows land in Supabase (`listings`, `normalized_products`, `deal_scores`)
5. React reads scored deals from FastAPI and subscribes to `deal_scores` for live snipes

## Boundaries

- Frontend never calls eBay or Apify
- Frontend never computes profit
- Backend never owns Auth UI
- Secrets stay in backend env, except Supabase anon key in frontend
