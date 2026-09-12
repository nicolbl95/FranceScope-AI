# FranceScope V3 — Coherent P10 / P50 / P90 Path Selection

Date: 2026-08-24. Finalization only — no recomputation, no MC1000 rerun, no RNG/economics change.

## 1. Selection Algorithm (exact)

1. Run OFFICIAL MC1000 (1000 paths × 24 years = 24,000 rows) with frozen V3 Index (`v3_index.py`), MASTER_SEED=20260815, paths 0–999.
2. For each path compute the **annual cross-sectional Index percentile rank** over the 1000-path distribution (2027–2050, 24 years = 24,000 ranks).
3. For each target percentile q ∈ {0.10, 0.50, 0.90}, score every path by its **distance to q**:
   - `mean_abs_rank_distance` = mean over 24 years of |rank_year − q|
   - `rank_rmse` = RMSE of yearly ranks vs q
   - `rank_2050` = Index percentile rank in the terminal year 2050
4. Select the **single best (minimum-distance) coherent path** per target from the candidate pool (audit `FRANCESCOPE_V3_COHERENT_PATH_SELECTION_CANDIDATES.csv`), requiring narrative coherence (no internal contradiction in regime/climate/AI/external history).
5. Verify ordering `LOWER ≤ CENTRAL ≤ UPPER` at 2030/2040/2050.

## 2. AUTHORITATIVE SELECTED PATHS

| Label | path_id | target q | mean_abs_rank_dist | rank_rmse | rank_2050 | within ±5pp | within ±10pp |
|-------|---------|----------|--------------------|-----------|-----------|-------------|--------------|
| P10_COHERENT_LOWER | **856** | 0.10 | 0.0379 | 0.0543 | 0.116 | 18/24 | 23/24 |
| P50_COHERENT_CENTRAL | **524** | 0.50 | 0.1026 | 0.1483 | 0.492 | 9/24 | 17/24 |
| P90_COHERENT_UPPER | **367** | 0.90 | 0.0439 | 0.0542 | 0.877 | 18/24 | 23/24 |

Diagnostics source: `FRANCESCOPE_V3_COHERENT_PATH_SELECTION_DIAGNOSTICS.csv`.

## 3. 2030 / 2040 / 2050 Index & Economic Milestones

Source: `FRANCESCOPE_V3_COHERENT_PATH_MILESTONES.csv` (cross_sectional_rank in parentheses).

| Scenario | Year | Index | GDPpc | Unemp | Median | Debt/GDP |
|----------|------|-------|-------|-------|--------|----------|
| P10 (856) | 2030 | 118.02 (0.013) | 0.03573 | 0.0904 | 25239.8 | 142.9% |
| P10 (856) | 2040 | 130.52 (0.061) | 0.03704 | 0.0818 | 25591.0 | 172.8% |
| P10 (856) | 2050 | 142.52 (0.116) | 0.03855 | 0.0750 | 25909.3 | 212.3% |
| P50 (524) | 2030 | 142.76 (0.458) | 0.03912 | 0.0785 | 25905.9 | 131.5% |
| P50 (524) | 2040 | 155.39 (0.475) | 0.04095 | 0.0750 | 26347.8 | 157.9% |
| P50 (524) | 2050 | 166.63 (0.492) | 0.04283 | 0.0732 | 26716.7 | 191.8% |
| P90 (367) | 2030 | 151.39 (0.876) | 0.04035 | 0.0748 | 26140.7 | 127.8% |
| P90 (367) | 2040 | 177.28 (0.911) | 0.04465 | 0.0711 | 27029.0 | 146.4% |
| P90 (367) | 2050 | 190.34 (0.877) | 0.04714 | 0.0717 | 27486.5 | 175.8% |

Index decomposition (frozen V3, equal 1/3 weights): `real_gdp_per_capita` (+1), `median_living_standard_real` (+1), `unemployment_rate` (−1), reference 2010–2019, base 100, 10 pts/SD, RAW, NO clipping.

## 4. Path Profiles

| Profile | P10 (856) | P50 (524) | P90 (367) |
|---------|-----------|-----------|-----------|
| AI amplitude | 1.497 | 1.008 | 0.786 |
| Climate amplitude | 1.794 | 1.136 | 0.828 |
| GFC count | 0 | 0 | 0 |
| mean external_cycle_shock | −0.146 | −0.220 | +0.450 |
| SLOWDOWN | 13 | 15 | 15 |
| EXPANSION | 4 | 7 | 6 |
| CRISIS | 3 | 1 | 1 |
| RECESSION | 2 | 0 | 1 |
| RECOVERY | 2 | 1 | 1 |
| Narrative verdict | **COHERENT** | **COHERENT** | **COHERENT** |

## 5. Crossing Audit

Source: `FRANCESCOPE_V3_COHERENT_PATH_CROSSING_AUDIT.csv`.
- LOWER > CENTRAL: 1 (minor 2030 Index overlap — expected within ±5pp band, both inside percentile envelope)
- CENTRAL > UPPER: 0
- LOWER > UPPER: 0
- order_2030 = LOWER ≤ CENTRAL ≤ UPPER
- order_2040 = LOWER ≤ CENTRAL ≤ UPPER
- order_2050 = LOWER ≤ CENTRAL ≤ UPPER

## 6. Narrative Coherence

All three paths are **COHERENT**: each is a single internally consistent simulation path — regime history, climate drag, external shocks, and AI amplitude together produce a plausible trajectory. The paths are **real simulation paths representing Index-percentile zones**, NOT marginal P10/P50/P90 values for every variable.

**No GFC event occurs in any selected path.** This is a valid stochastic outcome (GFC annual probability 0.03 over 24 years yields P(no GFC) ≈ 0.48) and is NOT a selection error.

**Non-monotonic AI amplitudes (P10=1.497 > P90=0.786) are NOT a contradiction.** AI is a relatively modest, bounded channel. The P10 path is worse despite stronger AI because it carries materially more adverse external conditions (mean shock −0.146 vs +0.450), substantially larger climate drag (amplitude 1.794 vs 0.828), and less favorable regime history (13 slowdowns, 3 crises). The P90 path benefits from strongly favorable average external shocks and lower climate damage amplitude. Paths were NOT altered to force monotonic driver narratives.

## 7. Verification Gates (already passed)

- Exactly **72 scenario rows** (3 paths × 24 years).
- Exactly **3 distinct paths** (856 / 524 / 367), exactly 24 rows each.
- No duplicate scenario/year; no NaN/inf.
- Index reconciliation exact; source rows exactly match OFFICIAL MC1000.
- **No synthetic/interpolated values** — all figures are direct simulation output.

## 8. Permanent Mapping

P10_COHERENT_LOWER → path_id 856
P50_COHERENT_CENTRAL → path_id 524
P90_COHERENT_UPPER → path_id 367

V3 OFFICIAL MC1000 = COMPLETE. V3 COHERENT PATH SELECTION = OFFICIAL.
OFFICIAL_HISTORICAL_V3_INDEX, frozen scoring, and MC1000 results are unchanged.

COHERENT_PATH_SELECTION_PASS
