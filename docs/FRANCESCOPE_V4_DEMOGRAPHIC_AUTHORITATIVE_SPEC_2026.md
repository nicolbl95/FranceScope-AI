# FranceScope V4 — Authoritative Demographic Data Specification (pre-implementation)

**Status**: FROZEN specification, pre-implementation.
**Created**: 2026-09-02.
**Purpose**: Lock the demographic data lineage, vintage, transition rules and age-band definitions that FranceScope V4 must use for the final forecast. **No code, data or equation is changed by this document.**

---

## 1. Authoritative INSEE dataset / version

| Layer | Authoritative source | Vintage label to use |
|---|---|---|
| Observed / recent-estimate levels and rates, 2000 → 2026 | **INSEE — Bilan démographique 2025** (Insee Première n°2087, **published 2026-01-13**) + **INSEE Résultats "La situation démographique en 2025 et en séries longues"** (published **2026-06-15**); population tables POP1, POP3, POP4, POP5 | `INSEE Bilan démographique 2025 (publié 2026-01-13) + Situation démographique 2025 (publié 2026-06-15)` |
| Institutional projection, **2027 → 2070** | **INSEE — Projections de population 2026-2070**, scénario central (**published 2026-06-08**), Insee Première n°2108 | `INSEE Projections de population 2026-2070 (publié 2026-06-08), scénario central` |

The 2021 INSEE projection ("Projections de population 2021-2070, publié 2021-11-29") currently used in `francescope_v3_demographic_canonical.csv` is **SUPERSEDED** and must no longer drive V4.

### Central-scenario hypotheses (frozen)

| Component | Value | Source |
|---|---|---|
| Total fertility rate (ICF) | central = **1.45**; convergence at horizon **2028**; scenarios ±0.25 around 1.45 | Insee, Blanpain et al. 2026-04 |
| Life expectancy at birth (women) | reaches **89.5 yr in 2070** (+3.6 vs 2025) | Insee 2026-06-08, central |
| Life expectancy at birth (men) | reaches **86.7 yr in 2070** (+6.4 vs 2025) | Insee 2026-06-08, central |
| Net migration | **+150,000 / yr constant from 2026 onward**; scenarios ±80,000 | Insee 2026-06-08, central |
| Mean age at motherhood | rises from 31.2 (2025) to **33.0 yr in 2050**, then stabilizes | Insee 2026-06-08, central |
| Old-age dependency ratio (65+ / 20-64) | 40 / 100 in 2026; **49 / 100 in 2040**; 62 / 100 in 2070 | Insee 2026-06-08, central |

### Alternative INSEE scenarios to retain

`esperance_vie_basse`, `esperance_vie_haute`, `fecondite_basse`, `fecondite_haute`, `migrations_basses`, `migrations_hautes`, `population_agee`, `population_basse`, `population_haute`, `population_jeune` — **all from the 2026-2070 exercise**, not from the 2021 vintage.

---

## 2. FranceScope central demographic baseline

The FranceScope V4 central baseline = **INSEE 2026-2070 central scenario**, with the observed 2026 anchor (Bilan démographique 2025).

Per-year value policy (2027 → 2050) for the central scenario:

| Variable | Source rule |
|---|---|
| `total_population` | INSEE 2026 central projection, 2027–2050 |
| `working_age_population` | sum of 20–64 male + 20–64 female, INSEE 2026 central pyramid |
| `old_age_population` (= population_65_plus) | sum of 65+ male + 65+ female, INSEE 2026 central pyramid |
| `working_age_share` | recomputed = `WAP / total_population` |
| `old_age_share` | recomputed = `pop65+ / total_population` |
| `old_age_dependency_ratio` | recomputed = `pop65+ / WAP` (matches the 49/100 in 2040 headline) |
| `total_fertility_rate` | INSEE 2026 central: 1.56 (2026) → converging to 1.45 by 2028, stable thereafter |
| `life_expectancy_male` | INSEE 2026 central, 2005-2025 mortality trend excluding Covid years |
| `life_expectancy_female` | INSEE 2026 central, 2005-2025 mortality trend excluding Covid years |
| `net_migration` | INSEE 2026 central: +150,000 / yr from 2026 onward (constant) |
| `scenario_identifier` | `"central"` (with the 11 alternative INSEE scenarios retained as alternates) |

---

## 3. Observed / bridge / institutional projection segmentation

| Year window | Status | Source | data_status label |
|---|---|---|---|
| 2000 → 2021 | Historical (observed) | INSEE Bilan démographique 2025 + séries longues 2026-06-15 (POP1, POP3, POP4, POP5) | `observed` |
| 2022 → 2024 | Provisional observed (INSEE Bilans démographiques 2023, 2024, 2025) | INSEE Bilan démographique 2025 + Situation démographique 2025 | `observed_provisional` |
| **2026** | **Anchor (observed level + rates)** | **INSEE Bilan démographique 2025 (published 2026-01-13)** — population au 1er janvier 2026 = **69,082,000** | `observed` |
| **2027** | **Bridge year (linear-interpolated 2026→2028 mid-point)** for **level variables only** (total_population, working_age_population, old_age_population); rates come straight from INSEE 2026 central | mixed: anchor 2026 + projection 2028 | `bridge` |
| 2028 → 2050 | Institutional projection | INSEE Projections 2026-2070 central | `official_projection` |

### Transition rule from observed 2026 into projection 2027+

