# FranceScope V3 — Integration Contract & Orchestrator Checkpoint

Date: 2026-08-23. SPECIFICATION / WIRING AUDIT ONLY. No code implemented.

## 1. Authoritative annual execution order (single path, year t = 2027..2050)

`S` = persistent state carried from t-1 (init at 2026 anchors).

0. **Init (once)**: S = {regime=SLOWDOWN, real_gdp, unemployment, median_living, debt_gdp, deficit_gdp, interest_burden, premium=0, oat=v2_baseline, adjustment=0, stress=0}.
1. Demographic/labor inputs for t: `labor_force_growth`, `total_population` (D3/labor_force).
2. Deterministic AI profiles: `ai_productivity_effect(t, amp)`, `ai_employment_displacement_effect(t, amp)`.
3. Climate: `climate_structural_drag(t)` (chronic ≈ -0.001) and `major_climate_disaster_shock(t)` (acute, default 0).
4. **Orchestrator RNG draws for t**: external_cycle_shock `z`, GFC trigger `u_gfc`, climate disaster draw, AI `amp`. (All owner = orchestrator.)
5. GFC: `triggered = gfc_trigger_from_uniform_draw(u_gfc, 0.03)`; if triggered, `gfc_external_shock` (z=-3) becomes `global_financial_crisis_shock`; capture `gfc_regime_adjustments(triggered)` for step 15.
6. External acute: `apply_external_contagion(z, global_financial_crisis_shock)` → `external_cyclical_input`, foreign_demand, etc. (GFC shock already inside z.)
7. **Fiscal start (uses t-1 state)**: `adjustment_t = compute_fiscal_adjustment(adjustment_{t-1}, stress_{t-1})`; `target = compute_target_sovereign_premium(debt_{t-1}, deficit_{t-1}, interest_{t-1})`; `premium_t = AR(1)`; `oat_t = compose_v3_france_oat(v2_oat_baseline, premium_t)`; `effective_debt_cost_t = compute_effective_debt_cost(oat_{t-1})` (lag); `adjusted = apply_fiscal_reaction(baseline_primary, baseline_revenue, adjustment_t)`. Feed `adjusted` into V2 government-consumption/GDP and `oat_t` into V2 credit/investment.
8. Regime (carried `current_regime`): `regime_cyclical_input(current_regime)` = persistent GDP contribution for year t.
9. Structural GDP: `compute_structural_gdp_growth(labor_force_growth, LABOR_PRODUCTIVITY_TREND, ai_productivity_effect, climate_structural_drag)`.
10. Total GDP: `compose_real_gdp_growth(structural, cyclical_input = regime_cyclical_input + external_cyclical_input, shock_input = climate_disaster_shock)`.
11. Update level: `next_real_gdp(real_gdp_{t-1}, total)`.
12. Unemployment: `compute_unemployment_rate(unemp_{t-1}, total, productivity_growth) + ai_employment_displacement_effect(t, amp)` (productivity_growth = trend + AI; both decimal pp).
13. Median living: `compute_median_living_standard(prev, total, productivity_growth, real_wage_growth, unemployment)` (real_wage from V2 wage eq).
14. Fiscal end: update deficit_t, debt_t, interest_burden_t from GDP + effective_debt_cost_t; `stress_t = compute_fiscal_stress(debt_t, deficit_t, interest_t, premium_t)` (for t+1 adjustment).
15. **Next regime**: `probs =... ; trans = transition_probabilities(current_regime, adjustments=gfc_regime_adjustments)`; `next_regime = regime_from_uniform_draw(trans, u_regime)`; persist.
16. Emit three components + diagnostics; persist S.

## 2. Module/API wiring summary
- GDP: structural_growth (ai_productivity_effect hook) + regime_cyclical_input + external_cyclical_input + climate disaster shock.
- External: single `external_cyclical_input` hook; GFC shock enters via same z.
- GFC: trigger (u vs 0.03) → external shock (-3) + regime transition adjustments; sovereign shock = 0; credit DEFERRED.
- AI: productivity → structural GDP; displacement → unemployment delta.
- Fiscal: premium/OAT/debt-cost/adjustment hooks; transmitted via EXISTING V2 gov-consumption & credit equations (no new coefficient).
- Climate: chronic drag → structural; disaster → shock_input.

## 3. READY_TO_WIRE connections
labor_force_growth→structural GDP; AI productivity→structural GDP; climate drag→structural GDP; regime→cyclical input; external→cyclical input; GFC→external shock; GFC→regime transition; climate disaster→shock input; sovereign premium/OAT→V2 credit/investment; fiscal adjusted ratios→V2 gov consumption.

## 4. True NUMERIC_LINK_MISSING blockers
**NONE for the three core outputs.** All three (real_gdp, unemployment, median_living) are producible with existing identities/transmissions. No new fiscal multiplier or AI-unemployment coefficient is required. Remaining items are integration-wiring/anchor tasks (see §15), not missing calibrated coefficients.

## 5. Minimal unemployment V3 contract
Reuse V2 `compute_unemployment_rate(current, gdp_growth, productivity_growth)`, decimal rate (0.075=7.5% anchor), Okun -0.2, prod +0.05, mean-revert 0.075, soft floor. Add `ai_employment_displacement_effect(t, amp)` directly as a decimal-pp delta. No regime→unemployment direct shock (cycle transmits via GDP/Okun). 2026 anchor required.

