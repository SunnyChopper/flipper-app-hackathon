-- Demo rows for local / hackathon screens. Safe to re-run after truncate.

insert into public.repair_costs (category, issue, estimated_cost)
values
  ('home', 'battery', 45),
  ('home', 'dent', 20),
  ('electronics', 'cracked glass', 89),
  ('tools', 'missing charger', 28);

-- Listings / scores are seeded by the FastAPI in-memory store until
-- the backend writes through SUPABASE_SERVICE_ROLE_KEY.
