# FranceScope V3 — Frontend Architecture

Date: 2026-08-24. Presentation-only layer over frozen V3 model artifacts.

## Framework

- **Next.js 16** (App Router, React 19, TypeScript, Turbopack).
- **Tailwind CSS v4** for styling (neutral, institutional design: zinc palette, whitespace, clear hierarchy).
- **Recharts v3** for all charts (line, band/area, comparison).
- No backend, no API server, no authentication. Pure static presentation.

The existing repo already contained a Next.js + recharts frontend scaffold; this work replaced its
backend-API data contract (`src/lib/api.ts` calling `127.0.0.1:8000`) with a static-file
data layer, and implemented the required Overview / Forecast / Scenarios / Methodology pages.

## Routes (pages)

| Route | Purpose |
|-------|---------|
| `/` (Overview) | Hero, three-phase explainer, historical Index (2010–2026) with bridge distinction, 2026 context, 2050 MC1000 snapshot, scenario cards. |
| `/forecast` | Distribution bands (P05–P95 outer, P10–P90 inner, P50 median) and percentile tables for Index, GDPpc, unemployment, median living, debt at 2030/2040/2050. Explicit "percentiles ≠ confidence interval" language. |
| `/scenarios` | Side-by-side comparison (2030/2040/2050), annual Index comparison chart (paths 856/524/367), and three detail blocks (narrative, drivers, Index logic, fiscal/debt, turning points, limitations). |
| `/methodology` | Pipeline diagram + sections A–G + interpretation notes. |

## Authoritative data artifacts consumed (frozen, read-only)

- `data/processed/index/francescope_v3_historical_index_2010_2026.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_MC1000_INDEX_DISTRIBUTIONS.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_MC1000_CORE_DISTRIBUTIONS.csv`
- `data/processed/scenarios/francescope_v3_coherent_p10_p50_p90_paths.parquet`
- `data/processed/scenarios/francescope_v3_coherent_scenario_summary.json`

## Frontend-derived data artifacts (presentation transformation only)

Built by `frontend/scripts/build_frontend_data.py` (no recomputation of economics):

- `frontend/public/data/historical_index.json` — annual 2010–2026 + `current_2026` (debt 2026 sourced from published narrative bridge anchor, 123.3%, since the historical file carries no debt column; annual debt left null).
- `frontend/public/data/distributions.json` — P05–P95 / mean / sd per metric per year (2030/2040/2050) from the two MC1000 distribution audits.
- `frontend/public/data/scenarios.json` — scenario summary JSON augmented with the annual 2027–2050 trajectories per path.
- `frontend/public/data/methodology.json` — static methodology text + pipeline.

Server components load these via `src/lib/data.ts` (Node `fs` read of `public/data`), so no client
network fetch or browser parquet parsing is required.

## Key source files

- `src/lib/types.ts` — shared types + `SCENARIO_COLORS` (P10 #b45309, P50 #2563eb, P90 #047857).
- `src/lib/data.ts` — static JSON loaders.
- `src/lib/format.ts` — number/percent formatters.
- `src/components/SiteNav.tsx` — top navigation.
- `src/components/SeriesChart.tsx` — generic multi-line chart.
- `src/components/BandChart.tsx` — distribution band chart.
- `src/app/{layout,page}.tsx`, `src/app/forecast/page.tsx`, `src/app/scenarios/page.tsx`, `src/app/methodology/page.tsx`.

## How to run locally

```bash
cd frontend
python scripts/build_frontend_data.py   # regenerate public/data JSON (optional; already present)
npm install
npm run dev        # http://localhost:3000
# production:
npm run build && npm run start
```

## Validation performed

- `npm run build` passes (TypeScript + static prerender of all 4 routes).
- Runtime check: all routes return 200 with expected content — 2026 Index 140.95, debt 123.3%,
  2050 P90 Index 192.8%, scenario path IDs 856/524/367, scenario 2050 Index 142.5/166.6/190.3,
  debt-exclusion copy present, "zero GFC" note present, P10/P90 percentile wording correct.

## Next integration point (NOT implemented here)

The explanatory LLM layer is the designated next task. It should consume
`frontend/public/data/scenarios.json` (and the narrative fields already present) to answer
user questions about scenarios, drivers, and limitations. No backend is required; a client-side
or server-side LLM call can read the static JSON. The frontend currently has no chatbot, API,
RAG, embeddings, or vector DB.
