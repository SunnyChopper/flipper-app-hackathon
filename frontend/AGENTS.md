# Frontend — Deal Sniper UI

React + TypeScript app for search, filters, deal cards, profit/risk views, and saved searches.

## Run

```bash
npm install
npm run dev
```

Deploy this folder to Vercel. `vercel.json` already rewrites to `index.html`.

## Layout

- `src/pages/SearchPage.tsx` — feed + filters
- `src/pages/DealDetailPage.tsx` — profit / risk breakdown
- `src/pages/SavedSearchesPage.tsx` — saved queries
- `src/pages/AuthPage.tsx` — Supabase Auth
- `src/components/` — presentational UI
- `src/lib/api.ts` — FastAPI client
- `src/lib/supabase.ts` — Auth + Realtime client

## Conventions

- Talk to FastAPI for deals, ingest, and saved searches.
- Use Supabase only for Auth and Realtime (`deal_scores` inserts).
- Do not score deals in the browser. Render `Deal.score` from the API.
- Keep styling in `src/index.css`. Match the existing dark / serif / mono look.
