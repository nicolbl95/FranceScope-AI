# FranceScope V3 — Current State Checkpoint

Date: 2026-08-23. Read-only checkpoint (no code modified).

## 1. Current Product Definition
FranceScope V3 has exactly THREE direct Index components:
1. `real_gdp_per_capita`
2. `median_living_standard_real`
3. `unemployment_rate`

NOT direct Index components (may remain engine/intermediate): `average_net_pension_real`,
`effective_retirement_age`, `poverty_rate`, `housing_cost_burden`, total `real_gdp`.

Strategy: keep the useful V2 macro engine; correct FIVE areas (demographics, GDP/structural-growth,
debt→spread→fiscal reaction, world/Europe/China contagion, climate persistence+disaster); add THREE
new mechanisms (macro_regime, global_financial_crisis, AI productivity/employment).

## 2. V2 Reusable Baseline (scripts/build_probabilistic_forecast_v2.py, 2284 lines)
Production/GDP, consumption, investment, productivity, unemployment, employment/participation,
wages/compensation, median living standard, inflation (headline/energy/food), ECB rate, OAT/sovereign
financing, household/corporate credit, public revenue/expenditure/deficit/debt/interest (stock-flow),
trade/foreign demand, energy/Brent, pensions/retirees, poverty, housing, Monte Carlo (seed 20260816,
horizon 2027-2050), scenario selection, diagnostics. Classified in the matrix CSV.

## 3. Completed V3 Work
- **Demographics (D1/D2/D3): COMPLETE.** D1 ingestion, D2 canonical panel, D3 structural driver all exist and pass tests.
- All 10 canonical demographic variables present; history 2000-2021 (HISTORICAL_COMMON), projection 2022-2070 (11 INSEE scenarios).

## 4. Five V3 Correction Status
| Item | Status | Note |
|------|--------|------|
| A. Demographics | EXISTS_SUFFICIENT | D1/D2/D3 done |
| B. GDP / structural-growth | IMPLEMENTED_FOUNDATION | structural-growth module done; macro_regime/crisis/AI + D5 labor_force upgrade pending |
| C. Debt→spread→fiscal reaction | IMPLEMENTED_FOUNDATION | V3 C2: incremental sovereign_fiscal_risk_premium (Arch B, no Bund), v3_france_oat, effective_debt_cost lag, fiscal_stress, lagged bounded reaction. Hooks exposed; GDP/median-living wiring + macro_regime/crisis/GFC still absent |
| D. World/Europe/China contagion | IMPLEMENTED_FOUNDATION | V3 D2 minimal contagion module (`src/francescope/external/contagion.py`): ONE common `external_cycle_shock` z -> global-growth dev / europe_factor / euro_area_growth / foreign_demand_growth / world_trade_growth / `external_cyclical_input = 0.008*z`. Pure deterministic, no random draws. China channel = IMPLEMENTED_HOOK (pending calibration, coefficient 0); `CHINA_COMPETITIVE_PRESSURE = DEFERRED` |
| E. Climate persistence + disaster | IMPLEMENTED_FOUNDATION | V3 E2 minimal two-channel climate module (`src/francescope/climate/climate_effects.py`): chronic `climate_structural_drag = -0.001` (V2-reused calibration) + acute `major_climate_disaster_shock` (default 0, one-year). Pure deterministic; no random draws. `CLIMATE_LONG_RUN_TREND_CALIBRATION_PENDING`; `CLIMATE_FISCAL_PRESSURE=DEFERRED` |

## 5. Three New V3 Mechanism Status
| Mechanism | Status |
|-----------|--------|
| A. macro_regime | IMPLEMENTED_FOUNDATION | V3 1B minimal deterministic module (`src/francescope/regime/macro_regime.py`): 5-state regime, base transition matrix, regularized regime_cyclical_input, 2026=SLOWDOWN. RNG deferred to orchestrator; transition modifiers not calibrated |
| B. global_financial_crisis | IMPLEMENTED_FOUNDATION |
| C. AI productivity/employment | IMPLEMENTED_FOUNDATION | V3 3B minimal deterministic module (`src/francescope/ai/ai_effects.py`): TWO channels (productivity `ai_productivity_effect`, employment `ai_employment_displacement_effect`). Central profiles fade to ~0 by 2050 (no permanent floor). Calibration MODEL_PRIOR/EXTERNAL_BENCHMARK_REQUIRED; RNG deferred to orchestrator |

