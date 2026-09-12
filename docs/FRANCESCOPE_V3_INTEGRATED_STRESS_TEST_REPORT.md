# FranceScope V3 — Integrated Deterministic Stress Test Report

Date 2026-08-23. Diagnostic only; no model code modified. Counterfactual pairs vs CONTROL_NOT_FORECAST.

## A. Regime transmission
Forced SLOWDOWN->RECESSION->RECOVERY via regime draws (0.95). 2030: real_gdp_growth lower, unemployment higher, median living weaker, debt higher vs control. Chain confirmed: adverse regime -> GDP down -> unemployment up -> median weaker -> fiscal weaker. No direct regime->unemployment effect added.

## B. External slowdown
Negative external_cycle_shock (-1.0) in 2031-2033. external_cyclical_input falls to -0.008; GDP growth, median living lower; unemployment higher. No second trade-to-GDP channel.

## C. GFC
Trigger 2030 (gfc_uniform_draw=0). external_cyclical_input = -0.024 (z=-3). Next-regime probabilities shifted adverse. Year+1 acute effect = 0 (verified). 1/3/5-yr cumulative: real GDP, per-capita, median living lower; unemployment/debt higher. No double counting.

## D. Climate disaster
major_climate_disaster_shock=-0.005 in 2030 only. Trigger-year GDP growth lower by exactly -0.005 (acute); next year disaster input = 0. Downstream unemployment/median/debt mildly weaker.

## E. AI (Case D amps 1.7/1.8)
Higher AI raises AI productivity effect, structural GDP, GDP/capita. AI displacement higher -> temporary unemployment pressure. Both fade toward ~0 by 2050. Net unemployment mixed (productivity->Okun offsets some displacement).

## F. Fiscal / sovereign stress
Initial debt160/deficit8/interest5. Premium, OAT, effective debt cost, stress, adjustment ALL higher than control. BUT real_gdp_growth and median_living IDENTICAL to control -> fiscal stress currently NOT transmitted to real economy. Marked FISCAL_TO_REAL_ECONOMY_INTEGRATION_GAP. No new coefficient: reuse V2 gov-consumption/household-consumption.

## G. Sovereign financing -> credit/investment
SOVEREIGN_FINANCING_TO_REAL_ECONOMY_NOT_YET_WIRED. Orchestrator computes OAT/effective debt cost but does NOT simulate mortgage/corporate credit or investment. Connection not wired.

## H. Combined systemic stress
GFC + high fiscal stress + adverse regime. All outputs finite, no NaN/inf, no explosion, no duplicate acute GFC, debt feedback active, fiscal adjustment bounded (<0.8). Robust.

## I. Median-living decomposition
Terms (e.g. 2030): gdp*0.6approx+0.0019, prod*0.4approx+0.0035, rw*0.3approx+0.0018, unemp*0.2approx-0.0156 -> net approx -0.0084. The -0.2*unemployment weight dominates because unemployment (~8%) is large vs low growth. Verdict: EXPECTED_FROM_EXISTING_FORMULA (reduced form under persistently high unemployment). Flagged for economic-model review, not a unit error.

## J. Debt decomposition
119.45% (2026) -> 196.4% (2050). debt_t = prev/(1+nominal) + deficit; nominal = gdp_growth+0.02(constant). With ~5.6% deficits and ~2% nominal growth, debt rises mechanically. Verdict: ACCOUNTINGALLY_EXPECTED_GIVEN_INPUTS (no real-economy feedback, constant inflation). Not an identity error.

## Transmission matrix summary
PASS: regime->GDP, GDP->unemp, GDP/unemp->median, external->GDP, GFC->external, GFC->regime, climate->GDP, AI->GDP, AI->unemp, fiscal stress->adjustment, premium->OAT, OAT->eff debt cost, debt/deficit/interest->premium. FAIL_NOT_WIRED: fiscal adjustment->GDP, fiscal adjustment->median, OAT->credit, credit->investment, investment->GDP. PARTIAL: GDP->deficit/debt.

## Pre-Monte-Carlo blockers (max 5)
B1 fiscal adjustment -> real economy NOT WIRED (Test F). B2 sovereign financing -> credit/investment NOT WIRED (Test G). Both closeable with EXISTING V2 equations, no new calibration. Median-living drift (I) and debt rise (J) are EXPECTED, not blockers.

## Artifacts
- docs/FRANCESCOPE_V3_INTEGRATED_STRESS_TEST_REPORT.md
- data/audits/economic_system/FRANCESCOPE_V3_INTEGRATED_STRESS_RESULTS.csv
- data/audits/economic_system/FRANCESCOPE_V3_TRANSMISSION_VALIDATION_MATRIX.csv
- data/audits/economic_system/FRANCESCOPE_V3_PRE_MONTE_CARLO_BLOCKERS.csv
