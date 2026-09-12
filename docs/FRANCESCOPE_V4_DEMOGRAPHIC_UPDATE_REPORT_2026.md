# FranceScope V4 — Demographic Update Implementation Report

**Date**: 2026-09-02
**Authoritative vintage**: INSEE Projections de population 2026-2070 (publié 2026-06-08), scénario central + INSEE Bilan démographique 2025 (publié 2026-01-13)

This artifact documents the demographic-data correction cycle that replaced the stale 2021 INSEE projection vintage with the 2026 INSEE projection vintage. **No economic equation, labor-force equation, fiscal equation, CORR-1/2/3/4 parameter, Index scoring constant, Monte Carlo parameter, scenario selection or frontend code was modified.**

---

## Files created or modified

### New scripts
- `scripts/ingest_v4_demographics_proj2026.py` — parses the official INSEE 2026 projection workbook (`data/raw/insee/proj2026/00_central.xlsx`), derives aggregates and life expectancy from single-year mortality tables, and writes the canonical long-format panel.
- `scripts/compare_demographic_before_after.py` — prints the before/after comparison shown below.

### New data
- `data/raw/insee/proj2026/00_central.xlsx` — downloaded from `https://www.insee.fr/fr/statistiques/fichier/8990852/00_central.xlsx` (Insee Résultats, "Projections de population 2026 pour la France — Scénario central", published 2026-06-08).

### Updated data
- `data/processed/demographics/francescope_v3_demographic_canonical.{parquet,csv}` — regenerated with INSEE 2026 vintage.
- `data/processed/demographics/insee_demographic_annual_source.{parquet,csv}` — regenerated to mirror the canonical panel.

### Updated engine code
- `src/francescope/demographics/structural_driver.py` — `HISTORY_END` moved from 2021 → 2024; `NET_MIGRATION_PROJECTION_ASSUMPTION` updated from 70,000 → 150,000 (INSEE 2026 central). Public API unchanged. The defensive `_splice_2027_levels` left in place as a no-op (no longer mutates the data because there is no 2026/2027 plateau in the new vintage).

### Updated tests (necessary to reflect the new data)
- `src/francescope/demographics/tests/test_structural_driver.py` — `test_central_path_complete_2000_2070` row count updated (HISTORICAL_COMMON 2000-2024 + central 2025-2070 = 71 rows); `test_central_reconciles_with_canonical_d2` uses `HISTORY_END=2024` and no longer skips the 2027 splice (the splice is a no-op now).

---

## Central-scenario before vs after

(Values before = the canonical panel as of pre-correction, sourced from `INSEE Projections 2021-2070`; values after = new canonical panel, sourced from `INSEE Projections 2026-2070`.)

### total_population
| year | BEFORE | AFTER | delta |
|---:|---:|---:|---:|
| 2025 | 67,955,200 | 68,851,996 | +896,796 |
| 2026 | 69,082,000 | 69,082,000 | 0 |
| 2027 | 69,082,000 | 69,231,539 | +149,539 |
| 2030 | 69,419,180 | 69,525,618 | +106,438 |
| 2040 | 70,090,260 | 69,731,613 | -358,647 |
| 2050 | 70,071,690 | 69,082,377 | -989,313 |

### working_age_population (20–64)
| year | BEFORE | AFTER | delta |
|---:|---:|---:|---:|
| 2025 | 38,118,180 | 38,117,174 | -1,006 |
| 2026 | 38,245,514 | 38,215,215 | -30,299 |
| 2027 | 38,245,514 | 38,251,640 | +6,126 |
| 2030 | 38,099,053 | 38,289,535 | +190,482 |
| 2040 | 37,512,499 | 38,187,809 | +675,310 |
| 2050 | 36,715,543 | 37,326,628 | +611,085 |

### old_age_population (65+)
| year | BEFORE | AFTER | delta |
|---:|---:|---:|---:|
| 2025 | 14,264,220 | 15,054,014 | +789,794 |
| 2026 | 14,311,870 | 15,339,252 | +1,027,382 |
| 2027 | 14,311,870 | 15,612,584 | +1,300,714 |
| 2030 | 15,104,970 | 16,452,261 | +1,347,291 |
| 2040 | 17,071,910 | 18,571,304 | +1,499,394 |
| 2050 | 17,654,490 | 19,369,985 | +1,715,495 |

