# FranceScope V3 — IMPLEMENTATION PLAN (dependency-ordered, no code yet)

This plan sequences V3 build to minimise rework. Each stage reuses V2 components where possible and
is gated before the next begins. V2 remains preserved as the benchmark and is not modified.

## TASK 6 — IMPLEMENTATION ORDER

### Stage 0 — Data acquisition layer
- Module: `data/audits` + new ingestion. Depends on: nothing.
- V2 reused: master_canonical ingestion, 43-P0 registry.
- New: INSEE population (total & working-age, migration), OAT-Bund spread, debt maturity,
  public-spending composition, defense, China macro, US/global financial stress, social-unrest,
  climate-damage/disaster, AI exposure, historical-regime labels, event-calibration dates.
- Data: all `NEW_DATA_REQUIRED` / `PARTIAL_DATA` rows in `FRANCESCOPE_V3_DATA_REQUIREMENTS.csv`.
- Tests: source coverage check, vintage/unit consistency.
- Gate: all Stage-1/2/3 priority-1 data present.

### Stage 1 — Demographics & population
- Module: demographic projection block. Depends on: Stage 0.
- V2 reused: retiree_count / retirement_age / contributors_per_retiree projection (extend).
- New: total_population, working-age population, labor-force, migration, dependency ratios.
- Data: INSEE projections.
- Tests: population accounting (births-deaths+migration = Δ); per-capita identity.
- Gate: real_gdp_per_capita computable end-to-end.

### Stage 2 — Potential growth & macro-regime engine (Layer B)
- Module: regime state machine (EXPANSION/SLOWDOWN/RECESSION/CRISIS/RECOVERY). Depends on: Stage 1,
  V2 GDP/potential transmission (KEEP_WITH_EXTENSION).
- V2 reused: productivity driver, Okun unemployment (feed regime), inflation eqs.
- New: persistent multi-variable regime state replacing independent additive shocks
  (REPLACE gdp_growth_transmission_architecture, independent_shock_event_architecture).
- Data: historical regime labels (NBER-like/OECD CLI) for calibration.
- Tests: regime transition matrix valid; recessions persist >1 year; crisis-direction.
- Gate: regime system produces realistic recession frequency (not ~0).

### Stage 3 — Sovereign debt & fiscal reaction (chains 1, 2, 3)
- Module: debt/spread/fiscal block. Depends on: Stage 2, Stage 0 spread/maturity data.
- V2 reused: debt stock-flow, interest, revenue (KEEP).
- New: debt→spread feedback (REPLACE sovereign_yield_determination), fiscal reaction function
  distinguishing expenditure types (REPLACE fiscal_expenditure_process), sovereign-bank nexus.
- Data: OAT-Bund spread, debt maturity, spending composition, historical consolidations.
- Tests: debt accounting; spread responds to debt; consolidation raises revenue/cuts spend;
  sovereign stress tightens credit.
- Gate: debt spiral and consolidation both attainable in paths.

### Stage 4 — International regime & contagion (chains 4, 5, 6)
- Module: world/euro/China block. Depends on: Stage 2.
- V2 reused: euro-area/german/spain/nl/be processes, foreign-demand bridge (extend).
- New: US/global financial stress variable, China slowdown + overcapacity channel,
  shared ECB/financial regime, German-weakness propagation.
- Data: US/global FSIs, China macro/CPB, ECB regime.
- Tests: global crisis lowers French exports/GDP; China shock hits competitiveness.
- Gate: correlated international downturns appear in paths.

### Stage 5 — Climate, defense, geopolitics, energy (chains 7, 8; hazards)
- Module: hazard-state system (Layer C). Depends on: Stage 2, Stage 0.
- V2 reused: climate_damage, energy/oil eqs (extend), geopolitical AR1 (extend).
- New: acute disaster state, chronic sectoral damage, defense spending loop, nuclear/energy
  availability, war state with energy/trade/confidence channels.
