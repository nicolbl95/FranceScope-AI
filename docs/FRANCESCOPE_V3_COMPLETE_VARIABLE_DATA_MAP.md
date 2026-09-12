# FranceScope V3 — Complete Variable & Data-Lineage Inventory

**Inventory task only.** No model code was modified, no Monte Carlo was rerun, no forecasts recalculated, no recalibration performed, no data downloaded, and Index/scenarios were unchanged.

## 1. Scope and sources

Authoritative sources reconciled:
- `src/francescope/orchestrator/v1_orchestrator.py` — `V3PersistentState`, `V3YearInputs`, `V3Context`, `V3YearResult`, 2026 anchors, reproduced V2 coefficients, fiscal-impulse wiring.
- `gdp/structural_growth.py`, `gdp/labor_force.py`, `regime/macro_regime.py`, `external/contagion.py`, `climate/climate_effects.py`, `gfc/global_financial_crisis.py`, `ai/ai_effects.py`, `fiscal/sovereign_fiscal.py`, `demographics/structural_driver.py`, `index/v3_index.py`, `simulation/monte_carlo_v3.py` (RNG contract + stochastic draws).
- Older registries: `variable_registry.csv`, `FRANCESCOPE_V3_STATE_REGISTRY.csv`, `FRANCESCOPE_V3_ORCHESTRATOR_STATE_REGISTRY.csv`, `FRANCESCOPE_V3_INTERNAL_DRIVER_INVENTORY.csv`, `FRANCESCOPE_V3_DEMOGRAPHIC_VARIABLE_METADATA.csv`, `p0_future_role_map.csv`, `FRANCESCOPE_V3_INDEX_REFERENCE_STATISTICS.csv`, `FRANCESCOPE_V3_MC1000_RUN_METADATA.csv`, `FINAL_FRANCESCOPE_VARIABLE_METADATA.csv`, `FINAL_FRANCESCOPE_VARIABLE_COVERAGE.csv`.

## 2. Totals

- **Total variables inventoried: 140**
- **Static parameters inventoried: 105**
- **Data-availability rows: 50**

### Counts by primary status
- ACTIVE_V3_STATE: 17
- ACTIVE_V3_DRIVER: 3
- ACTIVE_V3_DERIVED: 33
- STOCHASTIC_INPUT: 6
- INDEX_COMPONENT: 3
- INDEX_SCORE: 4
- STATIC_PARAMETER: 33
- LEGACY_V2_ONLY: 28
- DEFERRED_NOT_ACTIVE: 13

### Counts by domain
- STATIC: 33
- V2_ENGINE: 19
- EXTERNAL: 14
- DEMOGRAPHICS: 13
- INDEX: 13
- FISCAL: 10
- PRODUCTION: 6
- CLIMATE: 6
- AI: 6
- SOVEREIGN: 5
- REGIME: 4
- GFC: 4
- CORE_OUTPUT: 3
- CREDIT: 3
- LABOUR: 1

## 3. Active V3 variables (complete list)

Active universe = 66 variables (ACTIVE_V3_STATE / ACTIVE_V3_DRIVER / ACTIVE_V3_DERIVED / INDEX_COMPONENT / INDEX_SCORE / STOCHASTIC_INPUT).

