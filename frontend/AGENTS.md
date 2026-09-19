# Frontend — DealSniper UI

React + TypeScript dashboard for marketplace arbitrage discovery.

## Run

```bash
npm install
npm run dev
```

## Routes

- `/` redirects to `/radar`
- `/radar` searchable, filterable opportunity feed
- `/opportunities/:id` financial analysis
- `/saved` bookmarked deals (localStorage)
- `/*` tasteful 404

Do not add login, settings, analytics, or other dead navigation.

## Data

Use mock opportunities in `src/data/`. Filtering and scoring display happen on the client. Zustand persists saved IDs.

## Visual system

Navy header, white cards, emerald profit, amber uncertainty, Geist/Inter, compact SaaS density. Icons from `lucide-react` only.