## 6. Minimal median-living V3 contract
Reuse V2 `compute_median_living_standard(current, gdp_growth, productivity_growth, real_wage_growth, unemployment)`: `growth = 0.6*gdp +0.4*prod +0.3*real_wage -0.2*unemp`. Uses existing V3 inputs only; no microsimulation; pensions/transfers DEFER.

## 7. Fiscal integration architecture
Do NOT add a separate `fiscal_spending_drag` coefficient. Feed `apply_fiscal_reaction` adjusted primary/revenue into the EXISTING V2 government-consumption/expenditure and household-consumption equations. Avoids double counting (tightening already in endogenous expenditure/revenue).

## 8. Sovereign financing integration architecture
`v3_france_oat` and `effective_debt_cost` feed EXISTING V2 mortgage_rate/corporate-credit/investment equations (already calibrated to OAT). READY_WITH_EXISTING_V2_TRANSMISSION. No banking model.

## 9. RNG ownership map (orchestrator owns all draws)
- macro-regime transition draw `u_regime`: CALIBRATED (probs validated).
- GFC trigger `u_gfc` vs p=0.03: CALIBRATED.
- external_cycle_shock `z`: MODEL_PRIOR (loadings fixed; z distribution PENDING).
- climate disaster / amplitude draw: PENDING.
- AI amplitude `amp`: PENDING (AI_PRODUCTIVITY_AMPLITUDE_DISTRIBUTION_PENDING).
- V2 residual innovations (housing AR(1) etc.): CALIBRATED (fixed sigma).

## 10. Minimum persistent state vector
PERSISTENT: year, regime, real_gdp_level, unemployment_rate, median_living_standard_real, debt_gdp, deficit_gdp, interest_burden, sovereign_premium, france_oat, fiscal_adjustment. (fiscal_stress, effective_debt_cost, adjusted ratios, population, all growth components, three outputs = YEARLY_DERIVED.)

## 11. Minimum V2 equations still required
REQUIRED_FOR_CORE_V3: compute_unemployment_rate, compute_median_living_standard, V2 consumption/investment/government-expenditure & GDP identity, wage/compensation (real_wage), ECB, credit (mortgage/corporate), inflation, trade/foreign-demand, revenue/expenditure baselines. REQUIRED_LATER: pensions, poverty, housing. LEGACY_NOT_NEEDED_FIRST: detailed banking/health/defense/cyber.

## 12. Three FranceScope output contracts
- real_gdp_per_capita = real_gdp_level / total_population.
- unemployment_rate = V3 unemployment recurrence (§5).
- median_living_standard_real = V2 recurrence (§6).
Only these three are direct Index components. Index scoring NOT implemented (V3_INDEX_IMPLEMENTATION=PENDING, V3_SCORING_METHOD=NOT_FROZEN; legacy 7-comp code unchanged, not a blocker).

## 13. Minimum first orchestrator scope (V1)
One deterministic (later Monte-Carlo) path 2027–2050 producing, each year, the ordered steps above, emitting real_gdp, unemployment, median_living + diagnostics. Reuse V2 equations. Secondary P0 outputs added only after core loop stable.

## 14. Exact next task
Implement the V1 orchestrator loop per §1, using 2026 state anchors (§15 B1) and wiring fiscal (B2) and AI-displacement (B3) into existing V2 recurrences. No new coefficients.

## 15. Integration blockers (max 5; none are new coefficients)
- B1 — 2026 state anchoring (initial unemployment, median_living, debt_gdp, deficit_gdp, interest_burden, OAT baseline, premium=0, regime=SLOWDOWN). Missing: initial numeric state. Why: orchestrator cannot start year-1 without t-1. Evidence: V2 2026 actuals in repo; INITIAL_REGIME_2026=SLOWDOWN. Next: extract 2026 anchors, pass as initial S. (Anchor task, not a new coefficient.)
- B2 — Fiscal adjustment → V2 gov expenditure/consumption wiring. Missing: connection of `apply_fiscal_reaction` adjusted ratios into V2 GDP government consumption. Why: fiscal→GDP transmission without double counting. Evidence: V2 gov consumption already in GDP; `apply_fiscal_reaction` returns adjusted ratios. Next: replace baseline fiscal ratios with adjusted before V2 gov consumption. (READY_WITH_EXISTING_V2_TRANSMISSION.)
- B3 — AI displacement → V2 unemployment recurrence wiring. Missing: add `ai_employment_displacement_effect(t, amp)` delta into `compute_unemployment_rate` step. Why: AI employment channel. Evidence: identical decimal-pp unit. Next: add one line in unemployment update. (READY_WITH_EXISTING_IDENTITY.)

All three are wiring/anchor tasks; no NUMERIC_LINK_MISSING coefficient gap for the core outputs.

## Artifacts
- docs/FRANCESCOPE_V3_INTEGRATION_CONTRACT.md (this file)
- data/audits/economic_system/FRANCESCOPE_V3_INTEGRATION_WIRING_MATRIX.csv
- data/audits/economic_system/FRANCESCOPE_V3_ORCHESTRATOR_STATE_REGISTAN.csv
- data/audits/economic_system/FRANCESCOPE_V3_INTEGRATION_BLOCKERS.csv