### ACTIVE_V3_STATE (17)
- **debt_gdp** — General government debt / GDP (SOVEREIGN): Gross public debt % of GDP
- **deficit_gdp** — General government deficit / GDP (FISCAL): Net lending/borrowing % of GDP (sign: +deficit)
- **fiscal_adjustment** — Fiscal adjustment (lagged) (FISCAL): Bounded lagged fiscal consolidation adjustment (pp GDP)
- **france_oat** — France 10Y OAT yield (SOVEREIGN): French 10-year government bond yield (decimal)
- **interest_burden** — Interest expenditure / GDP (FISCAL): Government interest expenditure % of GDP (=interest_expenditure_gdp)
- **life_expectancy_female** — Life expectancy at birth, female (DEMOGRAPHICS): Years
- **life_expectancy_male** — Life expectancy at birth, male (DEMOGRAPHICS): Years
- **net_migration** — Net migration (annual) (DEMOGRAPHICS): Annual net migration (persons); 0 for history (INSEE gap)
- **old_age_dependency_ratio** — Old-age dependency ratio (DEMOGRAPHICS): OAP / WAP (ratio)
- **old_age_population** — Old-age population (65+) (DEMOGRAPHICS): Population aged 65+ (persons)
- **old_age_share** — Old-age share (DEMOGRAPHICS): OAP / total_population (share)
- **real_gdp_level** — Real GDP level (PRODUCTION): Real GDP chain-linked volume (MEUR)
- **regime** — Macro-regime state (REGIME): French business-cycle state {EXPANSION,SLOWDOWN,RECESSION,CRISIS,RECOVERY}
- **sovereign_premium** — Sovereign fiscal-risk premium (SOVEREIGN): Incremental French sovereign risk premium (decimal rate), AR(1) state
- **total_fertility_rate** — Total fertility rate (DEMOGRAPHICS): Period TFR (children/woman)
- **working_age_share** — Working-age share (DEMOGRAPHICS): WAP / total_population (share)
- **year** — Simulation year (CORE_OUTPUT): Loop/calendar year counter

### ACTIVE_V3_DRIVER (3)
- **labor_force_growth** — Labour-force growth (DEMOGRAPHICS): YoY growth of labour force (decimal)
- **total_population** — Total population (DEMOGRAPHICS): French residents, all ages (persons)
- **working_age_population** — Working-age population (20-64) (DEMOGRAPHICS): Population aged 20-64 (persons)

### ACTIVE_V3_DERIVED (33)
- **adjusted_primary_expenditure** — Adjusted primary expenditure (FISCAL): Primary expenditure after reaction (pp GDP)
- **adjusted_revenue** — Adjusted government revenue (FISCAL): Revenue after reaction (pp GDP)
- **ai_employment_displacement_effect** — AI employment displacement (AI): AI labour-displacement pressure (decimal pp)
- **ai_productivity_effect** — AI productivity effect (AI): AI productivity-growth contribution (decimal)
- **climate_disaster** — Climate disaster shock (CLIMATE): Acute climate disaster GDP shock (decimal)
- **climate_drag** — Climate structural drag (CLIMATE): Chronic climate GDP drag = baseline_drag * amplitude (decimal)
- **corporate_credit_rate** — Corporate credit rate (CREDIT): Corporate lending rate (decimal), B2 wiring
- **cyclical_contribution** — Cyclical contribution (PRODUCTION): Sum of regime + external cyclical inputs
- **effective_debt_cost** — Effective debt cost (SOVEREIGN): Avg interest rate on debt (decimal), lag-1 OAT
- **effective_external_shock** — Effective external shock (EXTERNAL): Combined external-cycle + GFC shock z
- **euro_area_growth** — Euro-area growth (EXTERNAL): Euro-area GDP growth (decimal)
- **europe_factor** — Europe factor (EXTERNAL): European growth factor
- **expenditure_cut** — Expenditure cut (FISCAL): Fiscal expenditure cut (pp GDP)
- **external_cyclical_input** — External GDP cyclical input (EXTERNAL): V3 GDP cyclical hook = CYC_LOAD * z (decimal GDP growth)
- **fiscal_gdp_contribution** — Fiscal->GDP impulse (FISCAL): GDP-growth impact of lagged fiscal impulse (decimal)
- **fiscal_stress** — Fiscal stress index (FISCAL): Continuous fiscal-stress index in [0,1]
- **foreign_demand_growth** — Foreign-demand growth (EXTERNAL): Foreign-demand (FDI) index growth (decimal)
- **gfc_triggered** — GFC trigger flag (GFC): Boolean: global financial crisis triggered this year
- **global_growth_deviation** — Global growth deviation (EXTERNAL): Cyclical deviation around central global growth
- **interest_expenditure_gdp** — Interest expenditure / GDP (FISCAL): Interest expenditure % of GDP (=interest_burden)
- **investment_growth** — Investment growth (PRODUCTION): Real investment growth (decimal), V2 equation
- **labor_force** — Labour force (DEMOGRAPHICS): Employed + seeking (persons) = WAP * participation_rate
- **labor_force_participation_rate** — Labour-force participation rate (DEMOGRAPHICS): Participation rate (decimal, V2 AR(1))
- **median_living_growth** — Median-living growth (diagnostic) (CORE_OUTPUT): Yearly median-living growth used in MC collector
- **mortgage_rate** — Mortgage rate (CREDIT): New-business mortgage rate (decimal), B2 wiring
- **next_regime** — Next-year macro regime (REGIME): Regime drawn for next year from transition matrix
- **real_gdp_growth** — Real GDP growth (PRODUCTION): Total real-GDP growth = structural + cyclical + shock
- **regime_cyclical_input** — Regime cyclical input (REGIME): Persistent cyclical GDP contribution of current regime (decimal)
- **revenue_gain** — Revenue gain (FISCAL): Fiscal revenue gain (pp GDP)
- **shock_contribution** — Shock contribution (CLIMATE): Acute climate disaster GDP shock contribution
- **structural_gdp_growth** — Structural GDP growth (PRODUCTION): Structural GDP growth = labour_supply + productivity + AI + climate_drag
- **target_sovereign_premium** — Target sovereign premium (SOVEREIGN): Target incremental premium from fiscal fundamentals (decimal)
- **world_trade_growth** — World trade growth (EXTERNAL): World trade-volume growth (decimal)

