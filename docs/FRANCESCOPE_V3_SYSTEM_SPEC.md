# FRANCESCOPE V3 — FORMAL SYSTEM SPECIFICATION

Authoritative architecture for all later V3 implementation tasks. Based on the completed V2→V3 gap
analysis (`docs/FRANCESCOPE_V3_GAP_ANALYSIS.md` and companion CSVs). **No coefficients are assigned.**
V2 remains the preserved baseline and is not modified.

## FROZEN PRODUCT DECISONS
- Final Index outcomes (only 3): **real_gdp_per_capita**, **median_living_standard_real**,
  **unemployment_rate**. Conceptually equal weight (1/3 each), but **SCORING / NORMALIZATION =
  UNRESOLVED — SEPARATE INDEX V3 TASK**.
- Removed from Index but kept as model/dashboard variables: poverty_rate, average_net_pension_real,
  effective_retirement_age, housing_cost_burden, real_gdp total (plus debt, deficit, inflation, etc.).
- Monte Carlo: **1,000 coherent trajectories**; P10/P50/P90 are ACTUAL complete simulation paths.
- No "France must be worse in 2050". Mechanisms are economically defensible; uncertainty is mostly
  AMPLITUDE, not existence. Aging, chronic climate damage, debt pressure, defense burden exist in ALL
  paths with trajectory-varying severity.

## 1. LAYER A — STRUCTURAL STATES / FORCES
Persistent slow-moving states (full list in `FRANCESCOPE_V3_STATE_REGISTRY.csv`). Each state carries:
state name, concept, unit, endo/exo/derived, process (deterministic trend or stochastic),
parents, children, timescale, V2-part, new-data flag. Highlights:
- **total_population / working_age_population / labor_force / retirees / dependency_ratio** —
  NEW (V2 has no population); deterministic cohort + stochastic migration.
- **potential_growth / productivity_trend / capital_accumulation / human_capital** — potential_growth
  partly via V2 productivity_growth driver; capital/human-capital NEW.
- **debt_stock / effective_debt_cost / sovereign_interest_burden** — EXISTS in V2 (KEEP).
- **fiscal_consolidation_pressure / tax_pressure** — NEW latent (drives fiscal reaction).
- **chronic_climate_damage / climate_adaptation** — chronic_damage PARTIAL in V2; adaptation NEW.
- **defense_spending / productive_public_investment / investment_composition** — NEW.
- **industrial_competitiveness / deindustrialization_trend** — NEW.
- **global_trade_fragmentation / euro_area_structural_growth / china_structural_growth /
  china_overcapacity / french_energy_nuclear_availability / euro_exchange_rate** — mostly NEW;
  trade_fragmentation PARTIAL in V2.
- **ai_productivity_gain / ai_job_displacement / ai_inequality_pressure / ai_foreign_rent_leakage** —
  NEW; uncertainty on amplitude, existence in trajectories optional (boom/bust hazards cover extremes).

## 2. MACRO REGIME SYSTEM (Layer B)
One persistent French regime state ∈ {EXPANSION, SLOWDOWN, RECESSION, CRISIS, RECOVERY}.
- EXPANSION: strong GDP, high investment, low unemployment, easy credit, mild inflation, improving fiscal.
- SLOWDOWN: sub-potential growth, slowing investment, rising unemployment, tightening credit.
- RECESSION: negative actual growth, falling investment/employment, credit stress, fiscal deterioration.
- CRISIS: severe contraction + financial/sovereign stress, collapsing credit, surging spread.
- RECOVERY: positive growth returning, investment rebuilding, unemployment peaking then falling.
Transition hazard depends on: financial_stress, sovereign_stress, global_regime, investment weakness,
unemployment trend, credit stress, geopolitical_shock, climate_disaster, banking_credit_stress.
Allowable transitions: EXPANSION→SLOWDOWN; SLOWDOWN→EXPANSION|RECESSION; RECESSION→CRISIS|RECOVERY;
CRISIS→RECOVERY; RECOVERY→EXPANSION|SLOWDOWN. **Persistence** enforced by duration counters / AR(1)
so a regime lasts multiple years (no isolated one-year "fake recessions").

## 3. EVENT / HAZARD STATES (Layer C)
14 hazards (`FRANCESCOPE_V3_HAZARD_REGISTRY.csv`): global_financial_crisis, france_fiscal_stress,
france_sovereign_stress, france_sovereign_crisis, banking_credit_crisis, geopolitical_escalation,
war_escalation, energy_shock, major_climate_disaster, severe_social_unrest, pandemic,
cyber_infrastructure_shock, ai_boom, ai_bust. Each: binary/multi/continuous severity; triggering
parents (system-state dependent, NOT fixed dates); affected variables; persistence/duration;
recovery mechanism; international correlation flag; V2 partial analogue. Hazards EMERGE from state;
never scheduled by scenario.

