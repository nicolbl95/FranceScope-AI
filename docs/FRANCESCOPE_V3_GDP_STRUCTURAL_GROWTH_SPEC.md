# FranceScope V3 — GDP Structural-Growth Specification (PRODUCTIVITY FOUNDATION VALIDATED)

Date: 2026-08-23. Final calibration gate (productivity representation). No engine code modified.

## 1. Historical inputs available (repo-only)
- `real_gdp_per_capita` (eurostat_canonical.parquet, FR, annual 2010-2025, CLV20_EUR_HAB).
- `labor_productivity` (eurostat_canonical.parquet, FR, annual 2010-2025, index 2020=100) — **observed output per employee**.
- `real_gdp` annual level NOT present (only quarterly); `employment_rate`, `labor_force_participation_rate`, `hours_worked_per_employee` also present.
- D3 `working_age_population` (annual 2000-2070).
Common FR coverage 2010-2025. Labor productivity IS constructible/available directly.

## 2. Labor-productivity growth statistics
From `labor_productivity` (annual growth): mean(full 2011-2025)=0.44%, median=0.38%, pre-Covid mean(2011-2019)=**0.825%**, post-2020 weak/negative (Covid + energy shock). Selected structural trend = **pre-Covid mean 0.825%/yr** (potential trend; 2020 anomaly and depressed post-2020 excluded). Full-sample mean 0.44% reported as conservative sensitivity.

## 3. Architecture comparison
- **A (TFP-style, prior): REJECTED.** `0.6*wap_g + 0.4*productivity` is non-standard — in Cobb-Douglas, TFP enters with coefficient **1**, not capital share. The V2 `productivity_growth` is a generic, uncalibrated ScenarioDriver, so it cannot supply a defensible TFP series.
- **B (labor-productivity): SELECTED.** Observed FR data; transparent identity `Y ≈ L × (Y/L)`; no unobserved TFP; no capital-stock model; no arbitrary capital constant. Avoids double-counting (labor productivity already embeds capital deepening + TFP).
- **C (Cobb-Douglas + capital): REJECTED** — no capital-stock series.

## 4. Final formula
```
structural_growth_t = working_age_population_growth_t
                      + labor_productivity_growth_trend
                      + ai_productivity_effect_t                # future hook, default 0

real_gdp_growth_t = structural_growth_t + cyclical_input_t + shock_input_t
real_gdp_t        = real_gdp_{t-1} * (1 + real_gdp_growth_t)
```
Constants: labor_productivity_growth_trend = 0.00825 (pre-Covid 2011-2019 mean, observed). Units: annual fractional growth. No external-growth permanent term; no capital constant; no generic TFP driver.

## 5. Future hooks
```
cyclical_input_t = B_g*(global_growth_t - 0.018) + B_fd*(foreign_demand_t - fd_mean) + macro_regime_t
shock_input_t    = -0.5*climate_damage - 0.2*oil_shock - 0.15*geopolitical_shock - 0.3*fiscal_stress + global_financial_crisis_t
```
`ai_productivity_effect` modifies the productivity term (default 0) until the explicit AI module exists. V2 to replace: `compute_real_gdp` growth line.

## 6. Structural-only diagnostic (NOT P50; no recessions by construction — post-D5A, uses labor_force_growth)
Average structural growth: **2027-2030 = 0.452%**, **2031-2040 = 0.592%**, **2041-2050 = 0.593%**, **2027-2050 = 0.569%**.
- Productivity contribution: constant **+0.825pp/yr** (trend).
- Labor contribution: labor_force_growth = WAP growth + LFPR growth. LFPR uses the deterministic V2 AR(1) (mean ~80pp), reverting from the 81.5% (2026) anchor toward ~80%, so participation drags labor-force growth by ~0.1-0.25pp/yr (front-loaded in 2027).
Path is domestic, gently declining; recessions deferred to macro_regime / global_financial_crisis / correlated shocks.

## 7. D5 labor-force upgrade — DONE
`labor_force_growth` (= WAP × participation_rate, V2 AR(1) deterministic) now replaces the temporary WAP-growth proxy in the structural GDP formula. Unemployment stays out of labor supply (enters later as labor_force × (1 − unemployment_rate)). Retiree/pension integration remains pending (fiscal / median-living-standard work).

## 8. Artifacts
- docs/FRANCESCOPE_V3_GDP_STRUCTURAL_GROWTH_SPEC.md
- FRANCESCOPE_V3_GDP_INPUT_CLASSIFICATION.csv
- FRANCESCOPE_V3_GDP_STRUCTURAL_CANDIDATES.csv
- FRANCESCOPE_V3_GDP_STRUCTURAL_DIAGNOSTICS.csv
