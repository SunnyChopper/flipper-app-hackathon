---
name: supabase-data
description: Change Deal Sniper Supabase schema, RLS, seed data, Auth, and Realtime. Use when working in supabase/, SQL migrations, listings, deal_scores, saved_searches, or live deal updates.
---

# Supabase data

## Do this

1. Read `supabase/AGENTS.md` before writing SQL.
2. Add a new timestamped file under `supabase/migrations/` instead of rewriting an applied migration.
3. Keep RLS enabled. Browser reads listings/scores; only the owner reads/writes `saved_searches`.
4. After adding a table the UI should live-update, add it to `supabase_realtime`.

## Core entities

`listings → normalized_products → deal_scores`
`listings` are the source of truth for marketplace rows. Scores are derived.

## Auth

Supabase Auth owns users. `profiles.id` references `auth.users.id`. Never create a parallel password table.
