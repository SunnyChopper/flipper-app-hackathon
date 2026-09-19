-- Canonical Deal Sniper contract model.
-- Opportunity is a UI/API projection and is intentionally not persisted.

create table if not exists public.repair_skills (
  slug text primary key,
  display_name text not null,
  category text not null
);

alter table public.profiles
  add column if not exists persona text not null default 'restorer'
    check (persona in ('restorer', 'harvester')),
  add column if not exists min_profit_margin_usd numeric(12, 2) not null default 100,
  add column if not exists min_roi_percent numeric(8, 2) not null default 20,
  add column if not exists updated_at timestamptz not null default now();

create table if not exists public.user_skills (
  user_id uuid not null references public.profiles (id) on delete cascade,
  skill_slug text not null references public.repair_skills (slug) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, skill_slug)
);

create table if not exists public.catalog_products (
  id uuid primary key default gen_random_uuid(),
  brand text not null,
  model text not null,
  variant text,
  category text not null,
  estimated_working_market_value numeric(12, 2) not null,
  valuation_confidence_score numeric(4, 3) not null check (valuation_confidence_score between 0 and 1),
  last_valuation_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists public.product_market_comps (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references public.catalog_products (id) on delete cascade,
  source text not null,
  sold_price numeric(12, 2) not null,
  shipping_price numeric(12, 2) not null default 0,
  item_condition text not null,
  sold_date date not null,
  listing_url text not null,
  created_at timestamptz not null default now()
);

create table if not exists public.components (
  id uuid primary key default gen_random_uuid(),
  name text not null
);

create table if not exists public.product_bom_items (
  id uuid primary key default gen_random_uuid(),
  product_id uuid not null references public.catalog_products (id) on delete cascade,
  component_id uuid not null references public.components (id) on delete restrict,
  required_skill_slug text not null references public.repair_skills (slug),
  avg_replacement_cost numeric(12, 2) not null,
  salvage_resale_value numeric(12, 2) not null default 0,
  harvest_liquidity_score int not null check (harvest_liquidity_score between 1 and 5)
);

-- Existing listings table is additive-extended to match the Listing contract.
update public.listings
set source = 'facebook_marketplace'
where source = 'facebook';

alter table public.listings drop constraint if exists listings_source_check;
alter table public.listings
  add constraint listings_source_check
  check (source in ('ebay', 'facebook_marketplace'));

alter table public.listings
  add column if not exists shipping_cost numeric(12, 2) not null default 0,
  add column if not exists condition text not null default 'used_fair',
  add column if not exists image_urls text[] not null default '{}',
  add column if not exists listed_at timestamptz,
  add column if not exists matched_product_id uuid references public.catalog_products (id),
  add column if not exists detected_defective_bom_ids uuid[] not null default '{}',
  add column if not exists required_repair_skills text[] not null default '{}',
  add column if not exists projected_restorer_net numeric(12, 2) not null default 0,
  add column if not exists projected_harvest_yield numeric(12, 2) not null default 0;

update public.listings
set image_urls = array[image_url]
where image_url is not null
  and (image_urls is null or cardinality(image_urls) = 0);

create table if not exists public.user_deals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.profiles (id) on delete cascade,
  listing_id uuid not null references public.listings (id) on delete cascade,
  status text not null check (status in ('saved', 'acquired', 'dismissed')),
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, listing_id)
);

create index if not exists catalog_products_category_idx on public.catalog_products (category);
create index if not exists listings_matched_product_idx on public.listings (matched_product_id);
create index if not exists listings_condition_idx on public.listings (condition);
create index if not exists listings_listed_at_idx on public.listings (listed_at desc);
create index if not exists user_deals_user_status_idx on public.user_deals (user_id, status);

alter table public.repair_skills enable row level security;
alter table public.user_skills enable row level security;
alter table public.catalog_products enable row level security;
alter table public.product_market_comps enable row level security;
alter table public.components enable row level security;
alter table public.product_bom_items enable row level security;
alter table public.user_deals enable row level security;

create policy "public read repair_skills" on public.repair_skills for select using (true);
create policy "public read catalog_products" on public.catalog_products for select using (true);
create policy "public read product_market_comps" on public.product_market_comps for select using (true);
create policy "public read components" on public.components for select using (true);
create policy "public read product_bom_items" on public.product_bom_items for select using (true);

create policy "users read own skills" on public.user_skills
  for select using (auth.uid() = user_id);
create policy "users manage own skills" on public.user_skills
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "users manage own deals" on public.user_deals
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
