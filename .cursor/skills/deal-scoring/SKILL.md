---
name: deal-scoring
description: Normalize messy marketplace listings and score flip profit, repair cost, fees, and risk. Use when changing analyzer.py, deal_scorer.py, LLM/vision analysis, comps, or profit math.
---

# Deal scoring

## Pipeline

1. `analyzer.normalize(listing)` → `NormalizedProduct`
2. `deal_scorer.score(listing, product)` → `Deal`

Heuristic scoring is the default. When `OPENAI_API_KEY` is set, keep the same Pydantic output — only the internals of `analyzer` should change.

## Score fields

- `estimated_resale`
- `repair_estimate`
- `fees_estimate`
- `net_profit`
- `profit_margin`
- `risk_score` (0-100)
- `overall_score` (0-100)
- `rationale`

Do not compute these in React. Persist them on `deal_scores` when Supabase is connected.
