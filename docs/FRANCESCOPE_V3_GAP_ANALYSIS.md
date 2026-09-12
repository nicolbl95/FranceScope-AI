# FranceScope V3 — V2→V3 GAP ANALYSIS

Formal gap analysis performed on the **CURRENT (frozen) V2 baseline**. No V2 code, equations, or
outputs were modified. V2 remains the benchmark. V3 will use 1,000 coherent Monte Carlo trajectories;
P10/P50/P90 remain actual simulation paths.

## TASK 1 — V2 ENGINE INVENTORY (authoritative)

V2 macro engine lives in `scripts/build_probabilistic_forecast_v2.py` (2,284 lines). Registries in
`data/audits/economic_system/` (variable_registry.csv, exact_p0_variables.json, feedback_loops.json,
relationship_registry.csv, p0_future_role_map.csv) confirm the inventory.

### P0 variables (43, frozen)
- **production_demand (6):** real_gdp, household_consumption, investment, france_real_exports,
  france_real_imports, france_trade_balance
- **labour_income (7):** unemployment_rate, employment_rate, labor_force_participation_rate,
  underemployment_rate, compensation_per_employee, private_sector_real_net_salary_eqtp,
  real_disposable_income
- **prices_monetary (7):** inflation, ecb_policy_rate, france_10y_government_rate,
  mortgage_new_business_rate, energy_inflation, food_inflation, brent_crude_oil_price
- **credit_financial (5):** corporate_credit_rate, external_stress_index, global_geopolitical_risk,
  global_supply_chain_pressure, world_trade_volume
- **public_finance (5):** public_revenue_gdp, public_deficit_gdp, public_debt_gdp,
  public_interest_expenditure_gdp, public_expenditure_gdp
- **sovereign_financing (2):** france_10y_government_rate (dup), public_debt_gdp (dup)
- **housing (2):** mortgage_new_business_rate (dup), housing_cost_burden
- **demography_pensions (5):** retiree_count_france, contributors_per_retiree,
  average_net_pension_real, pension_expenditure_gdp, effective_retirement_age
- **trade_external (6):** euro_area_real_gdp, germany_real_gdp, spain_real_gdp,
  netherlands_real_gdp, belgium_real_gdp, foreign_demand_index
- **energy (1):** energy_import_dependency

### Internal state variables / drivers NOT exposed as P0
11 `ScenarioDriver` futures: productivity_growth, climate_damage, retirement_age, global_growth,
trade_fragmentation, oil_price_shock, geopolitical_shock, ecb_rate, fiscal_stress,
supply_chain_pressure, brent_growth. 5 AR(1) state processes: external_stress_index,
global_geopolitical_risk, world_trade_volume, foreign_demand_index, brent_crude_oil_price.
Computed scalars: real_wage_growth, unemployment_change_pp, gdp_growth_rate, effective_rate,
europe_factor, germany_gdp_share. (Full list in
`FRANCESCOPE_V3_INTERNAL_DRIVER_INVENTORY.csv`.)

### Stochastic shocks
All 11 ScenarioDrivers + the 5 AR(1) residuals + residual normal noise in `europe_factor`
(global_growth*0.6+N(0,0.01)) and `wtv_growth` (global_growth+N(0,0.04)). Each is sampled
**independently per year** — the root cause of "trend + annual noise" behaviour.

### Feedback loops (per feedback_loops.json)
debt→financing-cost→deficit (moderate); consumption→production→employment→income (strong);
inflation→rates→demand (strong); housing→credit→demand (moderate);
ageing→pensions→fiscal (weak); weak-growth→revenue→deficit→debt (moderate).
**No sovereign→spread→bank→credit loop; no fiscal reaction function.**

### Cross-country variables
euro_area, germany, spain, netherlands, belgium (evolve as global_growth*0.6+noise);
foreign_demand_index (AR1 of euro_area_growth); world_trade_volume; global_growth.
**No US, no China.**

### Demographic variables
retiree_count_france, contributors_per_retiree, average_net_pension_real, effective_retirement_age,
old_age_dependency_ratio, pension_expenditure_gdp, labor_force_participation_rate,
employment_rate, underemployment_rate. **No total_population, no working-age population, no migration.**

### Climate variables
climate_damage (driver), energy_inflation, food_inflation, brent_crude_oil_price,
global_supply_chain_pressure, energy_import_dependency. **No acute disaster state; no sectoral damage.**

### Fiscal variables
public_revenue_gdp (AR1), primary_expenditure_gdp (exogenous AR1), public_interest_expenditure_gdp,
public_expenditure_gdp, public_deficit_gdp, public_debt_gdp, effective_rate, france_10y_government_rate.

### Financial variables
ecb_policy_rate, france_10y_government_rate (= f(ecb_rate) only), mortgage_new_business_rate,
corporate_credit_rate, external_stress_index, global_geopolitical_risk, global_supply_chain_pressure,
world_trade_volume, foreign_demand_index.