- Data: climate damage/disaster, SIPRI/MINARM, RTE/EDF, GPR.
- Tests: disaster destroys capital + raises fiscal; defense crowds out civilian investment.
- Gate: hazard states trigger with state-dependent probabilities.

### Stage 6 — AI, human capital, migration, structural forces
- Module: Layer A residual forces. Depends on: Stage 1, Stage 5.
- V2 reused: none directly (all MISSING).
- New: AI productivity/displacement/inequality/rent-leakage, education/human capital,
  migration, industrial competitiveness/deindustrialization, euro FX, investment composition.
- Data: OECD AI, PISA, INSEE migration/industrial, ECB FX.
- Tests: AI raises productivity but raises inequality; migration lifts labor.
- Gate: structural forces coherent with regime layer.

### Stage 7 — Social/political stress loop (chain 10) & full integration
- Module: social-stress index → unrest → reform-delay → sovereign credibility. Depends on: Stage 2–6.
- V2 reused: poverty/inequality terms (extend). New: social-stress index + feedback to spread.
- Tests: high unemployment+inflation+austerity raises unrest probability.
- Gate: full engine validates accounting + regime + crisis-direction tests.

### Stage 8 — Index V3 (output layer)
- Module: Index from 3 outcomes only. Depends on: Stage 7 validated; Stage 1 for per-capita.
- V2 reused: median_living_standard_real, unemployment_rate outputs.
- New: real_gdp_per_capita (needs population). Scoring methodology = SEPARATE TASK (UNRESOLVED).
- Tests: Index historical 2010–2025 reconstructable; 1,000-path stability.
- Gate: only after macro engine fully validated.

## TASK 7 — VALIDATION REQUIREMENTS (pre-final-2050)

### Accounting tests
debt (stock-flow), deficit (rev−exp), interest (rate×debt), trade (X−M identity),
employment (pop×participation×employment), pensions (retirees×pension),
population (cohort consistency), GDP per capita (gdp/pop).

### Regime tests
expansion, slowdown, recession, recovery, crisis all reachable; **crisis persists ≥2 years**
(multi-variable, not one-year noise).

### Historical stress-pattern tests (qualitative, not date-fit)
GFC 2008–09, euro sovereign crisis, Covid, 2022 energy/inflation shock — engine must be capable of
generating dynamically similar paths.

### Crisis-direction tests
global crisis must NOT raise French investment/GDP absent explicit recovery channel;
sovereign stress must raise spread and lower credit; defense shock must raise debt.

### Distribution tests
recession frequency (non-zero, plausible), crisis frequency, debt-tail behaviour,
unemployment-tail behaviour, GDP-growth distribution (not truncated-optimistic),
cross-country correlation (France↔Germany↔world positive in downturns).

### 1,000-path Monte Carlo stability
P10/P50/P90 stable vs 500 paths; paths coherent (not variable-by-variable percentiles);
seed/antithetic checks; runtime/consistency.

## MAJOR DEPENDENCIES (order-determining)
1. Population/demographics → real_gdp_per_capita & labor force (Stage 1 before Stage 2/8).
2. Potential growth + regime engine → all GDP dynamics (Stage 2 before everything macro).
3. World/euro/China regime → French external demand (Stage 4 after Stage 2).
4. Debt/spread → sovereign-crisis hazard (Stage 3 before Stage 5 sovereign hazards).
5. Social stress → after income/unemployment/fiscal (Stage 7 after Stage 2–6).
6. Index only after macro engine validated (Stage 8 last).

## ARCHITECTURAL CONFLICTS FOUND (V2 vs V3)
- **Additive independent-shock design** (all 11 ScenarioDrivers + AR1 sampled independently) is
  structurally incompatible with V3's coherent regime + hazard-state architecture — must be REPLACED,
  not extended. This is the primary cause of "too optimistic, no recessions."
- **Sovereign yield = f(ECB only)** breaks the debt↔spread↔bank loop; V3 requires debt/spread feedback.
- **Primary expenditure exogenous AR1** contradicts V3 fiscal-reaction loop; must be replaced.
- **No population in engine** blocks the required real_gdp_per_capita outcome.