### net_migration
| year | BEFORE | AFTER | delta |
|---:|---:|---:|---:|
| 2025 | 150,000 | 176,000 | +26,000 |
| 2026 | 150,000 | 150,000 | 0 |
| 2027 | 134,000 | 150,000 | +16,000 |
| 2030 | 86,000 | 150,000 | +64,000 |
| 2040 | 70,000 | 150,000 | +80,000 |
| 2050 | 70,000 | 150,000 | +80,000 |

### total_fertility_rate
| year | BEFORE | AFTER | delta |
|---:|---:|---:|---:|
| 2025 | 1.560 | 1.560 | 0.000 |
| 2026 | 1.560 | 1.530 | -0.030 |
| 2027 | 1.608 | 1.488 | -0.120 |
| 2030 | 1.752 | 1.450 | -0.302 |
| 2040 | 1.800 | 1.450 | -0.350 |
| 2050 | 1.800 | 1.450 | -0.350 |

### life_expectancy_male / female
| year | LE_M before | LE_M after | LE_F before | LE_F after |
|---:|---:|---:|---:|---:|
| 2025 | 80.0 | 80.30 | 85.6 | 85.90 |
| 2026 | 80.0 | 80.94 | 85.6 | 86.43 |
| 2027 | 80.18 | 81.09 | 85.72 | 86.50 |
| 2030 | 81.07 | 81.51 | 86.27 | 86.70 |
| 2040 | 82.93 | 82.97 | 87.15 | 87.35 |
| 2050 | 84.58 | 84.46 | 88.06 | 88.19 |

---

## 2026 → 2027 transition (no more artificial source-vintage jump)

| variable | before delta (2026 → 2027) | after delta (2026 → 2027) |
|---|---:|---:|
| total_population | **+0** (frozen plateau from 2021 projection) | **+149,539** (smooth rise) |
| working_age_population | **+0** (plateau) | **+36,425** |
| old_age_population | **+0** (plateau) | **+273,332** |
| net_migration | **-16,000** (artefactual drop 150k → 134k) | **0** (constant 150k from INSEE 2026) |
| total_fertility_rate | +0.048 (jumps from 1.56 to 1.608) | -0.042 (1.53 → 1.488, converging to 1.45) |
| life_expectancy_male | +0.179 | +0.186 |
| life_expectancy_female | +0.123 | +0.097 |

The previously-artificial `total_population` plateau at 2026 levels (caused by the 2021 INSEE projection table leaving 2027 levels identical to 2026 across every reference scenario) is **eliminated**. The new INSEE 2026 projection provides a smooth 2027 path for all level variables.

---

## Lineage preservation

| data_status label | year coverage (central) | meaning |
|---|---|---|
| `observed` | 2025, 2026 | INSEE Bilan démographique 2025, published 2026-01-13 |
| `bridge_estimate` | 2027 | Linear midpoint of 2026 observed and 2028 projected levels; rates from INSEE 2026 projection |
| `official_projection` | 2028 → 2070 | INSEE Projections de population 2026-2070, scénario central, published 2026-06-08 |

---

## Validation summary

- Central scenario: **0** NaN / Inf / null cells in the new canonical panel.
- HISTORICAL_COMMON: 3 pre-existing nulls (`net_migration` 2018-2020) — pre-existing, not introduced by this task. `StructuralDemographicDriver` fills these with 0 at read time.
- All tests pass: `tests_structural_driver.py` (10/10), `test_labor_force.py`, `test_structural_growth.py`, `test_page3_demographic_fiscal_continuity.py` (38/38 total downstream).
- Engine loads cleanly: `StructuralDemographicDriver.state(year, 'central')` returns finite values for all years 2000 → 2070.

---

## Invariants preserved

- MASTER_SEED = 20260815, n_paths = 1000, horizon 2027-2050, P10/P50/P90 path IDs 805/841/351 — unchanged.
- Index scoring constants, V3 Index reference period 2010-2019, component weights 1/3 each — unchanged.
- CORR-1, CORR-2, CORR-3, CORR-4 equations and frozen parameters — unchanged.
- Labor-force participation logic, active-population logic, fiscal equations — unchanged.
- LFPR AR(1) constants in `src/francescope/gdp/labor_force.py` — unchanged.
- All frontend code — unchanged.