## 6. Demographic D1/D2/D3 Status
- D1: `data/raw/insee/*.xlsx` (11 workbooks), `insee_population_by_age_sex.parquet`, `insee_demographic_annual_source.parquet/csv`.
- D2: `francescope_v3_demographic_canonical.parquet/csv` + metadata, validation, 2050 comparison, V2 compatibility, D3 contract CSVs.
- D3: `src/francescope/demographics/structural_driver.py` + tests (10/10 pass).
- D5A labor-force integration: **COMPLETE.** `src/francescope/gdp/labor_force.py` derives `labor_force = WAP × participation_rate` using the deterministic V2 LFPR AR(1) (mean ~80pp, 2026 anchor 81.5%). V3 GDP structural-growth module now consumes `labor_force_growth` (replacing the temporary WAP-growth proxy). Unemployment excluded from labor supply. Retiree/pension integration still pending (fiscal / median-living-standard work).

## 7. V3 Index Status
- Historical V2 Index: EXISTS (7-component scoring) — **LEGACY ONLY, unchanged**.
- V2 7-component scoring: EXISTS (legacy) in `compute_francescope_index` and `economic_index_freeze.py` CORE_VARIABLES — not modified.
- V3 3-component Index code: **IMPLEMENTED** in `src/francescope/index/v3_index.py` (pure deterministic scoring; no RNG, no file IO, no future-distribution dependence).
- V3 scoring methodology: **FROZEN** — legacy-style z-score; reference 2010–2019 (median center, sample SD ddof=1), base 100, 10 points/SD, equal 1/3 weights, directions (+1,+1,−1), RAW, NO CLIPPING, NO re-normalization. Provenance: `docs/FRANCESCOPE_V3_INDEX_SCORING_METHOD_EVALUATION.md`.
- **V3 HISTORICAL INDEX 2010–2026 = OFFICIAL** (`data/processed/index/francescope_v3_historical_index_2010_2026.csv` + `.parquet`). 25/25 validation tests PASS.
- **DISCREPANCY (non-blocking):** `economic_index_freeze.py` CORE_VARIABLES still lists 7 legacy components; align manifest to 3 before full V3 freeze — does not affect the frozen V3 method or official historical series.
- **AI_PRODUCTIVITY_SCALE_REVIEW = RESOLVED** (verification: implementation correct; prior 0.18% = mean-annual effect, not cumulative).
- **V3 OFFICIAL MC1000 = COMPLETE.** 1000 paths × 24 yrs = 24,000 rows; paths 0–99 bit-identical to corrected MC100 (max diff 0.0); future V3 Index computed RAW via frozen `v3_index.py`; MC1000 PASS.
- **V3 COHERENT PATH SELECTION = OFFICIAL (COHERENT_PATH_SELECTION_PASS).** Permanent mapping: P10_COHERENT_LOWER → path_id **856**; P50_COHERENT_CENTRAL → path_id **524**; P90_COHERENT_UPPER → path_id **367**. Exactly 72 scenario rows (3 paths × 24 yrs), 3 distinct paths, no NaN/inf, Index reconciliation exact, source rows exactly match MC1000, no synthetic/interpolated values. All three paths narrative-COHERENT. Crossing audit: LOWER≤CENTRAL≤UPPER at 2030/2040/2050 (1 within-band LOWER>CENTRAL Index overlap in 2030, expected). No selected path contains a GFC event (valid stochastic outcome, not an error). Non-monotonic AI amplitudes (P10 1.497 > P90 0.786) explained and retained. Report: `docs/FRANCESCOPE_V3_COHERENT_P10_P50_P90_PATHS.md`; audits: `FRANCESCOPE_V3_COHERENT_PATH_*`.

## 8. Optional / Deferred Mechanisms (OPTIONAL_LEGACY_SPEC)
Described in `docs/FRANCESCOPE_V3_SYSTEM_SPEC.md` and `economic_system_registry.py` (Blocks
TECHNOLOGY_AI_INNOVATION, GEOPOLITICS_DEFENCE): detailed banking, health/dependency, real estate,
pandemic, cyberattack, euro-FX standalone, political/institutional, detailed Chinese model, AI
inequality/rent, defense industry. NOT required to complete V3.

