# Deal Sniper

Monorepo for a marketplace flip / deal-sniping app.

## Layout

- `frontend/` — React + TypeScript UI (Vercel)
- `backend/` — FastAPI orchestration, scoring, ingestion adapters (Render)
- `supabase/` — Postgres schema, RLS, seed data

Read the `AGENTS.md` and `SKILL.md` in the folder you are changing before editing.

## Product surface

- Search + filters for marketplace listings
- Deal cards with profit and risk
- Saved searches
- Live updates when new scored deals arrive
- Auth via Supabase

## Rules

- Keep collection (eBay / Apify) out of the React app. Frontend talks only to FastAPI and Supabase Auth/Realtime.
- Normalize messy listing data in `backend/app/services/analyzer.py` before scoring.
- Score deals in `backend/app/services/deal_scorer.py`. Do not scatter profit math across the UI.
- Prefer mock/fallback paths so local demo works without every third-party key.
- Do not commit secrets. Use `.env.example` files.
