# FranceScope V4 — CORR-1 Implementation & Deterministic Validation

**Scope:** Implementation of the frozen CORR-1 contract + deterministic validation only.
No production recalibration; no MC100/MC1000; V2, unemployment, fiscal, external, climate, AI, Index unchanged.

## 1. Implementation
- New module `src/francescope/investment/financing_productivity.py` (pure, RNG-free) exposing:
  `compute_credit_rate_gap`, `compute_desired_investment_level_gap`, `update_investment_level_gap`,
  `update_capital_gap`, `compute_productivity_level_gap`, `compute_productivity_growth_deviation`, `step_corr1`.
- New persistent state in `V3PersistentState`: `investment_level_gap` and `capital_gap` (init 0.0 at 2026).
- New diagnostics in `V3YearResult`: `corporate_credit_rate_gap`, `desired_investment_level_gap`,
  `investment_level_gap`, `investment_growth_financing_contribution`, `capital_gap`,
  `productivity_level_gap`, `productivity_growth_dev_from_capital`.

## 2. Implemented equations (frozen contract)
```
credit_rate_gap_t       = corporate_credit_rate_t - CCR_REF          # CCR_REF = 0.01766
desired_inv_level_gap_t = BETA_CREDIT_LEVEL * credit_rate_gap_t      # -6.5 per +1pp, LEVEL
inv_level_gap_t         = RHO_INV*inv_level_gap_{t-1} + (1-RHO_INV)*desired   # RHO_INV = 0.20
capital_gap_t           = (1-DELTA)*capital_gap_{t-1} + (I/K)*inv_level_gap_t # DELTA=0.10, I/K=0.11
productivity_level_gap_t= ALPHA * capital_gap_t                       # ALPHA = 0.33
productivity_growth_dev_t = ALPHA * (capital_gap_t - capital_gap_{t-1})        # CORRECTED (was buggy alpha*I/K*inv)
labor_productivity_growth = 0.00825 + productivity_growth_dev_t
structural_gdp_growth = labor_force_growth + labor_productivity_growth + ai + climate
```
Corporate credit rate is the EXISTING V2 equation (coefficients untouched). CORR-1 is inserted after it,
before structural GDP, so its productivity effect enters the current-year GDP (and the Okun productivity term).
The diagnostic `investment_growth` keeps the V2 baseline plus `inv_level_gap_t - inv_level_gap_{t-1}`
(financing contribution); it is NOT re-fed into GDP (no double counting).

## 3. Reference-condition non-regression (mandatory)
With `corporate_credit_rate = CCR_REF`: desired gap = 0, `inv_level_gap` stays 0, `capital_gap` stays 0,
`productivity_growth_dev = 0`. Structural productivity = 0.00825 center exactly. The pre-CORR-1
deterministic trajectory is numerically identical under reference financing. **PASS.**

## 4. Dynamic + steady-state + recovery + upside tests
- +100/+200/+300bp match the authoritative diagnostics artifact (tolerances) for years 1,2,5,10,20.
- Steady state: `capital_gap_ss = (I/K/delta)*inv_gap_ss`; `prod_level_ss = ALPHA*capital_gap_ss`;
  `productivity_growth_dev -> 0`. **PASS.**
- +251bp: inv gap -> ~-16.3%, cap bounded, prod-level -> ~-5.9%, growth-dev -> 0. **PASS.**
- Recovery (5y +200bp then CCR_REF): gaps heal to ~0, growth-dev temporarily positive, level gap -> 0. **PASS.**
- Low-rate -100bp: symmetric positive gaps. **PASS.**

## 5. Deterministic 2030/2040/2050 comparison (diagnostics, NOT official forecasts)
| Scenario | 2050 cr | 2050 cap_gap | 2050 prod_level_gap | 2050 pgd | 2050 rGDP | 2050 debt |
|---|---|---|---|---|---|---|
| A reference (cr=CCR_REF) | 0.0177 | 0.0000 | 0.0000 | 0.00000 | 0.0021 | 197.4 |
| B current V3 financing | 0.0435 | -0.1602 | -0.0529 | -0.00089 | 0.0012 | 207.6 |
| C high financing (+200bp) | 0.0377 | -0.1313 | -0.0433 | -0.00043 | 0.0017 | 205.7 |

B shows the default French path already carries a ~+220–250bp financing gap; CORR-1 now transmits it
into a permanently lower capital/productivity LEVEL (≈ -5.3% by 2050) while the annual growth penalty
fades toward zero — resolving the prior debt↔productivity decoupling. All effects bounded.

## 6. Test suite
24 pytest functions (covering the 25 required checks) all PASS; existing `gdp` tests PASS (no regression).
Artifacts: `FRANCESCOPE_V4_CORR1_IMPLEMENTATION_TESTS.csv` (25 checks = PASS),
`FRANCESCOPE_V4_CORR1_DETERMINISTIC_VALIDATION.csv` (A/B/C × 2030/2040/2050).

## 7. Classification
**FRANCESCOPE V4 CORR-1 IMPLEMENTED AND VALIDATED — CORR1_IMPLEMENTATION_PASS**

## 8. Recommended next task
Run the V3 Monte Carlo (monte_carlo_v3.py / v1_orchestrator.py) with CORR-1 active to regenerate the
MC1000 distribution and validate Index/diagnostics; then re-verify the debt↔Index coupling and
reconcile against V3 official artifacts.
