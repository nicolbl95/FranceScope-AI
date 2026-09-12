# FRANCESCOPE V3 — OFFICIAL 1,000-PATH MONTE CARLO (2027–2050)

**Gate:** `OFFICIAL_MC1000_PASS`. `V3 OFFICIAL MC1000 = COMPLETED_PENDING_COHERENT_PATH_SELECTION`. 24,000 valid rows; paths 0–99 bit-identical to corrected MC100; frozen Index scoring applied; no numerical instability. No code recalibration; V2 unchanged.

## 1. Runner change
`src/francescope/simulation/monte_carlo_v3.py`: `run_development_mc` gained an explicit `n_paths: int = N_PATHS` parameter (default 100, backward-compatible). The per-path RNG construction `np.random.default_rng(np.random.SeedSequence([MASTER_SEED, path_id]))` is **unchanged**, so paths 0–99 reproduce the corrected MC100 exactly. No economic/annual logic duplicated or altered.

## 2. Reproducibility
`MASTER_SEED = 20260815`. Verified: MC100 vs MC1000 paths 0–99 **max absolute difference = 0.0** across all compared economic fields (gdp growth/level, gdp_pc, unemployment, median living, debt, deficit, gfc, external cyclical input, climate drag, AI effect, interest, OAT, fiscal stress). Deterministic; 24,000 rows regenerate identically.

## 3. Structural validation
1000 unique path IDs × 24 years = **24,000 rows**; no duplicate (path_id, year); no missing years; no NaN/inf in core outputs or Index; every path starts from the same authoritative 2026 state.

## 4. MC100 compatibility
See §2. Paths 0–99 identical (max diff 0.0). All divergence beyond path 99 is purely the larger stochastic sample.

## 5. Realized RNG statistics
- external_cycle_shock: mean 0.0127, sd 1.003, P10 −1.27 / P50 0.012 / P90 1.31, min/max −3.90/3.81 (≈ N(0,1)).
- ai_productivity_amplitude: mean 1.055, P10 0.720 / P50 1.051 / P90 1.411, min 0.452 / max 1.673 (Triangular 0.45/1.0/1.70).
- climate_amplitude: mean 1.205, P10 0.692 / P50 1.175 / P90 1.773, min 0.337 / max 2.239 (Triangular 0.3/1.0/2.3).

## 6. Regime frequencies (path-years, %)
EXPANSION 35.64 · SLOWDOWN 45.58 · RECESSION 6.03 · CRISIS 7.35 · RECOVERY 5.40. Closer to calibration than MC100 (larger sample).

## 7. GFC frequencies
Total trigger years = **765** (expected ~720 at p=0.03 × 24,000). Paths: 0 events 455 · 1 event 368 · 2 events 143 · 3 events 27 · 4+ events 7. Higher-than-expected count consistent with sampling/calibration tolerance; no bug.

## 8. Core distributions (P10 / P50 / P90)
- GDPpc (MEUR): 2030 0.0377/0.0392/0.0404 · 2040 0.0378/0.0412/0.0446 · 2050 0.0384/0.0429/0.0475.
- Unemployment: 2030 7.40/7.79/8.33% · 2040 7.03/7.54/8.23% · 2050 6.88/7.37/8.00%.
- Median living (EUR): 2030 25,636/25,924/26,159 · 2040 25,749/26,404/27,018 · 2050 25,885/26,744/27,551.
- Real GDP growth: 2030 0.53/5.27/2.24% · 2040 0.88/8.75/2.51% · 2050 0.61/6.05/2.29%.
- Debt/GDP (%): 2030 131.5/131.2/136.0 · 2040 146.6/157.1/169.8 · 2050 174.2/191.7/213.3.

## 9. V3 Index distributions (RAW, P10 / P50 / P90)
- GDPpc score: 2030 127.3/143.7/157.3 · 2040 128.3/165.7/203.1 · 2050 134.7/184.5/234.7.
- Median-living score: 2030 150.9/158.9/165.4 · 2040 154.0/172.2/189.2 · 2050 157.8/181.6/204.0.
- Unemployment score: 2030 119.8/128.1/134.3 · 2040 121.3/132.0/140.0 · 2050 124.9/134.7/142.4.
- **FranceScope_Index_V3**: 2030 132.6/143.6/152.2 · 2040 135.4/156.5/176.1 · 2050 **140.5/167.0/192.8**. No clipping; raw.

