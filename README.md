# Deal Sniper

Hackathon monorepo for finding underpriced marketplace listings, scoring flip potential, and pushing live “snipe” updates into the UI.

| Layer | Tech | Deploy |
|---|---|---|
| Frontend | React + TypeScript + Vite | Vercel |
| Backend API | FastAPI + Python | Render |
| Data / Auth / Realtime | Supabase | Managed |
| Ingestion | eBay API + Apify | Apify jobs |
| Analysis | LLM / vision stubs | Called from FastAPI |

```
deal-sniper/
├── frontend/     DealSniper dashboard: /radar, /opportunities/:id, /saved
├── backend/      FastAPI orchestration, scoring, marketplace adapters
└── supabase/     schema, RLS, seed data
```

## Quick start

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

The API returns mock deals if Supabase credentials are empty, so the UI works immediately.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The UI is frontend-first and runs on mock opportunities — no backend required for the Radar, analysis, or Saved flows.

### Supabase

Apply `supabase/migrations/` then `supabase/seed.sql` in the SQL editor, or with the Supabase CLI:

```bash
supabase db reset
```

## Agent guidance

Each package has `AGENTS.md` (how to work in that folder) and `SKILL.md` (domain skill for that layer). Project-wide Cursor skills live in `.cursor/skills/`.