## 9. Exact Next Implementation Task
**V3 Correction C — debt→spread→fiscal reaction.** V3-C2 foundation is now **IMPLEMENTED_FOUNDATION** in a
new, separate module `src/francescope/fiscal/sovereign_fiscal.py` (21/21 tests pass; V2 engine untouched).
It implements the incremental `sovereign_fiscal_risk_premium` (Architecture B — V2 OAT baseline + premium,
NOT a France-Germany spread), `v3_france_oat`, lagged `effective_debt_cost`, `fiscal_stress`, and the
lagged/bounded fiscal reaction, exposing future hooks (`fiscal_spending_drag`, `tax_pressure_effect`,
`sovereign_financing_effect`, `sovereign_risk_shock=0.0`).
REMAINING C-work (not done this session, by strict scope):
- wire `fiscal_spending_drag` into GDP cyclical input;
- wire `tax_pressure_effect` into consumption / median living standard;
- implement macro_regime, sovereign-crisis event, and global_financial_crisis;
- connect `sovereign_risk_shock` to a crisis regime.
V3-B (structural-growth foundation) is IMPLEMENTED_FOUNDATION; full GDP architecture remains incomplete
(macro_regime, global_financial_crisis, explicit AI dynamics not yet implemented; D5 labor_force upgrade pending).

## 10. Roadmap to Completion
1. V3-B: structural-growth / potential-output GDP generation — **IMPLEMENTED_FOUNDATION**.
2. V3-C: debt→spread→fiscal reaction loop.
3. V3-D: Europe/China contagion channels.
4. V3-E: climate persistence + disaster dynamics.
5. V3-NEW-A/B/C: macro_regime, global_financial_crisis, AI productivity/employment.
6. D4: migration uncertainty (after genuine historical migration series obtained).
7. V3-INDEX: freeze 3-component scoring; fix `economic_index_freeze.py` discrepancy.