## 4. GLOBAL / INTERNATIONAL ARCHITECTURE
Nodes: GLOBAL regime, US, euro area, Germany, China, world trade, financial stress, energy/geopolitical
environment. Propagation: global financial stress → US/markets/credit → world trade → China/Europe/
Germany → French foreign demand → exports/investment/GDP. **China dual channel:** (A) demand via
world trade; (B) overcapacity/industrial competition → french industrial_competitiveness (negative).
**Europe:** shared demand + shared ECB/financial channel + Germany linkage + common recession/crisis
regime where appropriate. Correlated: global financial crisis, European downturn, energy/geopolitical,
world trade, sovereign spreads, China/Europe industrial shock. Idiosyncratic: France-specific social
unrest, cyber, pandemic local severity.

## 5. SOVEREIGN / FISCAL SYSTEM
Core loop: debt → effective_debt_cost → interest_expense → deficit → debt. Extended:
debt/deficit/interest/political-credibility → France-Germany spread → sovereign financing cost →
bank/corporate financing → investment/consumption → GDP → public revenue → debt. Fiscal reaction:
high debt/deficit/spread → spending adjustment AND/OR taxation → disposable income/consumption/
investment → GDP → revenue. **Expenditure categories distinguished conceptually (no microsim yet):**
transfers, current government consumption, productive public investment, defense, climate repair/
adaptation, health/dependency. Causal direction documented; cuts to productive investment hurt
potential growth more than transfers.

## 6. SOVEREIGN-BANK NEXUS
sovereign_stress → bank funding/balance-sheet stress → tighter household/business credit →
construction/investment/consumption → GDP/employment. Interacts with ECB (funding), France-Germany
spread, corporate_credit_rate, mortgage_rate, and banking_credit_crisis hazard. Sovereign stress
raises bank funding cost → raises credit rates → lowers activity (two-way with debt loop).

## 7. CLIMATE ARCHITECTURE
**chronic_climate_damage:** slow trend → labor productivity, agriculture, infrastructure, health,
insurance, fiscal spending, capital depreciation (exists in ALL paths, severity varies).
**climate_disaster_shock:** rare/severe → capital stock, output, fiscal expenditure, insurance/credit,
confidence. Damage accumulates; adaptation offsets; recovery via reconstruction; hazard/severity rise
over time. Optimistic paths still carry positive chronic damage.

## 8. DEFENSE / GEOPOLITICS
Defense spending channels: short-run + government demand, domestic industry, employment, R&D spillovers,
defense exports; long-run − debt, − taxes, crowding-out of productive civilian investment, fiscal
opportunity cost. War/geopolitical escalation additionally → energy prices, trade, supply chains,
confidence, defense expenditure, migration, fiscal stress. Net sign NOT assumed.

## 9. AI ARCHITECTURE
ai_productivity_gain → productivity; ai_job_displacement → employment composition/unemployment;
ai_inequality_pressure → distribution; ai_foreign_rent_leakage → domestic income leakage;
ai_financial_bubble_risk → financial hazard (ai_boom / ai_bust). AI ≠ simple productivity+.

## 10. SOCIAL / POLITICAL STRESS
Latent **social_stress** ← unemployment, real-income pressure, tax rises, spending cuts, inflation,
inequality, poverty, pension/reform pressure. social_stress → severe_social_unrest hazard → activity/
confidence/consumption/investment, and → reform delays → weaker fiscal consolidation → sovereign
credibility/spread. No party assumptions.

## 11. DEMOGRAPHICS
total_population, working_age_population, labor_force, retirees, migration, dependency_ratio,
life expectancy. Identities: labor_force = working_age × participation; retirees drive pension spend;
population feeds labor, pensions, consumption, fiscal, health costs. **real_gdp_per_capita =
real_gdp / total_population** (correct units). Mandatory population subsystem (NEW).

## 12. POTENTIAL vs ACTUAL GDP
actual_real_gdp_growth = potential_growth + cyclical_regime_effect + structural_drag_effects
(climate/competitiveness/debt) + event_shocks + recovery_effects. potential_growth depends on
labor-force trend, productivity, capital, human capital, AI, competitiveness, chronic climate damage.
Actual GDP is NO LONGER "positive trend + independent annual noise".

## 13. MEDIAN LIVING STANDARD V3
disposable household resources = labor income + pensions + transfers + property/asset income −
taxes/social contributions → distribution adjustment → median_living_standard_real. V2 has
reduced-form (gdp+productivity+wage−unemployment) and pension/wage pieces; MISSING: explicit transfers,
asset income, tax decomposition. Reduced-form may remain as bridge until decomposed.

