-- Canonical catalog, BOM, and listing rows for local / hackathon screens.
-- Safe to re-run after truncate of these tables.

-- Demo API user (the hosted app has no Auth UI yet).
do $$
declare
  demo_id uuid := '00000000-0000-4000-8000-000000000001';
begin
  if not exists (select 1 from auth.users where id = demo_id) then
    insert into auth.users (
      instance_id,
      id,
      aud,
      role,
      email,
      encrypted_password,
      email_confirmed_at,
      raw_app_meta_data,
      raw_user_meta_data,
      created_at,
      updated_at
    ) values (
      '00000000-0000-0000-0000-000000000000',
      demo_id,
      'authenticated',
      'authenticated',
      'demo@dealsniper.local',
      crypt('demo-password', gen_salt('bf')),
      now(),
      '{"provider":"email","providers":["email"]}'::jsonb,
      '{}'::jsonb,
      now(),
      now()
    );
  end if;
end $$;

insert into public.repair_costs (category, issue, estimated_cost)
values
  ('home', 'battery', 45),
  ('home', 'dent', 20),
  ('electronics', 'cracked glass', 89),
  ('tools', 'missing charger', 28);

insert into public.repair_skills (slug, display_name, category)
values
  ('screen_swap', 'Screen / Display Replacement', 'electronics'),
  ('battery_replacement', 'Battery Replacement', 'electronics'),
  ('board_level_repair', 'Board-Level Repair', 'electronics')
on conflict (slug) do nothing;

insert into public.profiles (id, display_name, persona, min_profit_margin_usd, min_roi_percent)
values ('00000000-0000-4000-8000-000000000001', 'Demo flipper', 'restorer', 100, 20)
on conflict (id) do nothing;

insert into public.user_skills (user_id, skill_slug)
values
  ('00000000-0000-4000-8000-000000000001', 'screen_swap'),
  ('00000000-0000-4000-8000-000000000001', 'battery_replacement')
on conflict do nothing;

insert into public.catalog_products (
  id, brand, model, variant, category,
  estimated_working_market_value, valuation_confidence_score, last_valuation_at
)
values
  ('11111111-1111-4111-8111-111111111111', 'Apple', 'iPhone 13', '128GB Unlocked', 'smartphones', 425, 0.92, '2026-09-19T10:00:00Z'),
  ('22222222-2222-4222-8222-222222222222', 'Sony', 'PlayStation 5', 'Disc Edition', 'gaming_consoles', 370, 0.88, '2026-09-19T10:00:00Z'),
  ('33333333-3333-4333-8333-333333333333', 'Apple', 'MacBook Air M1', '256GB', 'laptops', 680, 0.85, '2026-09-19T10:00:00Z')
on conflict (id) do nothing;

insert into public.components (id, name)
values
  ('41111111-1111-4111-8111-111111111111', 'OLED Screen Assembly'),
  ('42222222-2222-4222-8222-222222222222', 'iPhone Battery'),
  ('43333333-3333-4333-8333-333333333333', 'HDMI Board'),
  ('44444444-4444-4444-8444-444444444444', 'Power Supply Unit'),
  ('45555555-5555-4555-8555-555555555555', 'MacBook Display Assembly')
on conflict (id) do nothing;

insert into public.product_bom_items (
  id, product_id, component_id, required_skill_slug,
  avg_replacement_cost, salvage_resale_value, harvest_liquidity_score
)
values
  ('51111111-1111-4111-8111-111111111111', '11111111-1111-4111-8111-111111111111', '41111111-1111-4111-8111-111111111111', 'screen_swap', 90, 35, 5),
  ('52222222-2222-4222-8222-222222222222', '11111111-1111-4111-8111-111111111111', '42222222-2222-4222-8222-222222222222', 'battery_replacement', 45, 28, 4),
  ('53333333-3333-4333-8333-333333333333', '22222222-2222-4222-8222-222222222222', '43333333-3333-4333-8333-333333333333', 'board_level_repair', 70, 32, 3),
  ('54444444-4444-4444-8444-444444444444', '22222222-2222-4222-8222-222222222222', '44444444-4444-4444-8444-444444444444', 'board_level_repair', 55, 30, 4),
  ('55555555-5555-4555-8555-555555555555', '33333333-3333-4333-8333-333333333333', '45555555-5555-4555-8555-555555555555', 'screen_swap', 180, 90, 5)
on conflict (id) do nothing;

insert into public.product_market_comps (
  id, product_id, source, sold_price, shipping_price, item_condition, sold_date, listing_url
)
values
  ('71111111-1111-4111-8111-111111111111', '11111111-1111-4111-8111-111111111111', 'ebay_sold', 410, 15, 'used_working', '2026-09-17', 'https://www.ebay.com/itm/mock-iphone-comp-1'),
  ('71111112-1111-4111-8111-111111111112', '11111111-1111-4111-8111-111111111111', 'ebay_sold', 399, 12, 'used_working', '2026-09-14', 'https://www.ebay.com/itm/mock-iphone-comp-2'),
  ('71111113-1111-4111-8111-111111111113', '11111111-1111-4111-8111-111111111111', 'ebay_sold', 430, 0, 'used_working', '2026-09-10', 'https://www.ebay.com/itm/mock-iphone-comp-3'),
  ('72222221-2222-4222-8222-222222222221', '22222222-2222-4222-8222-222222222222', 'ebay_sold', 355, 15, 'used_working', '2026-09-16', 'https://www.ebay.com/itm/mock-ps5-comp-1'),
  ('72222222-2222-4222-8222-222222222222', '22222222-2222-4222-8222-222222222222', 'ebay_sold', 349, 20, 'used_working', '2026-09-12', 'https://www.ebay.com/itm/mock-ps5-comp-2'),
  ('72222223-2222-4222-8222-222222222223', '22222222-2222-4222-8222-222222222222', 'ebay_sold', 380, 0, 'used_working', '2026-09-08', 'https://www.ebay.com/itm/mock-ps5-comp-3'),
  ('73333331-3333-4333-8333-333333333331', '33333333-3333-4333-8333-333333333333', 'ebay_sold', 650, 20, 'used_working', '2026-09-15', 'https://www.ebay.com/itm/mock-mba-comp-1'),
  ('73333332-3333-4333-8333-333333333332', '33333333-3333-4333-8333-333333333333', 'ebay_sold', 680, 15, 'used_working', '2026-09-11', 'https://www.ebay.com/itm/mock-mba-comp-2'),
  ('73333333-3333-4333-8333-333333333333', '33333333-3333-4333-8333-333333333333', 'ebay_sold', 640, 25, 'used_working', '2026-09-07', 'https://www.ebay.com/itm/mock-mba-comp-3')