### INDEX_COMPONENT (3)
- **median_living_standard_real** — Median living standard (real) (CORE_OUTPUT): Median equivalised household income, constant euros
- **real_gdp_per_capita** — Real GDP per capita (PRODUCTION): Real GDP / total population (MEUR/person)
- **unemployment_rate** — Unemployment rate (LABOUR): ILO unemployment rate (decimal)

### INDEX_SCORE (4)
- **francescope_index_v3** — FranceScope Index V3 (INDEX): Final V3 Index = arithmetic mean of 3 raw component scores (no clipping)
- **median_living_standard_real_score** — Median-living component score (INDEX): Raw z-style component score (base 100, 10 pts/SD)
- **real_gdp_per_capita_score** — Real GDP/capita component score (INDEX): Raw z-style component score (base 100, 10 pts/SD)
- **unemployment_rate_score** — Unemployment component score (INDEX): Raw z-style component score (base 100, 10 pts/SD, direction -1)

### STOCHASTIC_INPUT (6)
- **ai_employment_displacement_amplitude** — AI employment amplitude (AI): Path-level AI employment-displacement amplitude (triangular)
- **ai_productivity_amplitude** — AI productivity amplitude (AI): Path-level AI productivity amplitude (triangular)
- **climate_amplitude** — Climate amplitude (CLIMATE): Path-level climate amplitude draw (triangular)
- **external_cycle_shock** — External cycle shock (z) (EXTERNAL): Common external-cycle standard-normal draw (yearly)
- **gfc_uniform_draw** — GFC uniform draw (GFC): Uniform[0,1) draw for GFC trigger (yearly)
- **regime_uniform_draw** — Regime uniform draw (REGIME): Uniform[0,1) draw for next-regime selection (yearly)

## 4. Data availability

### Variables with historical data before 2010
- france_oat (start 1986)
- total_population (start 2000)
- working_age_population (start 2000)
- labor_force (start 2000)
- labor_force_participation_rate (start 2000)
- old_age_population (start 2000)
- working_age_share (start 2000)
- old_age_share (start 2000)
- old_age_dependency_ratio (start 2000)
- total_fertility_rate (start 2000)
- life_expectancy_male (start 2000)
- life_expectancy_female (start 2000)
- net_migration (start 2000)
- labor_force_growth (start 2001)
- mortgage_rate (start 2003)
- corporate_credit_rate (start 2003)

