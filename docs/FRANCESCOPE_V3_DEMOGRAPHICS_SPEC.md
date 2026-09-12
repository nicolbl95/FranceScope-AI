# FRANCESCOPE V3 — DEMOGRAPHICS & POPULATION / LABOR-SUPPLY SPEC

Foundation block for V3. Feeds total_population, working_age_population, labor_force, dependency_ratio,
retiree_count_france, migration, potential_growth, employment/unemployment, pensions, health/dependency
costs, real_gdp_per_capita. No V2 code modified; no engine implemented. Institutional DEMOGRAPHIC
projections are permitted as structural inputs (only institutional forecasts of final FranceScope
economic outcomes are prohibited).

## 1. INVENTORY OF EXISTING DATA (targeted inspection of master_canonical.parquet + DREES/Eurostat)
- **retiree_count_france** — DREES F01_Tableau_1, annual, thousand persons, 2004–2023 (16309 in 2023). Used in V2 (own trend process). Usable V3 as cross-check; should be re-derived demographically.
- **contributors_per_retiree** — DREES F01_Graphique_1, annual, ratio, 2004–2023 (1.87). Used in V2 (derived accounting). Usable V3.
- **average_net_pension_real** — DREES F05_Tableau_1, annual, EUR-2023, 2008–2023 (1692). V2 P0 output. Usable V3.
- **effective_retirement_age** — V2/projected, annual, years, 2004–2025 (63.13). V2 output. Usable V3 (endogenous demographic-fiscal).
- **life_expectancy** — INSEE/Eurostat, annual, years, 2010–2024 (83.0). EXISTS in canonical. Usable V3 (low uncertainty).
- **labor_force_participation_rate** — P0, quarterly→annual, %, 2010–2026 (81.5). V2. Usable V3 (endogenous economic).
- **employment_rate / underemployment_rate** — P0, 2010–2026. V2. Usable V3.
- **old_age_dependency_ratio** — ABSENT from canonical (Eurostat demo_pjangroup flagged missing in coverage audit). Treat as NEW_DATA_REQUIRED (or derive from age structure).
- **ABSENT (NEW_DATA_REQUIRED):** total_population, working_age_population, labor_force (level), net_migration, fertility, age structure (cohort bands), mortality disaggregation.

## 2. V3 DEMOGRAPHIC STATE SET (minimal sufficient)
Avoid redundancy: do not keep both active_population and working_age_population; retirees are derived
from old-age population + retirement age, not an independent trend. Proposed states:
- **total_population** (observable/structural EXOGENOUS driver) — persons.
- **working_age_population** (derived) — persons; = total_population × working_age_share.
- **old_age_population** (derived/structural) — persons; from age structure (65+).
- **labor_force** (derived) — persons; = working_age_population × participation_rate.
- **retirees (retiree_count_france)** (derived) — thousand persons; from old_age_population × eligibility(retirement_age).
- **dependency_ratio** (derived) — ratio; = (total_population − working_age_population)/working_age_population.
- **net_migration** (structural + stochastic) — persons/yr.
- **life_expectancy** (observable) — years.
- **effective_retirement_age** (endogenous, from V2) — years.
- **participation_rate** (endogenous, from V2 P0) — %.
- **aging_health_dependency_pressure** (latent index) — driven by old_age_population & life_expectancy.

## 3. IDENTITIES (definitions supported by project data)
- labor_force = working_age_population × participation_rate
- employment = labor_force × (1 − unemployment_rate)
- dependency_ratio = (total_population − working_age_population) / working_age_population  (working_age defined 20–64, INSEE-compatible)
- real_gdp_per_capita = real_gdp / total_population  (unit identity: EUR / person)
- contributors_per_retiree = contributors / retirees, with contributors ≈ employed population × coverage (~0.9); keep DREES ratio as anchor
- retiree_count_france = old_age_population × eligibility_fraction(retirement_age)
- contributors ≈ employment × coverage_factor
All denominators use INSEE-compatible age definitions; no mix of active-population vs 20–64 bands.