### Regime-like logic
**NONE.** Only a code comment ("low-unemployment regime"). Recessions are implicit one-year Gaussian
deviations, not a persistent state machine.

### Crisis / event logic
**NONE.** oil_price_shock, geopolitical_shock, fiscal_stress are additive Gaussian noise on GDP —
not state-dependent events with probabilities.

## TASK 2 — MECHANISM CLASSIFICATION (60 mechanisms)
Full detail in `FRANCESCOPE_V3_GAP_ANALYSIS.csv`.

- **EXISTS (4):** debt_stock, effective_debt_cost, sovereign_interest_burden, unemployment_rate_outcome
- **PARTIAL (22):** demographic_aging, labor_force_trend, dependency_ratio, health_dependency_aging_costs,
  potential_growth, productivity, capital_accumulation, chronic_climate_damage,
  global_trade_slowdown_fragmentation, european_structural_slowdown, french_energy_nuclear,
  france_fiscal_stress, war_geopolitical_escalation, energy_shock, sovereign_debt_loop,
  global_contagion, europe_regime, climate_loop, defense_geopolitics_loop,
  social_political_stress_loop, median_living_standard_loop, median_living_standard_outcome
- **MISSING (30):** total_working_age_population, human_capital_education, fiscal_consolidation_pressure,
  taxation_spending_adjustment, climate_adaptation, defense_spending, investment_composition,
  industrial_competitiveness, deindustrialization, china_slowdown_overcapacity, migration,
  euro_exchange_rate, ai_structural_effects, macro_regime_system, global_financial_crisis,
  france_sovereign_stress, france_sovereign_crisis, banking_credit_crisis, major_climate_disaster,
  severe_social_unrest, pandemic, cyber_infrastructure_shock, ai_boom, ai_financial_bust,
  fiscal_reaction_loop, sovereign_bank_nexus, china_channel, ai_loop, real_gdp_per_capita_loop,
  real_gdp_per_capita_outcome
- **REPLACE (4):** gdp_growth_transmission_architecture, fiscal_expenditure_process,
  sovereign_yield_determination, independent_shock_event_architecture

## TASK 3 — REUSABLE V2 COMPONENTS
**KEEP:** public debt stock-flow accounting; deficit/expenditure accounting; interest-expenditure
(effective_rate) block; compensation Model B; public-revenue AR1; inflation/energy/food equations;
historical data ingestion (master_canonical); 1,000-path Monte Carlo infrastructure & P10/P50/P90 path
identity; diagnostics framework; 43-P0 + relationship registries.
**KEEP_WITH_EXTENSION:** GDP/potential transmission (add regime); foreign-demand/trade bridge;
demographic retiree projection (extend to total population); unemployment Okun equation (feed regime);
median-living-standard reduced-form (decompose to wages/pensions/transfers/taxes).
**REPLACE:** gdp_growth_transmission_architecture; fiscal_expenditure_process (primary AR1 → reaction
function); sovereign_yield_determination (ecb-only → debt/spread feedback);
independent_shock_event_architecture (independent noise → regime + hazard states).

## TASK 4 — INTERNAL V2 DRIVERS NOT EXPORTED
22 internal drivers identified (see `FRANCESCOPE_V3_INTERNAL_DRIVER_INVENTORY.csv`): the 11 ScenarioDrivers,
5 AR(1) states, and computed scalars (real_wage_growth, unemployment_change_pp, gdp_growth_rate,
effective_rate, europe_factor, germany_gdp_share, brent_crude_oil_price). **Recommendation: all 11
ScenarioDrivers + 5 AR(1) states + real_wage_growth/gdp_growth_rate/effective_rate/unemployment_change_pp
MUST be exposed in V3 diagnostic outputs** so regime/event propagation is auditable; germany_gdp_share
optional.

## TASK 8 — INDEX V3 DEPENDENCY NOTES (scoring UNRESOLVED)
**Official outcomes (only these):** real_gdp_per_capita, median_living_standard_real, unemployment_rate.
- Historical series needed: real_gdp (exists), total_population (NEW — required for per-capita),
  median_living_standard_real (exists, P0), unemployment_rate (exists, P0).
- Common historical period available: 2010–2025 (P0 coverage); population requires INSEE extension.
- Population requirement: total_population + working-age population are mandatory for real_gdp_per_capita.
- Direction: higher real_gdp_per_capita ↑, higher median_living_standard_real ↑, lower unemployment_rate ↑.
- Double-counting: median_living_standard and real_gdp_per_capita share wage/income channels — scoring
  must avoid duplicate loading; unemployment is partly embedded in both.
- Legacy: the old 7-component Index (added poverty_rate, average_net_pension_real,
  effective_retirement_age, housing_cost_burden, real_gdp_total) is now **legacy only**; those variables
  remain in the macro engine/dashboard but are NOT Index components.

**SCORING METHODOLOGY: UNRESOLVED — SEPARATE V3 INDEX TASK REQUIRED.**
