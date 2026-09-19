---
name: frontend-deals-ui
description: Build Deal Sniper React UI — search, filters, deal cards, profit/risk views, saved searches, and Supabase auth/realtime. Use when working in frontend/, React, Vite, TypeScript pages, or deal cards.
---

# Frontend deals UI

## Do this

1. Read `frontend/AGENTS.md` before changing pages.
2. Fetch `Deal` objects from FastAPI via `src/lib/api.ts`. Never duplicate scoring math.
3. Put screens in `src/pages/` and reusable pieces in `src/components/`.
4. Use `src/lib/supabase.ts` for Auth and Realtime only.

## Screens

- `/` search + filters + deal cards
- `/deals/:id` profit / risk
- `/saved` saved searches
- `/login` Supabase Auth

## Styling

Keep the existing tokens in `src/index.css`: forest background, lime profit, orange risk, Newsreader headings, IBM Plex Mono data.