## 4. DATA GAPS
- total_population: **NEW_DATA_REQUIRED** (INSEE population projections, annual 2000–2050).
- working_age_population: **NEW_DATA_REQUIRED** (INSEE age bands) — or derive from total × INSEE working-age share.
- labor_force (level): **EXISTING_NEEDS_TRANSFORMATION** (derive from WAP × participation_rate; WAP NEW).
- net_migration: **NEW_DATA_REQUIRED** (INSEE/INSEE-IFE).
- age structure / cohort bands: **NEW_DATA_REQUIRED** (INSEE "scénarios de population" by age/sex).
- old_age_dependency_ratio: **NEW_DATA_REQUIRED / derivable** from age structure.
- retiree_count_france, contributors_per_retiree, life_expectancy, participation, employment, effective_retirement_age, average_net_pension_real: **EXISTING_SUFFICIENT**.

## 5. POPULATION PROJECTION METHODOLOGY
**Hybrid A+B.** Adopt INSEE official demographic projection (central scenario: total population by
age/sex, working-age 20–64, old-age 65+) as an **EXOGENOUS STRUCTURAL DRIVER** (option A). Within V3,
enforce **cohort consistency (option B)**: derive retirees from old-age population × retirement-age
eligibility, and labor_force from working-age × participation. Net migration enters as a structural base
(INSEE assumption) plus a **stochastic amplitude overlay** for scenario variation. This is defensible and
avoids independent-trend contradictions. Not a naive linear extrapolation.

## 6. MIGRATION
net_migration = INSEE base flow + stochastic scenario amplitude (structural + stochastic). Affects
total_population, working_age_population (migrant age profile skews working-age), labor_force,
contributors, consumption, public-service demand. **No welfare sign assigned**; affects labor supply and
fiscal demand symmetrically. Amplitude variation allowed across MC paths.

## 7. AGING / HEALTH-DEPENDENCY CHANNEL
Define **aging_health_dependency_pressure** (latent index, 0–1 normalized) driven by
old_age_population / working_age_population (or 65+ share) and life_expectancy (disability duration).
Parsimonious; feeds government spending (health/LTC) and fiscal_consolidation_pressure. No coefficients
assigned; existing old_age_dependency_ratio (if ingested) may anchor it.

## 8. RETIREE COUNT CONSISTENCY VERDICT
**REPLACE WITH DEMOGRAPHICALLY DERIVED PROCESS.** V2 projected retiree_count_france via an independent
trend (`compute_retiree_count`), which can diverge from population/labor-force support and leave
contributors_per_retiree implausibly fixed. V3 must derive retirees from old_age_population ×
eligibility(retirement_age), keeping V2 series as a calibration cross-check only.

## 9. UNCERTAINTY (2027–2050)
- mortality / life_expectancy: LOW uncertainty (smooth).
- fertility: MODERATE (drives long-run totals).
- net_migration: HIGHER (scenario amplitude, correlated with working_age_population).
- participation_rate: ECONOMIC/ENDOGENOUS (regime-dependent), not demographic.
- Correlation: migration↔working_age_population positive; life_expectancy↔mortality trivial; no strong
  cross-demographic correlation required beyond migration–working-age.

## 10. CALIBRATION CONTRACT
See `FRANCESCOPE_V3_DEMOGRAPHIC_CALIBRATION_PLAN.csv` (one row per state: historical variable, source,
unit, history period, projection approach, structural/stochastic, parameters, dependencies, validation).

## 11. VALIDATION REQUIREMENTS (pre-code acceptance)
population>0; working_age_population ≤ total_population; labor_force ≤ working_age_population (compatible
definitions); retirees consistent with 65+ population & retirement age; dependency_ratio identity exact;
contributors/retirees internally coherent; no one-year population jumps without migration/event cause;
2026 state reconciles with V2 bridge where definitions overlap; GDP-per-capita unit identity exact once GDP
connected; 2050 levels consistent with INSEE structural assumptions. No validation against desired
FranceScope outcomes.

## 12. IMPLEMENTATION PLAN (D1–D6, future coding tasks — not implemented now)
D1 demographic data ingestion (INSEE total/age/migration) → D2 canonical annual panel → D3 projection /
structural demographic driver (INSEE scenario + cohort consistency) → D4 migration uncertainty overlay →
D5 retiree/labor-force integration (replace V2 retiree process) → D6 demographic validation (all tests).
Details in `FRANCESCOPE_V3_DEMOGRAPHIC_IMPLEMENTATION_PLAN.csv`.