### Active dynamic variables lacking historical data
(Latent model variables with `MODEL_LATENT_NO_OBSERVED_HISTORY` are expected and not flagged as gaps.)
- sovereign_premium
- fiscal_adjustment
- next_regime
- gfc_triggered
- external_cyclical_input
- shock_contribution
- climate_drag
- climate_disaster
- ai_productivity_effect
- ai_employment_displacement_effect
- fiscal_gdp_contribution
- target_sovereign_premium
- expenditure_cut
- revenue_gain
- effective_external_shock
- global_growth_deviation
- europe_factor
- foreign_demand_growth
- world_trade_growth

### Active dynamic variables lacking forecast data

## 5. Legacy / deferred variables

Deferred or legacy (not part of active 3-component V3 simulation): 41

### DEFERRED_NOT_ACTIVE
- **ai_gfc_modifier** — DEFERRED.
- **ai_regime_direct_effect** — DEFERRED.
- **china_growth_gap** — DEFERRED: CHINA_LOAD = 0.0 pending calibration (CHINA_COEFFICIENT_PENDING_CALIBRATION). Unused China hook.
- **climate_fiscal_pressure** — DEFERRED: no climate fiscal pressure in minimal V3 foundation.
- **credit_investment_transmission** — DEFERRED: credit->investment link deferred (corporate_credit_rate not wired to investment).
- **external_stress_index** — DEFERRED: p0 external AR(1) block not wired into active V3 orchestrator. HISTORICAL_NOT_AVAILABLE.
- **foreign_demand_index** — DEFERRED: p0 external AR(1) block NOT wired into active V3 orchestrator (contagion.py uses constant-loadings). HISTORICAL_NOT_AVAILABLE (2026 bridge only).
- **gfc_credit_channel** — DEFERRED: no defensible GFC->credit coefficient.
- **gfc_sovereign_direct_shock** — DEFERRED: direct sovereign shock frozen at 0; reacts endogenously via debt/deficit.
- **global_geopolitical_risk** — DEFERRED: p0 external AR(1) block not wired into active V3 orchestrator. HISTORICAL_NOT_AVAILABLE.
- **global_supply_chain_pressure** — DEFERRED: p0 external AR(1) block not wired into active V3 orchestrator. HISTORICAL_NOT_AVAILABLE.
- **major_climate_disaster_shock** — DEFERRED: climate disasters EXCLUDED from official V3 simulation; official run sets value = 0. MODEL_LATENT_NO_OBSERVED_HISTORY.
- **world_trade_volume** — DEFERRED: p0 external AR(1) block not wired into active V3 orchestrator. HISTORICAL_NOT_AVAILABLE.

### LEGACY_V2_ONLY
The active official V3 Index is the **3-component** `francescope_index_v3` (`v3_index.py`). The older registries describe a **7-component** `FranceScope_Index_RAW` (mean of 7 raw scores). The four extra components and their scores, plus the V2-engine-only macro variables, are retained as the unchanged V2 baseline and are NOT wired into the active V3 orchestrator core.
- FranceScope_Index_RAW — FranceScope Index RAW (7-comp)
- average_net_pension_real — Average net pension (real)
- average_net_pension_real_score — Avg net pension score
- brent_crude_oil_price — Brent oil price
- compensation_per_employee — Compensation per employee
- contributors_per_retiree — Contributors per retiree
- ecb_policy_rate — ECB policy rate
- effective_retirement_age — Effective retirement age
- effective_retirement_age_score — Effective retirement age score
- employment_rate — Employment rate
- energy_import_dependency — Energy import dependency
- energy_inflation — Energy inflation
- euro_area_real_gdp — Euro-area real GDP (V2)
- food_inflation — Food inflation
- france_real_exports — Real exports
- france_real_imports — Real imports
- france_trade_balance — Trade balance
- household_consumption — Household consumption
- housing_cost_burden — Housing cost burden
- housing_cost_burden_score — Housing cost burden score
- inflation — HICP inflation (V2)
- pension_expenditure_gdp — Pension expenditure / GDP
- poverty_rate — Poverty rate
- poverty_rate_score — Poverty rate score
- public_expenditure_gdp — Public expenditure / GDP (V2)
- public_revenue_gdp — Public revenue / GDP (V2)
- real_disposable_income — Real disposable income
- retiree_count_france — Retiree count

