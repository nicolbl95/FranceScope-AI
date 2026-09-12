# FranceScope Changelog

All notable changes to FranceScope are documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [4.0.0] - 2026-08-25 — Official V4 MC1000 Release (FROZEN)

FranceScope V4 is the official, frozen baseline: 1,000-path Monte Carlo simulation
(2027–2050), fixed master seed **20260815**, 24,000 rows. Core structural corrections
(CORR-1 → CORR-4) are implemented and deterministically validated; the Next.js frontend
and LLM grounding layer are aligned to the official V4 results.

### Core Structural Corrections (frozen equations & calibration)

- **CORR-1 — Debt/Financing → Investment → Capital → Productivity**
  Corporate financing (credit-rate) gap suppresses the investment-level gap, which
  accumulates into a capital-stock gap (actual vs potential), producing a productivity
  growth deviation. Frozen calibration: `CCR_REF = 0.01766`, `BETA_CREDIT_LEVEL = -6.5`,
  `RHO_INV = 0.20`, `DELTA_CAPITAL = 0.10`, `INVESTMENT_TO_CAPITAL_RATIO = 0.11`,
  `CAPITAL_SHARE = 0.33`, `BASE_PRODUCTIVITY_TREND = 0.00825`.
  Module: `src/francescope/investment/financing_productivity.py`.

- **CORR-2 — Labor Market Hysteresis**
  Unemployment can remain above NAIRU (hysteresis gap), eroding the labor market and
  depressing the median living standard even after demand recovers. NAIRU is a persistent
  state updated from prior unemployment.

- **CORR-3 — Fiscal Drag**
  Debt servicing and automatic stabilisers impose an endogenous fiscal tightening
  (fiscal drag) measured relative to the baseline tax-ratio path, contributing a persistent
  real-economy drag distinct from the temporary consolidation impulse.

- **CORR-4 — External Structural Drag**
  A persistent external / de-globalization structural trend (competitiveness / import
  leakage) subtracts from demand, common across coherent paths and distinct from the
  i.i.d. external cycle shock.

### Official V4 MC1000 Results (2050 P50 Marginal Targets)

| Metric | V4 (2050 P50) | V3 pre-structural |
| --- | --- | --- |
| FranceScope Index V3 | **147.0** | 167.0 |
| Real GDP per capita | **0.0397** MEUR/person | 0.0429 |
| Unemployment rate | **7.89%** | 7.37% |
| NAIRU | **7.87%** | — |
| Median living standard | **€26,137** | €26,744 |
| Debt / GDP | **206.2%** | 192.0% |

The lower V4 Index (147.0 vs 167.0) reflects the four defensible, implemented structural
feedback channels above — not arbitrary pessimism.

### Representative Coherent Paths (frozen)

- **Path 470 — P10 (Stress / Lower bound)**
- **Path 386 — P50 (Central)**
- **Path 164 — P90 (Favorable / Upper bound)**

These are real selected simulation paths (full-horizon Index representativeness), not
synthetic marginal quantile envelopes. Legacy V3 path numbers (856 / 524 / 367) are
obsolete and MUST NOT be used.

### Frontend (Next.js)

- `app/forecast/page.tsx` and `app/scenarios/page.tsx` consume V4 official artifacts only
  (distributions, scenarios, historical index, methodology).
- New `components/CausalDiagnostics.tsx` exposes the four structural feedback channels
  (CORR-1 → CORR-4) across the three coherent paths with interactive charts and explanatory
  tooltips.
- Built data: `public/data/causal_diagnostics.json` (presentation-only conversion of the
  frozen V4 coherent-path trajectories).

### LLM Grounding Layer

- `lib/grounding.ts` system prompt embeds V4 official 2050 P50 figures, the coherent-path
  map (470 / 386 / 164), and the CORR-1 → CORR-4 causal channels as enforced guidance.
- `/api/explain` feeds `causal_diagnostics.json` into scenario/mixed contexts.

### Validation

- CORR-1 deterministic unit suite (`tests/test_corr1_financing_productivity.py`):
  **24/24 pass** — reference zero-gap, constant shocks (+100/+200/+300bp, +251bp),
  −100bp upside, and capital-healing recovery.
- `npm run build`: zero TypeScript / ESLint errors; all routes generate.

### DO NOT

- Do not re-run Monte Carlo (MC100 / MC1000) — the V4 MC1000 artifact is frozen.
- Do not modify V3 reference index, historical baseline statistics, simulation equations,
  parameters, or Next.js routes / LLM grounding configurations.

---

## Previous Versions

Pre-V4 history is preserved in the project memory and audit artifacts under
`data/audits/economic_system/` and `data/processed/v4/`.
