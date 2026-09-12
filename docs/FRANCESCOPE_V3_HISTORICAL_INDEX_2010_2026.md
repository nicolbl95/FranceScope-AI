# FRANCESCOPE V3 — OFFICIAL HISTORICAL INDEX 2010–2026

**Status:** `OFFICIAL_HISTORICAL_V3_INDEX`. Scoring methodology frozen (legacy-style z-score, 2010–2019 reference). Generated deterministically; no Monte Carlo, no clipping.

## 1. Production scoring module
`src/francescope/index/v3_index.py` exposes pure deterministic functions:
- `compute_component_score(value, median, sd, direction, base=100, points_per_sd=10)`
- `component_score_gdp_pc / _median_living / _unemployment`
- `compute_index_v3(gdp_pc, median_living, unemployment)` → 3 raw scores + RAW Index
- `contributions(...)` → diagnostic contribution relative to base 100

No file IO, no RNG, no future-distribution dependence, no state mutation. Reference statistics are module constants (exact stored values).

## 2. Exact frozen reference statistics (2010–2019)
| component | median | sd (ddof=1) | unit |
|---|---|---|---|
| real_gdp_per_capita | 0.035239062483334416 | 0.0009089951709464394 | MEUR/person |
| median_living_standard_real | 23800.0 | 360.647565729573 | EUR |
| unemployment_rate | 0.096 | 0.0064272099528316145 | decimal fraction |

Base 100, 10 points/SD, directions (+1,+1,−1), equal 1/3 weights.

## 3. Official historical Index — key years
| year | Index |
|---|---|
| 2010 | 97.966 |
| 2015 | 96.930 |
| 2019 | 123.459 |
| 2020 | 122.424 |
| 2021 | 130.612 |
| 2022 | 136.643 |
| 2023 | 140.945 |
| 2024 | 145.579 |
| 2025 | 143.421 |
| 2026 | 140.947 |

Full series min = **94.824 (2013)**, max = **145.579 (2024)**. All 17 years present, no NaN/inf.

## 4. Component scores — key years (RAW)
| year | gdp_pc | median_living | unemployment | Index |
|---|---|---|---|---|
| 2019 | 123.260 | 128.837 | 118.282 | 123.459 |
| 2020 | 91.192 | 151.574 | 124.505 | 122.424 |
| 2021 | 116.196 | 148.801 | 126.839 | 130.612 |
| 2022 | 126.839 | 147.692 | 135.396 | 136.643 |

## 5. Covid behavior (2019→2020→2021→2022)
2020 Index barely fell (123.46→122.42). Drivers: GDPpc collapsed (123.26→91.19, −32 pts) but **median living surged** (128.84→151.57, +23 pts, pandemic support) and unemployment improved (118.28→124.51). Net Index near-flat. 2021–2022 recovery: GDPpc rebounds, median living stays elevated, unemployment keeps improving → Index rises to 136.64. No scoring change; pure data reflection.

## 6. 2024–2026 bridge audit
| year | data_status | gdp_pc_s | med_s | unemp_s | Index |
|---|---|---|---|---|---|
| 2024 | OBSERVED | 138.527 | 164.757 | 133.452 | 145.579 |
| 2025 | MIXED_OBSERVED_BRIDGE | 141.404 | 159.685 | 129.173 | 143.421 |
| 2026 | BRIDGE_ESTIMATE | 142.697 | 156.806 | 123.338 | 140.947 |

No discontinuity from unit conversion (gdp_pc kept MEUR/person; unemployment decimal). Bridge status preserved in output.

## 7. Contribution balance (relative to base 100)
`contribution_j = (1/3)(score_j − 100)`; `Index = 100 + Σ contributions`. Example 2024: gdp +12.84, median +21.59, unemployment +11.15 → 145.58 (reconciles exactly). Median living is the largest positive contributor across 2020–2026 (consistent with its steady real growth).

## 8. Scoring sanity (25/25 tests PASS)
Reference 2010–2019; median→100; +1 SD→+10 (higher-better) / −10 (unemployment); one component ±1 SD moves Index by exactly **3.333333**; Index = arithmetic mean of components; contribution reconciles; NO clipping; fixed 2010–2019 normalization (never re-derived); unemployment decimal; gdp units match reference; weights exactly 1/3; all 17 years, no dup, no NaN/inf; bridge status preserved; deterministic; **V2 legacy artifacts unchanged**.

## 9. V2 unchanged
Legacy 7-component V2 Index (`FINAL_FRANCESCOPE_INDEX_ANNUAL_2010_2050.csv`, `compute_francescope_index`) not modified. V3 has different components; V3 is not tuned to V2.

## 10. Files created / modified
- `src/francescope/index/v3_index.py` (NEW module)
- `data/processed/index/francescope_v3_historical_index_2010_2026.csv` (+ `.parquet`)
- `data/audits/economic_system/FRANCESCOPE_V3_INDEX_HISTORICAL_VALIDATION.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_INDEX_HISTORICAL_CONTRIBUTIONS.csv`
- `docs/FRANCESCOPE_V3_HISTORICAL_INDEX_2010_2026.md` (this file)
- Updated: `FRANCESCOPE_V3_CURRENT_STATE_MATRIX.csv`, `docs/FRANCESCOPE_V3_CURRENT_STATE_CHECKPOINT.md`

## 11. Official historical status
`OFFICIAL_HISTORICAL_V3_INDEX` — 2010–2026 series official. Scoring method frozen. Future Index NOT marked complete.

## 12. AI review status
`AI_PRODUCTIVITY_SCALE_REVIEW = PENDING_BEFORE_OFFICIAL_MC1000` — non-blocking for historical Index.

## 13. Next task
**TARGETED V3 AI PRODUCTIVITY SCALE VERIFICATION**, then **OFFICIAL 1,000-PATH MONTE CARLO** with future V3 Index using the SAME frozen historical scoring constants.

## Final verdict
V3 HISTORICAL INDEX 2010–2026 OFFICIAL — READY FOR AI SCALE VERIFICATION
