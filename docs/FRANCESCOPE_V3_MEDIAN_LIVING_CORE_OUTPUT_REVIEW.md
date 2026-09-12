# FRANCESCOPE V3 — Median-Living-Standard Core Output Review

## Status
**RESOLVED — IMPLEMENTED.** The unemployment LEVEL specification was replaced by a
decimal-unemployment GAP in the frozen C1 model; legacy V2 source is untouched.

## 1. Exact current equation (V3 active recurrence)
Lives in `src/francescope/orchestrator/v1_orchestrator.py`, `_v3_median_living`:

```
growth = 0.00009
       + 0.2880 * gdp_growth
       - 0.0078 * (unemployment_rate - 0.075)
median_living_t = median_living_{t-1} * (1 + growth)
```
`unemployment_rate` is **decimal** (0.08 = 8%); gap = u − 0.075. No direct
productivity or real-wage term. The old `_v2_median_living` (0.6/0.4/0.3/−0.2
level) is permanently removed from the active V3 path.

## 2. Origin / calibration of coefficients
Round numbers (0.6/0.4/0.3/0.2), no docstring estimation period, no dependent/
independent variable documentation → **inherited heuristic / reduced-form**, NOT
historically estimated from French data.

## 3. Exact units of all inputs
- `gdp_growth`, `productivity_growth`, `real_wage_growth`, `growth`: **decimal
  growth rates** (0.01 = 1%).
- `unemployment_rate`: **decimal rate level** (0.08 = 8%), NOT a change/gap,
  NOT percentage points in the numerator sense (the coefficient already scales it).
- `median_living`: EUR level; recurrence multiplies previous level by (1+growth).

## 4. Exact meaning of the unemployment input
V2 passes `state["unemployment_rate"]` (decimal LEVEL). So `-0.2 * unemployment`
multiplies the **decimal rate level**. Intended use (relative to V2's own design)
is the level — this is therefore NOT a unit/variable mismatch vs V2. The problem
is the *specification*, not the unit.

## 5. Historical backtest (2010–2026)
Source: `data/modeling/economic_index/francescope_full_table_2010_2026.csv`
(actual `real_gdp`, `unemployment_rate`, `median_living_standard_real`).
`real_wage_growth` reconstructed as `0.7 * productivity_growth` (V2/V3 internal
definition — NOT from `compensation_per_employee`, which is **nominal**).
- n = 16
- mean actual median growth = **+0.0054** (+0.54%/yr)
- mean predicted growth (prod=0.00825) = **−1.7466** (−1.75%/yr)
- mean predicted growth (prod=0.015, V2 calib) = **−1.7425** (−1.74%/yr)
- mean unemployment ≈ 8.79% → annual unemployment drag ≈ **−1.76pp/yr**
- cumulative actual median change 2010→2026 = **+8.8%**
Model under-predicts actual by ~**2.3pp/yr**; compounding error is enormous.

## 6. Stable-unemployment diagnostic
LEVEL spec gives a permanent annual penalty for ANY positive unemployment:
- u = 5% → −1.00pp/yr; u = 8% → −1.60pp/yr; u = 10% → −2.00pp/yr.
GAP spec (reference 0.075, used elsewhere in V2): u=8% → −0.10pp/yr; u=5% → +0.50pp/yr.
The level term is the defect.

## 7. V3 2027/2030/2040/2050 decomposition (control, deterministic)
| year | gdp | prod | realwage | unemp | net | median |
|------|-----|------|----------|-------|-----|--------|
| 2027 | -0.0003 | 0.0033 | 0.0017 | -0.0161 | -0.0113 | 25,563 |
| 2030 | 0.0017 | 0.0033 | 0.0017 | -0.0157 | -0.0090 | 24,906 |
| 2040 | 0.0025 | 0.0033 | 0.0017 | -0.0154 | -0.0079 | 23,473 |
| 2050 | 0.0013 | 0.0033 | 0.0017 | -0.0151 | -0.0088 | 21,591 |
The unemployment term dominates and is permanently negative → median living
falls while real GDP per capita rises.

## 8. Constant-economy sanity
gdp=prod=rw=0, u=8% → growth = **−0.016/yr forever**. A stationary economy
shrinks perpetually solely because unemployment is nonzero. Flagged.

## 9. Double-counting
Unemployment reaches median living via (a) Okun → GDP → 0.6 term AND (b) the
direct −0.2 level term. The direct term is the dominant, problematic channel.
Also `real_wage = 0.7*productivity`, so productivity enters via 0.4 and
0.3*0.7 = 0.21 (total 0.61) — benign redundancy. No removal recommended now.

## 10. Pensions / transfers / taxes
Adding negative household-income channels would worsen an already-too-negative
model. The defect is internal (unemployment spec), not missing channels.
**CURRENT_REDUCED_FORM_SUFFICIENT** (fix is internal).

## 11. Classification
**C. ECONOMIC_MODEL_REVIEW_REQUIRED** (units correct; level spec indefensible).

## 12. Smallest defensible next task
Replace the unemployment **LEVEL** term with a **GAP**:
`growth -= 0.2 * (unemployment_rate - 0.075)` (0.075 = V2 natural rate, already
used in `_v2_unemployment` and the poverty equation). Same coefficient sign and
4-variable structure; re-run the backtest. If the gap still misfits, re-estimate
the reduced form with the same four variables (no new variables).

## 13. Credit→investment
Unchanged: OAT→credit = PASS; credit→investment = FAIL_NOT_WIRED.

## 14. Files
Created: `docs/FRANCESCOPE_V3_MEDIAN_LIVING_CORE_OUTPUT_REVIEW.md`,
`data/audits/economic_system/FRANCESCOPE_V3_MEDIAN_LIVING_HISTORICAL_BACKTEST.csv`,
`data/audits/economic_system/FRANCESCOPE_V3_MEDIAN_LIVING_DRIVER_DECOMPOSITION.csv`,
`data/audits/economic_system/FRANCESCOPE_V3_MEDIAN_LIVING_MODEL_REVIEW.csv`,
`scripts/v3_median_living_review.py`. Updated: `FRANCESCOPE_V3_PRE_MONTE_CARLO_BLOCKERS.csv`.
No model code modified.