on conflict (id) do nothing;

insert into public.listings (
  id, source, external_id, title, description, price, url, image_url,
  shipping_cost, condition, image_urls, listed_at, created_at,
  matched_product_id, detected_defective_bom_ids, required_repair_skills,
  projected_restorer_net, projected_harvest_yield
)
values
  (
    '61111111-1111-4111-8111-111111111111',
    'facebook_marketplace',
    'fb-iphone-13-cracked',
    'iPhone 13 128GB cracked screen works fine',
    'Screen damaged but everything else works.',
    220,
    'https://www.facebook.com/marketplace/item/mock-iphone-cracked',
    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80',
    0,
    'damaged',
    array[
      'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=900&q=80'
    ],
    '2026-09-19T12:00:00Z',
    '2026-09-19T12:03:00Z',
    '11111111-1111-4111-8111-111111111111',
    array['51111111-1111-4111-8111-111111111111']::uuid[],
    array['screen_swap'],
    115,
    -192
  ),
  (
    '62222222-2222-4222-8222-222222222222',
    'ebay',
    'ebay-iphone-13-battery',
    'iPhone 13 128GB swollen battery Face ID works',
    'Unlocked. Screen is fine. Battery is swollen and needs replacement.',
    155,
    'https://www.ebay.com/itm/mock-iphone-battery',
    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80',
    10,
    'used_fair',
    array['https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80'],
    '2026-09-19T08:30:00Z',
    '2026-09-19T08:32:00Z',
    '11111111-1111-4111-8111-111111111111',
    array['52222222-2222-4222-8222-222222222222']::uuid[],
    array['battery_replacement'],
    215,
    -130
  ),
  (
    '63333333-3333-4333-8333-333333333333',
    'ebay',
    'ebay-ps5-nopower',
    'PS5 Disc Edition won''t power on',
    'No lights. HDMI port looks intact. Sold as-is for parts or repair.',
    120,
    'https://www.ebay.com/itm/mock-ps5-nopower',
    'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=900&q=80',
    18,
    'for_parts',
    array[
      'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1607853202273-797f1c22a38e?auto=format&fit=crop&w=900&q=80'
    ],
    '2026-09-19T07:00:00Z',
    '2026-09-19T07:05:00Z',
    '22222222-2222-4222-8222-222222222222',
    array['54444444-4444-4444-8444-444444444444']::uuid[],
    array['board_level_repair'],
    177,
    -106
  ),
  (
    '64444444-4444-4444-8444-444444444444',
    'facebook_marketplace',
    'fb-ps5-hdmi',
    'PS5 Disc Edition no picture HDMI issue',
    'Console powers on. Fans spin. No video output.',
    145,
    'https://www.facebook.com/marketplace/item/mock-ps5-hdmi',
    'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=900&q=80',
    0,
    'damaged',
    array['https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?auto=format&fit=crop&w=900&q=80'],
    '2026-09-18T21:00:00Z',
    '2026-09-18T21:04:00Z',
    '22222222-2222-4222-8222-222222222222',
    array['53333333-3333-4333-8333-333333333333']::uuid[],
    array['board_level_repair'],
    155,
    -115
  ),
  (
    '65555555-5555-4555-8555-555555555555',
    'facebook_marketplace',
    'fb-mba-screen',
    'MacBook Air M1 screen damage cosmetic wear',
    'Screen damage, cosmetic wear on lid. Keyboard appears complete.',
    300,
    'https://www.facebook.com/marketplace/item/mock-mba-screen',
    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80',
    0,
    'damaged',
    array[
      'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80',
      'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80'
    ],
    '2026-09-19T03:00:00Z',
    '2026-09-19T03:06:00Z',
    '33333333-3333-4333-8333-333333333333',
    array['55555555-5555-4555-8555-555555555555']::uuid[],
    array['screen_swap'],
    200,
    -300
  ),
  (
    '66666666-6666-4666-8666-666666666666',
    'ebay',
    'ebay-mba-parts',
    'MacBook Air M1 256GB for parts cracked display',
    'Activation lock off. Display is cracked. Logic board not tested.',
    190,
    'https://www.ebay.com/itm/mock-mba-parts',
    'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80',
    25,
    'for_parts',
    array['https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80'],
    '2026-09-18T16:00:00Z',
    '2026-09-18T16:10:00Z',
    '33333333-3333-4333-8333-333333333333',
    array['55555555-5555-4555-8555-555555555555']::uuid[],
    array['screen_swap'],
    285,
    -215
  )
on conflict (source, external_id) do nothing;
