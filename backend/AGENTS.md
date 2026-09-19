# Backend — Deal Sniper API

FastAPI service for marketplace orchestration, listing normalization, repair estimates, and deal scoring.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Layout

- `app/main.py` — FastAPI app and CORS
- `app/api/` — HTTP routes only
- `app/services/ebay.py` — eBay fetch via Apify
- `app/services/apify.py` — Facebook Marketplace via Apify
- `app/services/analyzer.py` — title/description (and later vision) normalization
- `app/services/deal_scorer.py` — profit / risk / overall score
- `app/models/` — Pydantic contracts shared with the frontend shape

## Conventions

- Routes stay thin. Business logic lives in services.
- Return `Deal` from ingest and list endpoints so the UI never has to score.
- If a third-party key is missing, use the mock path. Do not fail local demo.
- Deploy as a Render web service from this folder.
