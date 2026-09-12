# FranceScope V3 — Orchestrator V1 (Deterministic Core Loop)

Date: 2026-08-23. Implements the integration contract as a deterministic year-by-year loop. No Monte Carlo; all stochastic/exogenous draws are caller-supplied.

## Package
`src/francescope/orchestrator/` — `__init__.py`, `v1_orchestrator.py` (+ `tests/test_v1_orchestrator.py`, 29/29 pass).

## API
- `load_2026_state()` — authoritative 2026 anchors.
- `V3PersistentState` — year, regime, real_gdp_level, unemployment_rate, median_living_standard_real, debt_gdp, deficit_gdp, interest_burden, sovereign_premium, france_oat, fiscal_adjustment (+ baseline fiscal ratios, inflation).
- `V3YearInputs` — external_cycle_shock, gfc_uniform_draw, regime_uniform_draw, climate_amplitude, major_climate_disaster_shock, ai_productivity_amplitude, ai_employment_displacement_amplitude.
- `simulate_year(prev, inputs, year, ctx)` -> `(V3YearResult, next_state)`.
- `simulate_path(initial, yearly_inputs, start, end)` -> list[V3YearResult].

## 2026 anchors (sources)
real_gdp 2,663,693.5 MEUR; unemployment 8.1%→0.081; median_living 25,848.70 EUR (resolved panel). debt 119.45%, deficit 5.48%, interest 3.01%, premium 0, OAT 0.0385, adjustment 0, baseline primary 54.97%, revenue 52.50% (V2 `state_2026`). regime = SLOWDOWN.

## Year-t order (per integration contract)
fiscal start (lagged stress→adjustment; premium AR(1); OAT; lagged effective debt cost; adjusted fiscal ratios) → AI/climate profiles → GFC trigger (caller draw) → external contagion (GFC shock inside z) → regime_cyclical_input(current) → structural GDP (labor+prod trend+AI+climate drag) → total (cyclical=regime+external; shock=climate disaster) → real_gdp level → unemployment (Okun + AI displacement) → median living (reduced form) → fiscal end (deficit/debt/interest/stress) → next regime (transition+GFC adj, caller draw).

## Reused V2 equations (exact adapters, no V2 import)
unemployment Okun (-0.2 gdp +0.05 prod + mean-revert 0.075, floor); median living (0.6 gdp+0.4 prod+0.3 real_wage−0.2 unemp); real_wage=0.7*prod; debt stock-flow.

## Nonblocking gaps
- Fiscal→GDP: V3 growth uses structural+cyclical; fiscal premium/OAT/debt states computed but NOT added as a separate GDP drag (no invented coefficient). Deferred integration refinement.
- Inflation for debt nominal growth carried as constant 0.02 (secondary).
- China load / climate disaster timing / AI amplitude distributions = DEFERRED (caller supplies realized values).

## Outputs
`data/processed/forecasts/francescope_v3_orchestrator_v1_validation_path.csv`; `data/audits/economic_system/FRANCESCOPE_V3_ORCHESTRATOR_V1_VALIDATION.csv`. V3 Index scoring NOT implemented.

## Status
V3 core orchestrator = IMPLEMENTED_V1. Remaining: integrated stress tests, RNG/distribution calibration, 100-path dev Monte Carlo, Index scoring freeze, 1,000-path official simulation.
