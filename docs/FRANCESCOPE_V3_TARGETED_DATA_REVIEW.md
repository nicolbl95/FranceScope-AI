# FRANCESCOPE V3 — TARGETED DATA REVIEW (2 MEDIUM + 13 LOW findings)

Diagnosis and classification only. No data, model, or catalog edits were made.

## 1. Inflation duplicate (MEDIUM A)

**Cause:** Two distinct `CATALOG` rows share the key `inflation`:

| Row | human_readable_name | primary_status | domain | source | unit | downstream |
|-----|--------------------|----------------|--------|--------|------|-----------|
| 1 | HICP inflation (V2) | LEGACY_V2_ONLY | V2_ENGINE | p0_future_role_map.csv | UNKNOWN | V2 engine |
| 2 | Inflation anchor (state field) | STATIC_PARAMETER | STATIC | v1_orchestrator.py | decimal | nominal_growth |

Row 1 is the legacy V2 HICP trajectory (not wired into active V3). Row 2 is the frozen
active static scalar `INFLATION_ANCHOR = 0.02` used for nominal-growth construction.

**Classification:** `ACTIVE_V3_VS_LEGACY_V2_NAME_COLLISION` — distinct entities sharing an
ambiguous catalog key.

**Output impact:** `METADATA_ONLY_NO_OUTPUT_IMPACT`. Zero hits for `inflation` in the
historical LONG, coherent forecast, MC1000, combined, boundary, and parameter tables.
No data row was overwritten, duplicated, merged, or ambiguously joined. Official outputs
use `INFLATION_ANCHOR` (static) and never reference the legacy V2 trajectory.

**Recommended action (next task):** `RENAME_LEGACY_KEY_FOR_CLARITY` — rename the legacy V2
row (e.g. `inflation_hicp_v2`) to remove the key collision; keep the active static
`inflation` = `INFLATION_ANCHOR` unchanged.

## 2. GDP growth 2026→2027 (MEDIUM B)

**Exact values (decimal annual growth):**

| Item | Value | pp |
|------|-------|-----|
| 2025 real_gdp_growth (derived) | +0.00888 | +0.89% |
| 2026 real_gdp_growth (derived) | +0.00500 | +0.50% |
| 2027 coherent P10 / P50 / P90 | −0.00539 / −0.00901 / +0.00703 | −0.54% / −0.90% / +0.70% |
| 2027 MC P10 / P50 / P90 | −0.01240 / −0.00110 / +0.00914 | −1.24% / −0.11% / +0.91% |

**Step analysis:**
- **Absolute step (primary metric):** 2027 P50 − 2026 = **−0.01401 = −1.401 pp.**
- **Relative step (diagnostic only):** −280% — this is a **small-base artefact** because
  the 2026 base is only +0.5%; a modest absolute decline looks large in relative terms.
  The relative metric must NOT be used as the primary measure here.

**Historical context (2010–2026):** mean +1.18%, median +1.21%, SD **2.71 pp**,
min −7.61% (2020), max +6.79%. Largest non-COVID year-to-year changes ~4 pp (2021→2022).
The 2026→2027 absolute step of **−1.4 pp is well inside normal historical volatility**
(SD 2.7 pp) and far smaller than the 2020 COVID step (−9.7 pp).

**2026 bridge semantics:** 2026 real_gdp_growth has `data_status = derived` (a derived/
bridge estimate, not a full-year observation); 2027 is the first fully model-generated
year. Constructed from repository lineage; no external data.

**2027 decomposition:** the final `real_gdp_growth` is a stored engine output. Stored
component effects for P50 2027 are present and plausible (ai_productivity_effect ≈ +0.05%,
climate_drag ≈ −0.11%, external_cycle_shock z ≈ −1.04). The additive sub-terms
(structural_gdp_growth, regime_cyclical_input, external_cyclical_input, fiscal_gdp_contribution)
are not stored as separate rows, but the output is internally consistent.

**2027 MC distribution (all quantiles shifted down together):** P05 −1.69%, P10 −1.24%,
P25 −0.65%, P50 −0.11%, P75 +0.43%, P90 +0.91%, P95 +1.13%. A uniform center shift (not a
stochastic tail) — consistent with a structural/bridge transition.

**GDP LEVEL continuity (critical check):** implied 2027 level = 2026 level × (1 + 2027 growth)
= 2,663,693.954 = **stored 2027 level 2,663,693.954 (residual 0.0000%)**. GDP-per-capita
continuity also holds (minor ~0.2% residual from the independent population path).

**Classification:** `LARGE_BUT_PLAUSIBLE_CHANGE` — a **GROWTH_RATE_STEP** (absolute −1.4 pp,
within historical volatility), NOT a level discontinuity, unit, definition, or model-wiring
problem.

**Recommended action:** `NO_ACTION_REQUIRED` (optionally document as EXPECTED_FORECAST_TRANSITION).

## 3. Historical LOW outliers

All 13 LOW flags are `historical_outlier` (robust first-difference z>5) and are directionally
coherent with adjacent years, with no unit change or source discontinuity:

- **2020 COVID shock** (`real_gdp_level` −7.6%, `real_gdp_growth` collapse, `real_gdp_per_capita` −7.8%,
  `median_living_growth` −460% rel, `real_gdp_per_capita_score` −26%, `debt_gdp` +17%,
  `deficit_gdp` +270%, `life_expectancy_male` −0.7%): **EXPECTED_HISTORICAL_EVENT**.
- **2021 rebound** (`real_gdp_growth` +189% rel, `median_living_growth` +190% rel,
  `investment_growth` +201% rel): **EXPECTED_HISTORICAL_EVENT** (recovery from 2020 trough).
- **2009 shock** (`corporate_credit_rate` −57.5% rel): **EXPECTED_HISTORICAL_EVENT** (GFC rate
  action).
- **2023** (`corporate_credit_rate` +140.9% rel): **EXPECTED_HISTORICAL_EVENT** (ECB hiking cycle).

No `SOURCE_REVIEW_REQUIRED`, `UNIT_REVIEW_REQUIRED`, or `DATA_REVIEW_REQUIRED` classifications.

## 4. Remaining required actions

1. **(Next task) Rename the legacy V2 `inflation` catalog key** to remove the metadata
   collision — harmless, does not change any numeric output.
2. No correction to GDP growth 2026→2027 (explained, plausible, level-exact).
3. No action on the 13 LOW historical outliers (expected real-world events).

## 5. Final gate

**FULL_DATA_METADATA_FIX_REQUIRED**

Both MEDIUM findings are explained: the GDP-growth step is a plausible growth-rate step with
exact level continuity (no correction needed), and the `inflation` duplicate is a harmless
catalog/metadata name collision. The only remaining item is a non-substantive catalog key
rename for the legacy V2 inflation row.
