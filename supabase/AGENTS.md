# Supabase

Postgres, Auth, and Realtime for Deal Sniper.

## Apply

1. Create a Supabase project.
2. Run every file in `migrations/` in order (SQL editor or `supabase db reset`).
3. Run `seed.sql`.
4. Copy project URL + anon key into `frontend/.env`.
5. Copy project URL + service role key into `backend/.env`.
6. In Authentication settings, add `http://localhost:5173` to Redirect URLs. For local demo, you can turn off “Confirm email”.

## Tables

| Table | Purpose |
|---|---|
| `listings` | Raw eBay / Facebook Marketplace items |
| `normalized_products` | Structured product extracted from messy titles |
| `comps` | Sold comparables |
| `repair_costs` | Category-level repair estimates |
| `deal_scores` | Profit, fees, risk, overall score |
| `saved_searches` | User search alerts |
| `profiles` | App profile on `auth.users` |

`deal_scores` is in the Realtime publication. The UI should subscribe to inserts for live snipes.

## Conventions

- RLS is on. The browser uses the anon key for reads and auth. The backend uses the service role for writes.
- `handle_new_user` inserts a `profiles` row on Auth signup. Do not create a parallel password table.
- Do not add marketplace secrets to the frontend env.
- Keep migrations additive. Do not edit an already-applied migration; add a new file.
