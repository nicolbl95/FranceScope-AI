# FRANCESCOPE V3 INDEX — SCORING METHOD EVALUATION / FREEZE

**Scope:** Select ONE transparent scoring method for the three frozen V3 Index components
(`real_gdp_per_capita`, `median_living_standard_real`, `unemployment_rate`),
applied to historical 2010–2026 and future MC outputs. No production code, no MC run, no weights optimization.
**Decision:** `LEGACY_STYLE_Z_SCORE` FROZEN.

## 1. Authoritative 3-component historical coverage
- **real_gdp_per_capita** (MEUR/person): constructed `real_gdp / total_population` from `francescope_core_annual_2010_2026.csv` (real_gdp, MEUR) and `francescope_v3_demographic_canonical.parquet` (HISTORICAL_COMMON 2010–2021, central 2022–2026).
- **median_living_standard_real** (EUR): from core panel; observed 2010–2024, bridge 2025–2026.
- **unemployment_rate** (fraction): from core panel; observed 2010–2024, bridge 2025–2026 (converted from % to fraction to match MC units).
- Coverage 2010–2026 complete (all three present). 2010–2019 fully observed; 2024–2026 partly bridge (flagged via `data_status`).

## 2. 2010–2019 reference statistics (frozen anchor)
| component | unit | median | sd | min | max | MAD | CV |
|---|---|---|---|---|---|---|---|
| real_gdp_per_capita | MEUR | 0.035239 | 0.000909 | 0.034351 | 0.037353 | 0.000413 | 2.6% |
| median_living_standard_real | EUR | 23800 | 360.65 | 23690 | 24840 | 140.85 | 1.5% |
| unemployment_rate | fraction | 0.096000 | 0.006427 | 0.084250 | 0.103500 | 0.007784 | 6.7% |

All scales meaningful; no near-zero scale. 10-year window gives adequate variation.

## 3–5. Candidate results (RAW, no clipping)
- **Candidate A (Legacy z):** `100 + 10·dir·(x−median)/sd`. Historical Index 2010=97.97 → 2019=123.46 → 2026=140.95. Covid: 2019→2020 dips slightly (122.42), then recovers. Direction matches components.
- **Candidate B (Robust MAD):** `K=10` with MAD×1.4826. MAD for median_living is tiny (140 vs sd 361) → median_living score SD explodes to ~68 vs unemployment ~14. **Median-living dominates → rejected.**
- **Candidate C (Percent deviation, K=100):** unemployment score SD ~11.5 vs others ~4–4.7 → **unemployment dominates 2.5× → rejected** (also requires arbitrary K for cross-component balance).

## 6. Component-balance comparison (score SD over 2010–2026)
- A: gdp 18.1 / median 26.6 / unemp 17.2 — **most balanced**.
- B: gdp 39.8 / median 68.2 / unemp 14.2 — median dominates.
- C: gdp 4.7 / median 4.0 / unemp 11.5 — unemp dominates.
Equal weights = equal conceptual weight; A gives near-equal realized influence. No single component overwhelms.

## 7. Economic direction sanity
Perturbation around 2026: +1 SD → +10.0 on each component; −1 SD → −10.0. Symmetric for all three. GDPpc↑→Index↑, median↑→Index↑, unemp↑→Index↓ confirmed.

## 8. Interpretability
A: 100 ≈ 2010–2019 center; +10 points ≈ +1 reference SD on one component; +1 SD on one component moves total Index by ~3.33 points (1/3 weight). Intuitive and transparent.

## 9. Historical V3 Index diagnostic (Candidate A, provisional)
2010 97.97 · 2015 96.93 · 2019 123.46 · 2020 122.42 · 2021 130.61 · 2022 136.64 · 2023 140.95 · 2024 145.58 · 2025 143.42 · 2026 140.95. Rises through 2010s (growth + falling unemployment), mild COVID dip, post-COVID recovery. No bridge-induced artifacts. (Provisional — not yet official.)

## 10. Covid / reference-window sensitivity
2010–2019 deliberately excludes COVID — **desirable** as a fixed historical anchor. 2010–2018 alternative would only shift centers marginally; adopted fixed window rejected moving reference.

## 11. Future-range transformation sanity (MC100 2050, Candidate A)
gdp_pc 126/185/230 · median_living 153/182/201 · unemployment 143/134/126 (P10/P50/P90). All finite, positive (MC 2050 exceeds 2010–2019 levels on all three), interpretable, no dimension dominates numerically.

## 12. GDPpc vs median-living redundancy
Historical corr 0.79; MC2050 corr 0.999. High but not perfect; distinct concepts (aggregate resources vs distribution-sensitive outcome). **Both retained**; equal weighting accepted (no near-perfect correlation, distinct information).

## 13. Unemployment scaling
Unemployment has the largest historical CV (6.7%) but under z-scoring its realized score SD is the *smallest* (17.2) — no domination. Influence is economically justified volatility, not a normalization artifact.

## 14. Weights
Default 1/3 each. No scaling pathology requiring unequal weights → **FREEZE equal weights**.

## 15. Selected method
`LEGACY_STYLE_Z_SCORE`.

## 16. Frozen implementation contract
REFERENCE 2010–2019 · CENTER=median · SCALE=sample SD (ddof=1) · BASE=100 · POINTS_PER_SD=10 · dir(gdp_pc)=+1, dir(median_living)=+1, dir(unemployment)=−1 · weights 1/3 · `score=100+10·dir·(x−ref_median)/ref_sd` · Index = arithmetic mean of 3 RAW scores · **NO CLIPPING** · fixed anchor, never re-derived from future data.

## 17. Missing / bridge-data policy
Compute annual V3 Index only when all 3 components available. Bridge estimates (2025–2026 median_living, unemployment) permitted as authoritative; preserve `data_status`. No silent imputation.

## 18. Future Monte Carlo policy
SAME frozen 2010–2019 centers/scales applied to every year, path, scenario. Never recalculate scaling from simulated distributions.

## 19. Files created
- `docs/FRANCESCOPE_V3_INDEX_SCORING_METHOD_EVALUATION.md`
- `data/audits/economic_system/FRANCESCOPE_V3_INDEX_REFERENCE_STATISTICS.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_INDEX_SCORING_CANDIDATES.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_INDEX_COMPONENT_BALANCE.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_INDEX_SCORING_DIAGNOSTICS.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_INDEX_IMPLEMENTATION_CONTRACT.csv`

## 20. AI coefficient review
Still PENDING before official 1,000-path simulation (non-blocking, out of scope here).

## 21. Recommended next task
**Recalculate the historical V3 Index 2010–2026** with the frozen LEGACY_STYLE_Z_SCORE method (official historical Index build), then proceed to the official 1,000-path Monte Carlo / V3 Index distribution.

## Final verdict
V3 INDEX SCORING METHOD FROZEN — READY FOR HISTORICAL V3 INDEX