## 11. V3 Correction D2 — Minimal External Contagion Foundation (COMPLETE this session)
- New pure deterministic module: `src/francescope/external/contagion.py` (+ package `__init__.py`, tests `test_contagion.py`, 24/24 pass).
- Selected architecture A (spec §3) implemented EXACTLY: `external_cyclical_input = CYC_LOAD*z` with `CYC_LOAD=0.008`. z=-1 -> -0.008 -> -0.80pp.
- One common `external_cycle_shock` coherently drives: `global_growth_deviation` (0.018 + 0.006z), `europe_factor` (0.6·ggd + 0.006z), `euro_area_growth` (0.0126 + 0.3·ef), `foreign_demand_growth` (0.008819 + 0.907467·euro_area + CHINA_LOAD·china_gap), `world_trade_growth` (ggd + 0.006z).
- LEVEL vs DEVIATION: `global_growth_deviation` is a cyclical deviation only; it is NEVER fed into structural GDP. The sole external GDP channel is `external_cyclical_input` (-> `compose_real_gdp_growth(..., cyclical_input=...)`). Structural GDP remains domestic (labor_force_growth + productivity + AI).
- China channel = IMPLEMENTED_HOOK: `china_growth_gap` input + `compute_foreign_demand_growth` hook exist; active `CHINA_LOAD = 0.0` (no exact numeric value in spec) -> `CHINA_COEFFICIENT_PENDING_CALIBRATION = True`. `CHINA_COMPETITIVE_PRESSURE = DEFERRED` (no housing/debt/tariff/industrial submodel).
- V2 trade equations unchanged; module exposes `export_growth_diagnostic` (canonical ECM reproduced for diagnostics only, no mutation, no GDP feedback).
- GFC future interface: `global_financial_crisis_shock` (default 0) combined as `effective_external_shock = external_cycle_shock + gfc` on the SAME system. NOT implemented (no crisis prob/duration/regime).
- Validation artifact: `data/audits/economic_system/FRANCESCOPE_V3_EXTERNAL_CONTAGION_IMPLEMENTATION_VALIDATION.csv` (A/B/C/D). External columns reconcile EXACTLY with `FRANCESCOPE_V3_EXTERNAL_CONTAGION_DIAGNOSTICS.csv`. Case C foreign demand does not soften in the foundation because CHINA_LOAD is reserved=0 (the diagnostic's 0.01589 reflects a future calibrated coefficient, which the task forbids inventing).
- No GDP double-counting: external_cyclical_input (direct hook) and foreign_demand->export (trade layer) both derive from the SAME z; exports are NOT fed back into V3 GDP in this task.
- REMAINING D2/D-work: (a) actual global-financial-crisis mechanism absent; (b) macro_regime absent; (c) external hooks not yet integrated into a full V3 simulation orchestrator; (d) calibrate CHINA_LOAD from QNA.json when authorized.

## 12. V3 Correction E2 — Minimal Climate Foundation (COMPLETE this session)
- New pure deterministic module: `src/francescope/climate/climate_effects.py` (+ package `__init__.py`, tests `test_climate_effects.py`, 24/24 pass; existing gdp tests still pass, 48 total).
- Two channels implemented: `compute_climate_structural_drag(baseline_drag=-0.001, amplitude=1.0) -> -0.001`; `compute_major_climate_disaster_shock(disaster_shock=0.0) -> 0.0`. No random draws; `amplitude` is a future Monte-Carlo/path hook only (no time trend).
- `CLIMATE_LONG_RUN_TREND_CALIBRATION_PENDING = True` (no defensible climate->GDP trend elasticity in repo; architecture implemented, long-run amplitude may be benchmarked externally).
- Backward-compatible extension: `compute_structural_gdp_growth(..., climate_structural_drag=0.0)` now accepts the chronic term (default 0.0 preserves all prior callers/tests). Climate enters structural growth EXACTLY ONCE. `compose_real_gdp_growth` already carries `shock_input` for the disaster channel.
- Double-counting protected: oil/Brent, geopolitical, carbon_price/energy_inflation channels untouched and NOT relabeled as climate.
- Validation artifacts: `data/processed/forecasts/francescope_v3_climate_structural_baseline.csv` (2027–2050, all −0.001, status V2_REUSED_CALIBRATION_LONG_RUN_TREND_PENDING) and `data/audits/economic_system/FRANCESCOPE_V3_CLIMATE_IMPLEMENTATION_VALIDATION.csv` (A/B/C/D).
- ALL FIVE V2 CORRECTIONS NOW HAVE AN IMPLEMENTED FOUNDATION: (A) demographics, (B) GDP structural growth, (C) debt/sovereign/fiscal, (D) external contagion, (E) climate.
- REMAINING (do NOT mark full V3 complete): long-run climate trend calibration pending; climate fiscal pressure deferred; disaster probability/timing not implemented; future orchestrator will generate uncertainty/events and integrate all foundations; macro_regime, global_financial_crisis, AI productivity/employment still MISSING.

## 13. V3 New Mechanism 1B — Minimal Macro-Regime Foundation (COMPLETE this session)
- New pure deterministic module: `src/francescope/regime/macro_regime.py` (+ `__init__.py`, `tests/test_macro_regime.py`, 28/28 pass). No random draws; RNG belongs to the future orchestrator.
- `Regime` enum (EXPANSION/SLOWDOWN/RECESSION/CRISIS/RECOVERY); `INITIAL_REGIME_2026 = SLOWDOWN`.
- `transition_probabilities(current_regime, adjustments=None)` returns the exact validated base matrix (rows normalized to sum 1, no recalibration). Optional `adjustments` is an external-only modifier (default leaves base unchanged).
- `regime_cyclical_input(regime)` returns the regularized effects (EXP +0.0098, SLOW −0.0029, REC −0.0214, CRISIS −0.0364, RECOV +0.0186). Raw single-obs extremes (−0.0856 / +0.0584) are NOT used.
- `stationary_distribution()` reconciles to validated frequencies (EXP 0.395, SLOW 0.429, REC 0.049, CRISIS 0.071, RECOV 0.056); weighted cyclical mean ≈ 0 (no permanent trend).
- Acute severity kept separate: CRISIS regime (−0.0364) + hypothetical −0.03 GFC + hypothetical −0.005 climate disaster = arithmetic-only separation diagnostics.
- Validation: `data/audits/economic_system/FRANCESCOPE_V3_MACRO_REGIME_IMPLEMENTATION_VALIDATION.csv`.
- REMAINING: RNG not integrated; transition modifiers (external/fiscal/GFC/climate/sovereign) not calibrated; full V3 orchestrator absent; global_financial_crisis (B) and AI (C) still MISSING; unemployment integration deferred to Okun path.

## 14. V3 New Mechanism 2B — Minimal Global Financial Crisis Foundation (COMPLETE this session)
- New pure deterministic module: `src/francescope/gfc/global_financial_crisis.py` (+ package `__init__.py`, `tests/test_global_financial_crisis.py`, 33/33 pass). NO internal RNG; the future orchestrator owns all randomness.
- Constants (frozen spec): `GFC_ANNUAL_PROBABILITY = 0.03` (MODEL_PRIOR), `GFC_CENTRAL_SEVERITY = -3.0`, `GFC_EVENT_DURATION_YEARS = 1`, `GFC_REGIME_ADJUSTMENTS` = {EXP −0.45, SLOW −0.30, REC +0.30, CRIS +0.35, RECOV −0.10}, `DIRECT_SOVEREIGN_RISK_SHOCK = 0.0`, `GFC_CREDIT_CHANNEL = "DEFERRED_TO_INTEGRATION"`. Reuses the existing `Regime` enum (no redefinition).
- `gfc_probability(p=0.03)` validates 0<=p<=1, default 0.03; no fiscal-stress modifier.
- `gfc_external_shock(triggered)` -> 0.0 / −3.0; `gfc_external_contagion` reuses the EXISTING external module (`apply_external_contagion`), so the single −0.024 GDP effect is produced once, by the external module — NOT duplicated inside GFC.
- `gfc_regime_adjustments(triggered)` -> None (base unchanged) when not triggered, else the frozen additive vector; applied via `R.transition_probabilities(current, adjustments=...)`. Base matrix never copied.
- `gfc_trigger_from_uniform_draw(u, p)` deterministic (u < p); boundary u==p not triggered.
- `gfc_sovereign_risk_shock` always 0.0; French sovereign stress endogenous later via GDP/debt.
- Acute vs persistent kept separate: trigger year delivers z=−3 (external_cyclical_input −0.024) AND adverse next-regime probabilities; following year acute external = 0 (orchestrator re-draws), persistence only via macro_regime (CRISIS −0.0364). Verified by two-year diagnostic (year T −0.02121, year T+1 −0.03071; −0.024 not repeated).
- Hazard analytics reconcile: 24y expected 0.72, P0 0.481, P>=1 0.519, P>=2 0.162.
- Validation artifact: `data/audits/economic_system/FRANCESCOPE_V3_GFC_IMPLEMENTATION_VALIDATION.csv` (hazard, severity, 5 transition rows, A/B/C/D, two-year separation).
- REMAINDER (do NOT mark full V3 complete): RNG integration (orchestrator draws u) pending; credit channel deferred; no direct sovereign-risk shock; AI mechanism (C) still MISSING; full V3 orchestrator absent; GFC module not yet wired into a simulation year.

## 15. V3 New Mechanism 3B — Minimal AI Productivity/Employment Foundation (COMPLETE this session)
- New pure deterministic module: `src/francescope/ai/ai_effects.py` (+ package `__init__.py`, `tests/test_ai_effects.py`, 38/38 pass). NO internal RNG; the future orchestrator owns all randomness (path-level amplitudes).
- Exactly TWO direct channels: (A) `ai_productivity_effect(year, amplitude=1.0)` (decimal annual real-GDP/productivity-growth contribution) entering structural GDP via the EXISTING `compute_structural_gdp_growth(..., ai_productivity_effect=...)` hook exactly once; (B) `ai_employment_displacement_effect(year, amplitude=1.0)` (decimal annual pp contribution to unemployment-rate change; 0.00100 = +0.10pp) exposed for LATER unemployment wiring only. Channels kept strictly distinct (no double counting).
- Central profiles (frozen, authoritative AI spec/diagnostics): productivity peaks ~2035 (0.0033) and fades to ~0.00002 by 2050; employment peaks ~2035 (0.00100) and fades to ~0.000001 by 2050. NO permanent productivity-growth floor and NO permanent technological-unemployment assumption.
- `ai_cumulative_productivity_level_gain(start, end, amplitude)` compounds Π(1+effect_t)−1: central 2030 ≈ +0.53%, 2040 ≈ +3.41%, 2050 ≈ +3.93% (level gain persists; annual fades).
- Diagnostic cases (exact amplitudes): A no-AI (0,0); B central (1,1); C weaker (0.45,0.5) peak prod≈0.00149 / emp≈0.00050; D stronger (1.7,1.8) peak prod≈0.00561 / emp≈0.00180.
- Calibration: `AI_PRODUCTIVITY_CALIBRATION_STATUS` / `AI_EMPLOYMENT_CALIBRATION_STATUS` = MODEL_PRIOR/EXTERNAL_BENCHMARK_REQUIRED (no historical French GenAI data in repo); `AI_PRODUCTIVITY_AMPLITUDE_DISTRIBUTION_PENDING = True`.
- Contracts: `AI_GFC_MODIFIER_CALIBRATION = "DEFERRED"` (current AI→GFC contribution = 0; no AI crash engine); `AI_REGIME_DIRECT_EFFECT = "DEFERRED"` (current AI→regime transition = 0). V2 engine, macro_regime, GFC, fiscal/external/climate/demographics, unemployment, median-living, Index all UNCHANGED.
- Central diagnostic path: `data/processed/forecasts/francescope_v3_ai_central_profile.csv` (2027–2050). Validation artifact: `data/audits/economic_system/FRANCESCOPE_V3_AI_IMPLEMENTATION_VALIDATION.csv`.
- **ALL STANDALONE V3 FOUNDATION MECHANISMS NOW IMPLEMENTED** (A–E corrections, macro_regime, GFC, AI). Do NOT mark full V3 complete: remaining work is INTEGRATION (V3 simulation orchestrator, unemployment integration, median-living-standard integration, fiscal/external/climate/regime/GFC hook wiring, RNG orchestration, stress tests, 100-path dev Monte Carlo, V3 Index implementation/scoring, 1,000-path official simulation).

## 16. V3 Core Orchestrator V1 — Deterministic Annual Loop (COMPLETE this session)
- New package `src/francescope/orchestrator/` (`__init__.py`, `v1_orchestrator.py`; `tests/test_v1_orchestrator.py`, **29/29 pass**). No Monte Carlo; all draws caller-supplied.
- Integrates ALL foundations in one year-by-year loop following the integration contract exactly: fiscal start (lagged stress→adjustment; premium AR(1); OAT = baseline+premium; lagged effective debt cost; adjusted fiscal ratios) → AI/climate profiles → GFC trigger (caller draw) → external contagion (GFC shock inside z) → regime_cyclical_input(current) → structural GDP (labor+prod trend+AI+climate drag) → total (cyclical=regime+external; shock=climate disaster) → real_gdp level → unemployment (Okun + AI displacement) → median living (reduced form) → fiscal end (deficit/debt/interest/stress) → next regime.
- 2026 anchors from V2 `state_2026` / resolved panel (real_gdp 2,663,693.5 MEUR; unemployment 0.081; median_living 25,848.70; debt 119.45%; deficit 5.48%; OAT 0.0385; regime=SLOWDOWN).
- V2 equations reproduced exactly as adapters (unemployment Okun, median living, real_wage=0.7*prod, debt stock-flow); V2 engine NOT imported/modified.
- Validation: `data/processed/forecasts/francescope_v3_orchestrator_v1_validation_path.csv` (2027–2050); `data/audits/economic_system/FRANCESCOPE_V3_ORCHESTRATOR_V1_VALIDATION.csv`.
- **V3 core orchestrator = IMPLEMENTED_V1.** Do NOT mark full V3 complete. Remaining: integrated deterministic stress tests; RNG/distribution calibration (AI amp, climate disaster, external z, China load); 100-path development Monte Carlo; distribution audit; V3 Index scoring freeze; 1,000-path official simulation; P10/P50/P90 selection; final human audit; institutional benchmark; frontend/explanatory AI.
- Nonblocking: fiscal→GDP (V3 growth uses structural+cyclical; fiscal states computed, not added as separate drag — no invented coefficient); inflation for debt nominal growth carried as constant 0.02.

## Artifacts
- `docs/FRANCESCOPE_V3_CURRENT_STATE_CHECKPOINT.md` (this file)
- `data/audits/economic_system/FRANCESCOPE_V3_CURRENT_STATE_MATRIX.csv` (33 rows)