## 6. Coverage reconciliation vs code containers

**V3PersistentState** — required fields: 14, missing from inventory: NONE (full coverage)
**V3YearInputs** — required fields: 7, missing from inventory: NONE (full coverage)
**V3YearResult** — required fields: 30, missing from inventory: NONE (full coverage)
**V3 Index scorer** — required fields: 7, missing from inventory: NONE (full coverage)
**MC1000 CORE_FIELDS** — required fields: 25, missing from inventory: NONE (full coverage)

## 7. Known mismatches between code and older registries

- **Index width mismatch (critical):** `FINAL_FRANCESCOPE_VARIABLE_METADATA.csv` / `_COVERAGE.csv` and `p0_future_role_map.csv` describe a **7-component** FranceScope index (real_gdp, unemployment_rate, median_living_standard_real, average_net_pension_real, effective_retirement_age, housing_cost_burden, poverty_rate). The **active** V3 index (`v3_index.py`, used by the official MC1000 run per `FRANCESCOPE_V3_MC1000_RUN_METADATA.csv`) is **3-component**. The 4 extra components are classified LEGACY_V2_ONLY here.
- **External block mismatch:** `p0_future_role_map.csv` and memory record the p0 external AR(1) processes (foreign_demand_index, world_trade_volume, global_geopolitical_risk, external_stress_index, global_supply_chain_pressure) with 2026 anchors. The **active** `external/contagion.py` does NOT use these AR(1) states; it uses constant-loadings (GLOBAL_GROWTH_CENTRAL, EURO_AREA_CONST, FDI_CONST, CYC_LOAD). The p0 AR(1) block is classified DEFERRED_NOT_ACTIVE.
- **China hook:** `contagion.py` reserves a China loading but `CHINA_LOAD = 0.0` (pending calibration). Older narratives list a China coefficient; it is inactive.
- **Credit->investment:** `corporate_credit_rate` is computed (B2 wiring) but is NOT an input to `_v2_investment_growth`; the credit->investment link is deferred (no coefficient).
- **Climate disasters:** the acute `major_climate_disaster_shock` input exists but is set to 0 in the official V3 simulation (climate disasters excluded); only the chronic `CLIMATE_BASELINE_DRAG = -0.001` is active.
- **Fiscal->GDP:** older `p0_future_role_map.csv` treats `public_revenue_gdp` as a V1 regression variable; the active V3 uses `baseline_revenue_2026` + lagged `fiscal_adjustment` reaction (no V1 revenue regression).

## 8. Artifacts produced
- `data/audits/full_data_review/FRANCESCOPE_V3_COMPLETE_VARIABLE_INVENTORY.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_STATIC_PARAMETER_INVENTORY.csv`
- `data/audits/full_data_review/FRANCESCOPE_V3_VARIABLE_DATA_AVAILABILITY.csv`
- `docs/FRANCESCOPE_V3_COMPLETE_VARIABLE_DATA_MAP.md`

## 9. Recommended next task

Build the actual historical / official-forecast / MC1000 distribution **tables** (one row per variable per year) by extracting observed values from the authoritative source files already referenced in this inventory (FranceScope components 2010-2026, master_canonical, financial_canonical, demographic canonical) and the official MC1000 parquet outputs, then validate lineage against the `upstream_dependencies` / `downstream_variables` columns. No recomputation or recalibration is required for that extraction step.