1. **Level variables** (`total_population`, `working_age_population`, `old_age_population`): for the bridge year 2027, use the linear midpoint between the 2026 observed level and the 2028 INSEE 2026-projection level. The 2026 endpoint is preserved exactly; only the 2027 row is overwritten.
2. **Rate variables** (`total_fertility_rate`, `net_migration`, `life_expectancy_male`, `life_expectancy_female`): taken directly from the INSEE 2026 central projection. No interpolation. TFR in 2027 follows the converging path (1.56 → 1.45 by 2028); net_migration = +150,000 from 2026 onward.
3. **Share / dependency variables** (`working_age_share`, `old_age_share`, `old_age_dependency_ratio`): always recomputed from the spliced level values to keep structural invariants `WAP/total`, `pop65+/total`, `pop65+/WAP` exactly satisfied post-splice.
4. **Scenario identifier**: 2027 row keeps `scenario = "central"` (and the 11 alternates), but `data_status = "bridge"` so any downstream consumer can flag it as non-projection, non-observed.

### Continuity invariants

- 2026 → 2027 transitions for **levels** must be continuous after the linear splice (no plateau).
- 2026 → 2027 transitions for **rates** must match the INSEE 2026 central published series for 2027 (no smoothing, no override).
- 2026 → 2027 → 2028 transitions for `working_age_population_growth` and `total_population_growth` must be well-defined and finite.

---

## 4. Working-age-population age band (frozen)

- **Definition**: working-age population = persons aged **20 to 64 inclusive** (années révolues), **both sexes combined**.
- Rationale: this is the band INSEE itself uses in the 2026 projection for the population-active indicator (Crédit Agricole ECO, 2026-06-12, footnote 2; Insee 2026-06-08 central scenario). It matches the existing definition in `francescope_v3_demographic_canonical.csv` (20–64), so the switch to the 2026 vintage does not require any labor-force equation redefinition.
- Population 65+ is the residual age band **65 ans ou plus** (both sexes).
- The "population des moins de 20 ans" group is kept for cross-checks only; it is not used by the V4 engine.

---

## 5. Existing old-projection files that should no longer drive V4

The following files currently in the repository carry the **2021 INSEE projection vintage** (or were built around it). They must be **deprecated as V4-driving inputs** after the new 2026-vintage ingestion is complete. They may be kept on disk for audit, but must not be read by the engine, the orchestrator, the labor-force builder or any MC simulation.

| File | Why deprecated |
|---|---|
| `data/processed/demographics/francescope_v3_demographic_canonical.csv` (+ `.parquet`) | All `central` and 11-alternate rows for years ≥ 2022 are sourced from `INSEE Projections de population 2021-2070 (paru 29/11/2021)` — must be replaced with the 2026-2070 exercise. |
| `data/processed/demographics/francescope_v3_demographic_structural_central.csv` | Pre-engine legacy V3 structural baseline built on the 2021 projection. Not currently read by the engine; remains on disk for audit only. **Do not feed it to V4.** |
| `data/processed/demographics/francescope_v3_labor_force_structural.csv` | Legacy V3 labor-force projection built on the 2021 vintage. Not currently read by the engine; remains on disk for audit only. **Do not feed it to V4.** |
| `data/processed/demographics/_d2_fertility_le_extract.parquet` | Older INSEE fertility / life-expectancy extract; superseded by the Bilan démographique 2025 + Projections 2026-2070 inputs. |
| `data/processed/demographics/insee_demographic_annual_source.csv` (+ `.parquet`) | Intermediate ingest file from the previous ingestion cycle; superseded by the new ingestion. |
| `data/processed/demographics/insee_population_by_age_sex.parquet` | Older age × sex extract; superseded by POP3 / POP4 / POP5 from the 2026 cycle. |
| Any reference to `INSEE Projections de population 2021-2070 (paru 29/11/2021)` in `data/processed/demographics/francescope_v3_demographic_canonical.csv` | All occurrences must be relabelled to the 2026-2070 vintage once that file is regenerated. |

After the new ingestion lands, the only files the engine is allowed to depend on are:

- `data/processed/demographics/francescope_v3_demographic_canonical.csv` (+ `.parquet`) — **regenerated**, with vintage labels updated to the 2026 sources above.
- All non-demographic canonical files (`master_canonical.parquet`, `financial_canonical.parquet`, `external_*.parquet`, `climate_canonical.parquet`, etc.) — **unchanged**.

---

## 6. Implementation hand-off checklist (future task — not in scope here)

When the next task implements this spec, the following must be true — and only these:

1. New ingestion script produces a **single** long-format `francescope_v3_demographic_canonical.csv` covering 2000 → 2070 with the per-row `(scenario, year, variable, value, unit, source, source_vintage, data_status)` schema, with vintage labels and data_status labels exactly as in §1 and §3 above.
2. The 12 INSEE scenarios (central + 11 alternates) are preserved; only the `central` row block and the `data_status` labels change.
3. `StructuralDemographicDriver` (in `src/francescope/demographics/structural_driver.py`) keeps its public API and its splice logic. `HISTORY_END`, `NET_MIGRATION_HISTORICAL_PLACEHOLDER`, `NET_MIGRATION_PROJECTION_ASSUMPTION` constants are updated to reflect the new vintage; `oadr_reference_2026()` is re-cached lazily on first use.
4. **No macro equation, no labor-force equation, no Index formula, no CORR-1/2/3/4 parameter, no scenario selection and no frontend code is modified.**

---

## 7. Invariants preserved

- MASTER_SEED = 20260815, n_paths = 1000, horizon 2027-2050, P10/P50/P90 path IDs 805/841/351, Index = FranceScope V3 — all unchanged.
- No data value is overwritten by this document.
- No simulation is rerun.
- No economic equation is altered.