# FRANCESCOPE V3 — FULL DATA CONSISTENCY AUDIT (Automated / Structural Pass)

**Scope:** All validated Session 2A extraction outputs (frozen). No values were
modified, no models re-run, no anomalies repaired. This document reports **mechanical /
structural** findings only.

**Reference constants:** Index scoring used exact frozen constants from
`src/francescope/index/v3_index.py` (GDPpc median/sd, median-living median/sd,
unemployment median/sd, base 100, 10 pts/SD, equal 1/3 weights). Recurrence, AI,
climate, and external identities used the active-V3 coefficients sourced from
`v1_orchestrator.py` / `contagion.py`.

---

## 1. FINAL GATE

**FULL_DATA_TARGETED_REVIEW_REQUIRED**

No CRITICAL or HIGH finding was produced. Two MEDIUM findings require human /
economic investigation, but neither invalidates the official outputs (no
arithmetic, unit, or source failure detected). Outputs remain usable.

---

## 2. FINDINGS BY SEVERITY

| Severity | Count | Meaning |
|----------|-------|---------|
| CRITICAL | 0 | none |
| HIGH | 0 | none |
| MEDIUM | 2 | targeted review required |
| LOW | 13 | documentation / expected-event / metadata |
| INFO | 0 | n/a |

---

## 3. CRITICAL / HIGH

None.

---

## 4. MEDIUM FINDINGS (require human review)

**M1 — Catalog duplicate key (`inflation`)**
- `check`: duplicate_key
- `evidence`: variable_name `('inflation',)` appears 2 times in
  `FRANCESCOPE_V3_COMPLETE_VARIABLE_INVENTORY.csv` (140-row catalog).
- `recommended_review`: Confirm whether the two `inflation` rows are intended
  (e.g. CPI vs HICP, or a true duplicate). Metadata only — does not affect
  numeric outputs.

**M2 — 2026→2027 continuity: `real_gdp_growth`**
- `check`: continuity_2026_2027
- `evidence`: coherent P50 path 524 shows a ~-280% *relative* change from the
  2026 historical `real_gdp_growth` to the 2027 coherent P50. As a YoY *rate*,
  this is a large but plausible slowdown-scenario transition (e.g. +1.x% → -x%).
- `recommended_review`: Human/economic confirmation that the 2026→2027 growth
  step is intended under the selected central scenario, not a serialization or
  unit artefact.

---

## 5. LOW FINDINGS (summary)

All 13 LOW findings are `historical_outlier` (robust first-difference z > 5) and
are consistent with known real-world events:

- **2020 COVID shock:** `real_gdp_level` (-7.6%), `real_gdp_growth` (-461% rel),
  `real_gdp_per_capita` (-7.8%), `median_living_growth` (-460% rel),
  `real_gdp_per_capita_score` (-26%), `debt_gdp` (+17%), `deficit_gdp` (+270%),
  `life_expectancy_male` (-0.7%).
- **2021 rebound:** `real_gdp_growth` (+189% rel), `median_living_growth`
  (+190% rel), `investment_growth` (+201% rel).
- **2009 financial crisis:** `corporate_credit_rate` (-57.5% rel).
- **2023:** `corporate_credit_rate` (+140.9% rel).

These are flagged `OUTLIER_REVIEW` / expected real-world events, NOT errors.
Classification recommendations: `EXPECTED_REAL_WORLD_EVENT` (2020/2021/2009).

---

## 6. WHAT WAS VERIFIED AS RECONCILED (no flags)

- **Basic integrity:** no NaN/Inf, no empty variable names, no duplicate keys
  (except the catalog `inflation` note above), consistent units/domains per
  historical variable.
- **Unit / scale:** unemployment decimal (0.081 = 8.1%), debt/deficit in
  percentage points of GDP, GDP/GDPpc in MEUR — no ×100/÷100/×1000 artefacts
  detected in the audited ranges.
- **Index identity (historical + forecast):** for all 17 historical years and
  all 24×3 forecast years, each component score and the aggregate
  `francescope_index_v3` reconcile with the frozen scoring formula and with
  `Index = mean(three component scores)` (0 mismatches, tolerance 1e-4).
- **GDPpc identity (historical):** `real_gdp_per_capita ≈ real_gdp_level /
  total_population` (reconciles within 5%, MEUR/person convention).
- **Median-living recurrence (paths 856/524/367):** 72 trajectory steps
  reconcile with `median_t = median_{t-1}·(1 + 0.00009 + 0.2880·gdp_growth
  − 0.0078·(u − 0.075))` (0 mismatches, tolerance 2%).
- **AI identities:** `ai_employment_displacement_amplitude ==
  ai_productivity_amplitude` for all 1000 paths; AI productivity profile is
  common across paths (effect/amplitude constant per year); amplitudes constant
  within path.
- **Climate identity:** `climate_drag = −0.001 · climate_amplitude` holds on all
  coherent rows.
- **Quantile ordering:** all 552 MC1000 rows monotonic (min ≤ P01 ≤ … ≤ max)
  and `count = 1000`.
- **Stochastic inputs:** all 1000 paths have AI amplitude ∈ [0.45, 1.70] and
  climate amplitude ∈ [0.30, 2.30].
- **Categorical:** regime categories within
  {EXPANSION, SLOWDOWN, RECESSION, CRISIS, RECOVERY}; GFC encoded
  TRIGGERED/NOT_TRIGGERED; shares per (variable, year) sum to 1; counts per
  (variable, year) sum to 1000.
- **Coherent-path mapping:** path 856 = P10, 524 = P50, 367 = P90; 1800
  coherent observations with no missing values.
- **2026→2027 boundary:** 14 COMPARABLE variables audited; only `real_gdp_growth`
  (M2) flagged for review; remaining 13 within plausible transition bounds.
- **Debt recursion (approximate):** using available real-growth proxy
  (inflation not in coherent audit set), max reconciliation residual < 10 pp
  across 856/524/367 — flagged INFO-level only; full nominal-growth check
  deferred to human review with complete MC trajectories.

---

## 7. NOTES / LIMITATIONS

- **External shock** (`external_cyclical_input = 0.008·z`): `external_cycle_shock`
  (the z) is present; `external_cyclical_input` itself is not in the coherent
  audit set, so a direct serialization check was not possible. `z` values are
  within plausible N(0,1) range.
- **Definition alignment:** COMPARABLE variables show consistent units between
  historical/forecast and inventory; no `DEFINITION_ALIGNMENT_REVIEW` raised.
- **Legacy/deferred (593 rows):** audited for labeling/metadata only; their
  absence from active V3 forecast logic is expected and NOT flagged.

---

## 8. DELIVERABLES

- `data/audits/full_data_review/FRANCESCOPE_V3_DATA_CONSISTENCY_FLAGS.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_HISTORICAL_DATA_AUDIT.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_FORECAST_DATA_AUDIT.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_2026_2027_CONTINUITY_AUDIT.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_IDENTITY_RECONCILIATION_AUDIT.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_RANGE_EXTREMA.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_FULL_DATA_BOOK.xlsx`
  (sheets **19_CONSISTENCY_FLAGS**, **20_BOUNDARY_AUDIT**,
  **21_IDENTITY_CHECKS**, **22_RANGE_EXTREMA** added; sheets 00–18 untouched)
- `docs/FRANCESCOPE_V3_FULL_DATA_CONSISTENCY_AUDIT.md` (this file)
