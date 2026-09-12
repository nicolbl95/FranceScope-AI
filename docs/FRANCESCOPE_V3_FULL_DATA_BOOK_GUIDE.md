# FRANCESCOPE V3 — FULL DATA BOOK GUIDE

**Workbook:** `data/audits/full_data_review/FRANCESCOPE_V3_FULL_DATA_BOOK.xlsx`

## Purpose

This workbook is a **forensic data-review** artifact for FranceScope V3. It consolidates
every validated extraction output from Session 2A into a single, human-inspectable
multi-sheet Excel file. Nothing here was recomputed, recalibrated, or inferred — all
values are copied verbatim from the frozen Session 2A CSVs.

## Sheet structure

| Sheet | Contents |
|-------|----------|
| `00_README` | Orientation, definitions, unit rules, legend |
| `01_VARIABLE_CATALOG` | Full 140-variable inventory (filter enabled) |
| `02_STATIC_PARAMETERS` | 105 frozen/material parameters, grouped by module |
| `03_HISTORY_CORE_INDEX` | Index build 2010–2026 — **high-priority review** |
| `04_HISTORY_DEMOGRAPHICS` | Demographic history (2000–2026) |
| `05_HISTORY_PRODUCTION_LABOUR` | Production / labour / GDP history (1996–2026) |
| `06_HISTORY_EXTERNAL` | Credit & regime history (2003–2026) |
| `07_HISTORY_FISCAL_SOVEREIGN` | Fiscal & sovereign history (1986–2026) |
| `08_HISTORY_OTHER_ACTIVE` | INDEX-domain raw variables |
| `09_FORECAST_P10` | Coherent path **856** (P10 lower), 2027–2050 |
| `10_FORECAST_P50` | Coherent path **524** (P50 central), 2027–2050 |
| `11_FORECAST_P90` | Coherent path **367** (P90 upper), 2027–2050 |
| `12_MC1000_QUANTILES` | MC marginal quantiles, 23 variables, 552 rows |
| `13_MC1000_CATEGORICAL` | Regime / GFC categorical shares, 282 rows |
| `14_MC1000_PATH_INPUTS` | 1000 path-level inputs (856/524/367 highlighted) |
| `15_HISTORY_FORECAST_COMBINED` | Unified 2026→2027 view, 1160 rows |
| `16_BOUNDARY_2026_2027` | 2026→2027 boundary check, 43 variables |
| `17_DATA_GAPS` | Missing-data classification, 66 rows |
| `18_LEGACY_DEFERRED` | Non-active V3 variables, 593 rows |

## Historical vs forecast values

- **HISTORICAL** = observed / derived / bridge data through 2026 (sheets 03–08, 15, 16).
- **FORECAST** = official V3 simulation 2027–2050 (sheets 09–11, parts of 15–16).

## Coherent paths vs MC marginal quantiles

| Concept | Meaning | Where |
|---------|---------|-------|
| Coherent path P10 | Selected representative lower trajectory | path **856** (`09_FORECAST_P10`) |
| Coherent path P50 | Selected representative central trajectory | path **524** (`10_FORECAST_P50`) |
| Coherent path P90 | Selected representative upper trajectory | path **367** (`11_FORECAST_P90`) |
| MC_P10 / MC_P50 / MC_P90 | Marginal quantiles across **all 1000** simulated paths | `12_MC1000_QUANTILES`, `15_HISTORY_FORECAST_COMBINED`, `16_BOUNDARY_2026_2027` |

The coherent paths are **not** the same as the MC marginal quantiles. A coherent path is
one internally consistent full trajectory; the MC quantiles are cross-sectional
percentiles taken independently at each year.

## Units (critical)

- **Unemployment** is stored as a **decimal**: `0.081` = 8.1%. The workbook applies Excel
  percentage display formatting (`8.10%`) but the underlying numeric value remains `0.081`.
- **Debt / fiscal ratios** are stored as **percentage points of GDP**: `debt_gdp = 123.3`
  means 123.3 % of GDP. These are shown as ordinary numbers; **do not** apply Excel `%`
  formatting (that would display 12,330%).
- Generic GDP-growth / rate decimals (e.g. `real_gdp_growth = 0.02`) are shown as decimals.

## Bridge statuses

On `03_HISTORY_CORE_INDEX`, the `data_status` column is colour-coded:

- `OBSERVED` — green
- `MIXED_OBSERVED_BRIDGE` — yellow
- `BRIDGE_ESTIMATE` — orange

Values are unchanged; only the cell fill is applied for visual scanning.

## Latent variables

Model-latent V3 shocks (e.g. `external_cycle_shock`, `climate_amplitude`,
`ai_productivity_amplitude`) legitimately have **no observed history**. This is documented
in `17_DATA_GAPS` under classification `MODEL_LATENT_NO_OBSERVED_HISTORY` and is **not** an
error. Do not fabricate historical series for them.

## Legacy / deferred variables

`18_LEGACY_DEFERRED` is clearly headed **NOT ACTIVE IN FRANCESCOPE V3**. It contains legacy
V2 variables, the old 7-component Index variables/scores, deferred external AR(1) variables,
the China hook where relevant, and credit→investment / climate-disaster deferred fields.
These are kept for traceability only and must not be confused with active V3 mechanisms.

## Inspecting 2026 → 2027 continuity

Two sheets are designed for this:

- `15_HISTORY_FORECAST_COMBINED` — sorted by `variable` then `year`. The `period_type`
  column is coloured (green = HISTORICAL, blue = FORECAST) so the 2026 → 2027 transition is
  visible per variable. `comparability_status` is variable-level.
- `16_BOUNDARY_2026_2027` — shows each variable's 2026 value/status alongside the 2027
  coherent and MC quantiles, plus `delta_2027_P50_vs_2026` and
  `pct_change_if_meaningful`. `comparability_status` is colour-coded
  (green = COMPARABLE, yellow = NO_HISTORICAL_ANALOGUE, orange = NO_FORECAST_ANALOGUE).
  A colour-scale is applied to the delta column for magnitude only — it does **not** mark
  anything as an error.

## Source immutability

No Excel formula recomputes Index, GDPpc, quantiles, coherent, or forecast values. All
cells are populated directly from the validated CSVs. Convenience formatting never alters
numeric content.

## Anomaly interpretation is deferred

This book supports inspection only. Interpretation of anomalies, gaps, and boundary jumps
is the subject of the **next task: FRANCESCOPE V3 FULL DATA CONSISTENCY AUDIT**.
