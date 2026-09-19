-- Prevent the crawler from inserting the same marketplace listing twice.
-- Init already unique'd (source, external_id); this makes that explicit and
-- also rejects the same listing URL arriving under a different external id.

create unique index if not exists listings_source_external_id_key
  on public.listings (source, external_id);

create unique index if not exists listings_url_uidx
  on public.listings (url);

alter table public.listings
  add column if not exists last_crawled_at timestamptz not null default now();
