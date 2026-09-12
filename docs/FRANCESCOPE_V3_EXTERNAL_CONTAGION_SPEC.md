# FranceScope V3 — Correction D1: World / Europe / China / Contagion SPECIFICATION AND CALIBRATION

**Status:** SPEC + CALIBRATION ONLY. V2 forecast code NOT modified. V3 GDP/fiscal/demographic code NOT modified. Trade equations NOT modified.

## 1. EXISTING V2 EXTERNAL ARCHITECTURE (inventory)
| Variable | Formula / source | Unit | Downstream | Class |
|---|---|---|---|---|
| `global_growth` | `ScenarioDriver(central=0.018, unc=0.006, pers=0.6)`, independent `N(0,horizon_unc)` each year | decimal | `europe_factor`, `world_trade`, `compute_real_gdp` | KEEP_WITH_EXTENSION (use as **cyclical deviation**, not permanent trend) |
| `europe_factor` | `0.6·global_growth + N(0,0.01)` | decimal | euro_area/germany/spain/nl/belgium growth | KEEP_WITH_EXTENSION (+common shock) |
| euro_area/germany/spain/nl/belgium growth | `const + 0.3·europe_factor + N(0,idio)` | decimal | `foreign_demand_index`, GDP | KEEP (common factor present; idio retained small) |
| `world_trade_volume` | `×(1 + global_growth + N(0,0.04))` | index | external demand proxy | KEEP_WITH_EXTENSION (+common shock) |
| `foreign_demand_index` (state) | `fdi_growth = 0.008819 + 0.907467·euro_area_growth`; `×(1+fdi_growth)` | index | **exports** (validated) | KEEP (trade transmission layer) |
| `foreign_demand` (local var, `compute_real_gdp`) | `0.8·global_growth − 2.0·trade_fragmentation` | decimal | `growth += 0.3·foreign_demand` | LEGACY_REDUNDANT (drop from V3 GDP; superseded by `external_cyclical_input`) |
| `trade_fragmentation` | `ScenarioDriver(central=0, unc=0.003)` | decimal | `foreign_demand` | KEEP |
| `external_stress_index` | AR(1) mean 0.6632, phi 0.4007, sd 0.5971 (z) | z-score | financing/sanity | KEEP_WITH_EXTENSION (optional load on common shock) |
| `global_geopolitical_risk` | AR(1) mean 107.46, phi 0.4192, sd 23.99 | index | (currently light use) | KEEP |
| `geopolitical_shock` | `ScenarioDriver(central=0, unc=0.012)` | decimal | `compute_real_gdp` | KEEP |
| `oil_price_shock` | `ScenarioDriver` | decimal | `compute_real_gdp` | KEEP |
| `france_real_exports/imports` | validated ex-2020 OLS + error-correction (see §5) | CLV20_MEUR | trade balance identity | KEEP (unchanged) |
| UK GDP/growth | NOT in active V2 loop | — | — | MISSING (not required; France's main partners euro_area/Germany) |
| China GDP/growth | no active variable; `data/raw/oecd/QNA.json` (OECD QNA) includes China | — | future | MISSING (raw present, no download needed) |

## 2. THE V2 PROBLEM (excessive independence / overlap)
- Each external series draws its **own** `np.random.normal` (`global_growth` ScenarioDriver noise, `europe_factor` noise, per-partner idio, `world_trade` noise) → they can diverge unrealistically; no single common external cycle.
- `compute_real_gdp` **double-counts** external: `global_growth` weight = 0.6 direct + 0.8×0.3 (via `foreign_demand`) ≈ 0.84.
- For V3, external must affect **cyclical/external demand**, not permanent structural growth (structural GDP already excludes external levels).

## 3. MINIMAL NORMAL-CYCLE CONTAGION ARCHITECTURE (SELECTED: A)
Introduce exactly **ONE** common input: `external_cycle_shock_t ~ N(0,1)` (future engine draws once per year).
```
global_growth_dev_t = 0.018 + GLOBAL_LOAD·z_t            # GLOBAL_LOAD=0.006
europe_factor_t      = 0.6·global_growth_dev_t + EU_LOAD·z_t   # EU_LOAD=0.006
euro_area_growth_t   = 0.0126 + 0.3·europe_factor_t
fdi_growth_t         = 0.008819 + 0.907467·euro_area_growth_t + CHINA_LOAD·china_growth_gap_t  # CHINA_LOAD reserved, china_gap=0
world_trade_growth_t = global_growth_dev_t + WTV_LOAD·z_t  # WTV_LOAD=0.006
external_stress_index_t += EXT_STRESS_LOAD·z_t            # optional, small
external_cyclical_input_t = CYC_LOAD·z_t                  # CYC_LOAD=0.008 (V3 GDP cyclical hook)
```
Propagation: `z↓` → global↓ → Europe↓ → `foreign_demand_index`↓ → exports↓; and `external_cyclical_input↓` → V3 GDP cyclical↓. Coherent, single latent shock, no new regime.

## 4. CHINA — MINIMAL
Repository raw `data/raw/oecd/QNA.json` contains China (no download). Default: reserve `china_growth_gap_t = 0.0` feeding `fdi_growth` with small `CHINA_LOAD` (later derived from QNA.json). **CHINA_COMPETITIVE_PRESSURE = DEFERRED** (no housing/debt/industrial/tariff model).

## 5. VALIDATED TRADE EQUATIONS — UNCHANGED
Exports: `export_growth = 0.008603 + 0.824370·domestic_gdp_growth + 0.773149·fdi_growth + 0.309779·(0.3162 − exports_gdp_lag)`.
Imports: `import_growth = 0.014986 + 1.984267·consumption_growth − 0.303148·investment_growth + 0.409133·(0.3193 − imports_gdp_lag)`.
Trade balance = exports − imports (identity). These remain the trade transmission layer.

## 6. CANDIDATES
- **A. Existing foreign-demand system + common external-cycle innovation — SELECTED** (minimal code, one shock, no double count, GFC-compatible).
- B. Global-growth gap + Europe factor + China growth gap feeding foreign demand — optional future (adds `china_growth_gap` now).
- C. Existing V2 with only correlated residual innovations — weaker (no named shock; less transparent).

## 7. DOUBLE-COUNTING TREATMENT
V3 structural GDP excludes external. External enters ONLY via `external_cyclical_input` (deviation of `z`, not `global_growth` level). The V2 `foreign_demand` local var in `compute_real_gdp` is dropped for V3 GDP; `foreign_demand_index`/exports kept as trade layer. Both GDP-cyclical and exports derive from the SAME `z` → coherent, no second injection.

## 8. FUTURE INTERFACES
- `external_cyclical_input` → V3 `compose_real_gdp(structural, cyclical_input=...)`.
- `global_financial_crisis_shock` → later sets `z_t` to a large negative (e.g., −4…−6) on the SAME system (no parallel global model).
- `china_growth_gap` → `fdi_growth` (reserved 0).
- `foreign_demand_index`/`europe_factor` → unchanged transmission.

## 9. DETERMINISTIC DIAGNOSTICS (see CSV; no Monte Carlo)
A normal (z=0): external_cyclical≈0, fdi_growth≈ normal.
B moderate slowdown (z=−1): global_growth_dev≈1.2%, euro_area≈1.1%, fdi_growth↓, export input↓, external_cyclical≈−0.8pp.
C China slowdown (z=−0.5, china_gap=−0.02): milder, foreign demand softened further via china_gap.
D broad synchronized (z=−2): global≈0.6%, euro_area≈0.4%, fdi_growth sharply↓, external_cyclical≈−1.6pp.
Later GFC: z=−5 → severe but on same mechanism.

## 10. IMPLEMENTATION LOCATIONS (future)
In V2 loop: replace independent `np.random.normal` draws in `global_growth` sampling, `europe_factor`, `world_trade`, partner idio with loadings on one `external_cycle_shock`. Add `external_cyclical_input` to state; feed V3 `compose_real_gdp`. Replace `compute_real_gdp`'s `global_growth`/`foreign_demand` terms for V3 path. Keep export/import eqs. Add `china_growth_gap` (0) input.
