---
name: marketplace-ingestion
description: Fetch and map eBay and Facebook Marketplace listings into Deal Sniper Listing models via eBay API and Apify. Use when working on ingestion, scrapers, ebay.py, apify.py, or marketplace adapters.
---

# Marketplace ingestion

## Adapters

- `backend/app/services/ebay.py` — eBay Browse API
- `backend/app/services/apify.py` — Facebook Marketplace via Apify
- HTTP triggers in `backend/app/api/ingest.py`

## Rules

- Map every source into `Listing`. Do not leak raw source JSON into React.
- If the API token is missing, return the mock listing used for local demo.
- Keep collection out of the frontend and out of `deal_scorer.py`.
- After fetch, always run `analyzer.normalize` then `deal_scorer.score`.
