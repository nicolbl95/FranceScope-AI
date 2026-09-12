# FranceScope V4 — CORR-1C Final Data + State-Equation Consistency Gate

**Scope:** Calibration gate only. No production code modified; no MC/MC1000; no forecast; no change to unemployment/fiscal/external/Index.

## 1. Data retrieval
- Route used: **Eurostat SDMX 2.1 JSONSTAT, full-dataset download then local filter** (query-string filters are ignored by this endpoint; path-key and SDMX 3.0 returned 400/404). Sanctioned "downloadable dataset file then filter locally" route.
- Source A — `nama_10_gdp`: France (FR), `P51G`, `CLV10_MEUR` (chain-linked 2010, real, MEUR). Coverage 1975–2025.
- Source B — `nama_10_lp_ulc`: France (FR), `RLPR_PER` (real productivity per person) and `RLPR_HW` (per hour), `I10` index. Coverage 1975–2025.
- Files: `data/external/corr1/france_real_gfcf.csv`, `france_labour_productivity.csv`, `france_labour_productivity_perhour.csv`.

## 2. Productivity center check
- Per person (RLPR_PER) 2011–2019 arithmetic mean = **0.006495** (sensitivity).
- Per hour (RLPR_HW) 2011–2019 arithmetic mean = **0.00825** — exact match to the V3 center. V3 historical concept = per-hour productivity.
- Verdict: **OLD_CENTER_CONFIRMED** (per-hour basis, exact). Per-person retained as sensitivity only.

## 3. Real GFCF history
- Coverage 1976–2025 (real growth). 2011–2019 mean real growth = **+1.73%**.
- 2020 −5.83% (COVID), 2021 +9.73% (rebound), 2022 −0.38%, 2023 +1.29%, 2024 −0.92%, 2025 +0.48%.
- Qualitatively consistent with V2-derived `investment_growth` (~1.5% mean) but shows the real COVID trough/rebound the V2 regression smoothed; V2-derived series is NOT treated as observed.

## 4. rho_inv timing resolution (desired gap D = −6.5% per +1pp)
Cumulative share of D reached:
| rho | y1 | y2 | y3 | y5 |
|-----|----|----|----|----|
| 0.0 | 100% | 100% | 100% | 100% |
| 0.2 | 80% | 96% | 99% | 100% |
| 0.4 | 60% | 84% | 94% | 99% |
| 0.6 | 40% | 64% | 78% | 92% |

External evidence: 1pp rate change → ~6–7% investment-level effect within **1–2 years**. rho=0.6 reaches only 40%/64% by y1/y2 → contradicts evidence. rho=0.2 reaches 80%/96% → matches. **Selected rho=0.20 central (low 0.0, high 0.40). rho=0.60 rejected.**

## 5. Capital-gap equation fix
Old (buggy): `prod_growth_dev = alpha*(I/K)*inv_level_gap_t` applied every year → unbounded accumulation.
Verdict: **FUNCTIONAL_FORM_BUG_CONFIRMED**.
Corrected:
```
capital_gap_t   = (1-delta)*capital_gap_{t-1} + (I/K)*inv_level_gap_t
prod_level_gap_t = alpha * capital_gap_t
prod_growth_dev_t = alpha*(capital_gap_t - capital_gap_{t-1})   # = alpha*Δcapital_gap
```
Growth deviation is the change in the capital gap, not a permanent annual penalty.

## 6. Constant financing-gap diagnostics (rho=0.20; values in %)
| bp | yr | inv_gap | cap_gap | prod_growth_dev | cum prod_level |
|----|----|---------|---------|-----------------|----------------|
| +100 | 1 | −5.20 | −0.57 | −0.19 | −0.19 |
| +100 | 2 | −6.24 | −1.20 | −0.21 | −0.40 |
| +100 | 5 | −6.50 | −2.81 | −0.16 | −0.93 |
| +100 |10 | −6.50 | −4.59 | −0.09 | −1.51 |
| +100 |20 | −6.50 | −6.26 | −0.03 | −2.06 |
| +100 | SS | — | −7.15 | →0 | −2.36 |
| +200 |20 | −13.0 | −12.51 | −0.07 | −4.13 |
| +200 | SS | — | −14.30 | →0 | −4.72 |
| +300 |20 | −19.5 | −18.77 | −0.10 | −6.19 |
| +300 | SS | — | −21.45 | →0 | −7.08 |

Property holds: persistent high financing → permanently lower capital/productivity level, but `prod_growth_dev → 0` at steady state (no forever annual penalty).

## 7. +251bp high-debt diagnostic (rho=0.20)
D = −16.315%. yr1 inv −13.05 / cap −1.44 / gdev −0.47 / level −0.47; yr2 …/−3.02/−0.52/−0.99; yr5 …/−7.05/−0.40/−2.33; yr10 …/−11.51/−0.24/−3.80; yr20 …/−15.70/−0.08/−5.18; SS cap −17.95 / level −5.92. Mechanism diagnostic only.

## 8. Steady-state check
`capital_gap_ss = (I/K / delta) * inv_gap`; `prod_level_ss = alpha * capital_gap_ss`. Verified numerically (table above). Correct bounded long-run materiality measure.

## 9. Double-counting
`BASE_PRODUCTIVITY_TREND = 0.00825` already embeds normal TFP + capital deepening. V4 adds ONLY the reference-relative capital-gap change: `prod_growth_t = 0.00825 + alpha*Δcapital_gap_t + ai_effect_t + climate_drag_t`. No stacking of normal deepening.

## 10. Reference conditions
`CCR_REF = 0.01766`; `inv_level_gap_0 = 0`; `capital_gap_0 = 0` at V4 start. Zero gap = "relative to historically normal/reference capital formation," not "France has zero capital."

## 11. Parameter provenance
| param | class |
|-------|-------|
| beta_credit_level | EXTERNAL_EMPIRICAL_PRIOR |
| rho_inv | MODEL_PRIOR (reconciled to 1–2yr response) |
| delta | EXTERNAL_EMPIRICAL_PRIOR |
| I/K | EXTERNAL_EMPIRICAL_PRIOR (reconfirmable vs retrieved GFCF) |
| alpha | EXTERNAL_EMPIRICAL_PRIOR |
| BASE_PRODUCTIVITY_TREND | OBSERVED_DATA_DERIVED (re-verified) |

## 12. Frozen central contract
CENTRAL: beta_credit_level −6.5; rho_inv 0.20; delta 0.10; I/K 0.11; alpha 0.33; BASE 0.00825.
Sensitivities only for external params: beta_credit_level {−4.0,−9.0}; rho_inv {0.0,0.40}; I/K {0.09,0.13}; alpha {0.30,0.36}.

## 14. Classification
**FRANCESCOPE V4 CORR-1 FINAL CALIBRATION GATE PASSED — READY FOR IMPLEMENTATION**

## 18. Recommended next task
Implement CORR-1 in production source per the frozen contract in `FRANCESCOPE_V4_CORR1_FINAL_IMPLEMENTATION_CONTRACT.csv` (capital-gap state + corrected productivity-growth-dev equation, rho=0.20), then re-run the V3 Monte Carlo (monte_carlo_v3.py / v1_orchestrator.py) and validate Index/diagnostics.