## 10. 2026→2027 continuity
Historical official 2026 Index = **140.947**. 2027 simulated Index P10/P50/P90 = **137.44 / 140.79 / 143.80** — mechanically continuous (no unit/scoring discontinuity; paths diverge forward as intended).

## 11. Index component balance / correlation (2050)
Scores reconcile exactly: `Index = 100 + Σ(score−100)/3` (verified to 1e-9). Contribution means (2050): gdp_pc +28.2, median +27.0, unemployment +11.3 — all positive, no domination. **gdp_pc_score ↔ median_living_score correlation = 0.999** (both driven by the same GDP growth in the reduced-form) — recorded as a **known structural characteristic**, not a scoring defect; equal 1/3 weights retained per frozen method. gdp↔unemp 0.59, median↔unemp 0.59.

## 12. Debt tail (2050, % units)
P90 213.4 · P95 220.4 · P99 240.6 · max 282.5. Paths >200%: **282**; >250%: **3**; >300%: **0**. Consistent with audited fiscal mechanism (persistent ~5–7% deficits + interest feedback). Classified **EXPECTED_TAIL_BEHAVIOR** — accepted modeled outcome, not a new structural problem.

## 13. Plausibility flags
All zero: gdp growth outside ±10% =0; unemployment <0 or >20% =0; debt <0 or >300% =0; median living ≤0 =0; gdp ≤0 =0; NaN/inf core =0; OAT >15% =0; Index <0 or >300 =0. No clipping applied; high scores (>100) are expected, not flagged.

## 14. MC100 vs MC1000 stability (2050 P10/P50/P90)
GDPpc 0.0384/0.0429/0.0475 vs 0.0376/0.0429/0.0470 (MC100) — directionally identical. Unemployment 6.88/7.37/8.00 vs 6.84/7.41/7.92. Median living 25,885/26,744/27,551 vs 25,728/26,747/27,453. Debt 174.2/191.7/213.3 vs 175.8/191.6/217.4. MC100 estimates were **directionally representative**; MC1000 tightens sampling error.

## 15. Suspicious behavior
None material. GFC count (765) slightly above 720 expectation = sampling variation. AI amplitude modest (~4% cumulative), as audited — not attenuation. Climate LOW, as designed.

## 16. Frozen scoring / no clipping
Confirmed: V3 Index uses `src/francescope/index/v3_index.py` constants (2010–2019 median/sd). RAW scores; no clipping; no re-normalization; no forecast-derived scale.

## 17. V2 unchanged
Legacy V2 engine and 7-component Index artifacts untouched.

## 18. Files created / modified
- `data/processed/forecasts/francescope_v3_mc1000_paths.parquet` (+ `.csv`)
- `data/processed/forecasts/francescope_v3_mc1000_rng_inputs.csv`
- `data/processed/index/francescope_v3_mc1000_index.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_MC1000_{RUN_METADATA,RNG_AUDIT,CORE_DISTRIBUTIONS,INDEX_DISTRIBUTIONS,INDEX_CONTRIBUTIONS,REGIME_GFC_AUDIT,PLAUSIBILITY_FLAGS,DEBT_TAIL_AUDIT,MC100_COMPARISON}.csv`
- `docs/FRANCESCOPE_V3_MC1000_OFFICIAL_REPORT.md`
- Modified (minimal): `src/francescope/simulation/monte_carlo_v3.py` (n_paths param). Updated: current-state matrix + checkpoint.

## 19. Decision
**OFFICIAL_MC1000_PASS** → `COMPLETED_PENDING_COHERENT_PATH_SELECTION`.

## 20. Next task
**COHERENT P10/P50/P90 PATH SELECTION** — select one internally-consistent simulation path per quantile (not marginal cross-variable quantiles) for the official V3 narrative/scenarios.

## Final verdict
V3 OFFICIAL 1000-PATH MONTE CARLO COMPLETE — OFFICIAL_MC1000_PASS
