-- Deal Sniper initial schema
-- Apply in the Supabase SQL editor or via `supabase db reset`.

create extension if not exists "pgcrypto";

create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now()
);

create table if not exists public.listings (
  id uuid primary key default gen_random_uuid(),
  source text not null check (source in ('ebay', 'facebook')),
  external_id text not null,
  title text not null,
  description text not null default '',
  price numeric(12, 2) not null,
  currency text not null default 'USD',
  url text not null,
  image_url text,
  location text,
  raw jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (source, external_id)
);

create table if not exists public.normalized_products (
  id uuid primary key default gen_random_uuid(),
  listing_id uuid not null references public.listings (id) on delete cascade,
  brand text,
  model text,
  category text not null default 'unknown',
  condition text not null default 'used',
  normalized_title text not null,
  attributes jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.comps (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references public.normalized_products (id) on delete cascade,
  sold_price numeric(12, 2) not null,
  sold_at timestamptz,
  source text,
  url text,
  created_at timestamptz not null default now()
);

create table if not exists public.repair_costs (
  id uuid primary key default gen_random_uuid(),
  category text not null,
  issue text not null,
  estimated_cost numeric(12, 2) not null,
  created_at timestamptz not null default now()
);

create table if not exists public.deal_scores (
  id uuid primary key default gen_random_uuid(),
  listing_id uuid not null references public.listings (id) on delete cascade,
  estimated_resale numeric(12, 2) not null,
  repair_estimate numeric(12, 2) not null default 0,
  fees_estimate numeric(12, 2) not null default 0,
  net_profit numeric(12, 2) not null,
  profit_margin numeric(8, 2) not null,
  risk_score int not null check (risk_score between 0 and 100),
  overall_score int not null check (overall_score between 0 and 100),
  rationale text,
  created_at timestamptz not null default now()
);

create table if not exists public.saved_searches (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  name text not null,
  query text not null default '',
  filters jsonb not null default '{}'::jsonb,
  notify boolean not null default true,
  created_at timestamptz not null default now()
);

create index if not exists listings_source_idx on public.listings (source);
create index if not exists deal_scores_listing_idx on public.deal_scores (listing_id);
create index if not exists deal_scores_overall_idx on public.deal_scores (overall_score desc);

alter table public.profiles enable row level security;
alter table public.listings enable row level security;
alter table public.normalized_products enable row level security;
alter table public.comps enable row level security;
alter table public.repair_costs enable row level security;
alter table public.deal_scores enable row level security;
alter table public.saved_searches enable row level security;

create policy "public read listings" on public.listings for select using (true);
create policy "public read products" on public.normalized_products for select using (true);
create policy "public read comps" on public.comps for select using (true);
create policy "public read repairs" on public.repair_costs for select using (true);
create policy "public read scores" on public.deal_scores for select using (true);

create policy "users read own profile" on public.profiles
  for select using (auth.uid() = id);
create policy "users update own profile" on public.profiles
  for update using (auth.uid() = id);

create policy "users manage own searches" on public.saved_searches
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Realtime: frontend subscribes to deal_scores inserts for live snipe updates.
alter publication supabase_realtime add table public.deal_scores;