## 14. UNEMPLOYMENT V3
Extend Okun with regime dependence, lagged adjustment, participation, hysteresis, AI displacement,
recovery dynamics. No instant reversion to one fixed natural rate.

## 15. REMOVED-FROM-INDEX VARIABLES
poverty_rate, average_net_pension_real, effective_retirement_age, housing_cost_burden, real_gdp total,
debt, deficit, inflation, pensions, trade, investment, consumption — remain model/dashboard outputs
explaining Index outcomes; not direct components.

## 16. YEARLY SIMULATION ORDER
Dependency-safe order (full detail `FRANCESCOPE_V3_SIMULATION_ORDER.csv`):
1. carry previous-year state; 2. update deterministic structural trends (population, potential, debt
cost, chronic climate); 3. update global/international regime & nodes (GLOBAL, US, Euro, Germany, China,
world trade, financial stress); 4. evaluate hazard probabilities from state; 5. realize events/hazards;
6. determine French macro regime transition (uses global_regime, financial/sovereign/credit stress);
7. update potential growth; 8. update financial/sovereign conditions (spread, rates, credit);
9. update fiscal reaction (expenditure type split + taxation); 10. update real economy (GDP via
potential+regime+events, consumption, investment, trade); 11. update labor (employment, unemployment,
participation); 12. update inflation/monetary/credit; 13. update public-finance identities
(revenue→deficit→debt, accounting Form A, uses t-1 debt); 14. update pensions/demographics;
15. update household income / median living standard; 16. compute secondary outputs; 17. compute
FranceScope outcomes (3); 18. save diagnostic states. Feedback loops use t-1 / sequential update /
accounting identity — no circular within-year dependencies.

## 17. STATE PERSISTENCE
macro_regime, global_regime, social_stress, sovereign_stress, financial_stress, climate-disaster
recovery: duration counter + AR(1). Avoids one-year crisis → instant normalization.

## 18. CORRELATION ARCHITECTURE
Shared latent factors: global financial stress, European downturn, energy/geopolitical, world trade,
sovereign spreads, China/Europe industrial shock. Common factor drives correlated realizations;
idiosyncratic residuals remain for France-specific hazards. Covariance matrix deferred to calibration.

## 19. DIAGNOSTIC EXPORT
Every path exposes: macro_regime, global_regime, potential_growth, productivity_growth, population,
working_age_population, labor_force, climate_chronic_damage, climate_disaster_state, geopolitical_state,
defense_spending, fiscal_stress, sovereign_stress, France-Germany spread, banking_credit_stress,
social_stress, AI states, crisis/event flags, global_growth, world_trade, China state, Europe state.

## 20. MINIMUM VIABLE ARCHITECTURE
CORE_V3 = 36 mechanisms (fixes the 4 principal V2 failures: excessive trend growth, no true recessions,
weak debt feedback, weak global contagion, plus required Index). SECONDARY_V3 = 22 (layered after core,
before final Index). OPTIONAL_LATER = 2 (human_capital_education, ai_structural_effects general).
See `FRANCESCOPE_V3_MECHANISM_REGISTRY.csv`.

## 21. MODULE BOUNDARIES
14 modules (`FRANCESCOPE_V3_MODULE_PLAN.csv`): demographics, regimes, hazards, global_system,
sovereign_fiscal, banking_credit, climate, geopolitics_defense, ai, social_stress, macro_transmission,
household_income, diagnostics, simulation_orchestrator. Each with responsibility/inputs/outputs/
V2-reused/forbidden. No single giant V3 script.

## 22. VALIDATION GATES
A architecture accepted (no code before); B deterministic mechanism direction tests; C historical/stress
patterns (GFC, euro crisis, Covid, 2022 energy/inflation) qualitative; D ~100-path MC numerical;
E 1,000-path distribution (recession/crisis frequency, debt/unemployment tails, cross-country corr);
F Index V3 frozen only after engine accepted.

## 23. WHAT V3 MUST NOT DO
No arbitrary 2050 targets; no manual P10/P50/P90 scheduling; no clipping to hide forecasts; no
institutional-forecast injection into outcomes; no independent-shock architecture where systemic
correlation required; no silent diagnostic states; no changing Index scoring after seeing results;
no calibration solely to force pessimism.

## 24. INDEX V3
Outcomes: real_gdp_per_capita (↑ better), median_living_standard_real (↑ better), unemployment_rate
(↓ better). Conceptual 1/3 each. **SCORING / NORMALIZATION = UNRESOLVED — SEPARATE INDEX V3 TASK.**
