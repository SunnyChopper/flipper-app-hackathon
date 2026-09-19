# Frontend — DealSniper UI

React + TypeScript dashboard for marketplace arbitrage discovery.

## Run

```bash
npm install
npm run dev
```

## Routes

- `/login` Supabase email/password sign in and sign up
- `/` redirects to `/radar`
- `/radar` searchable, filterable opportunity feed
- `/opportunities/:id` financial analysis
- `/saved` bookmarked deals
- `/*` tasteful 404

Radar, Saved, and opportunity detail require a session when `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` are set. Local demo without those keys stays open.

## Auth

Use `@supabase/supabase-js` in the React app. Do not build a custom password table or FastAPI login UI. Forward the access token as `Authorization: Bearer` on FastAPI calls.

## Data

Use mock opportunities in `src/data/`. Filtering and scoring display happen on the client. Zustand persists saved IDs.

## Visual system

Navy header, white cards, emerald profit, amber uncertainty, Geist/Inter, compact SaaS density. Icons from `lucide-react` only.
