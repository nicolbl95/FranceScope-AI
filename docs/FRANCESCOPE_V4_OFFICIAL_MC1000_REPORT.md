# FranceScope V4 — OFFICIAL Monte Carlo 1000 (MC1000) Report

**Paths:** 1000 (official MC, seed 20260815)  **Horizon:** 2027–2050  **Combinations:** 24,000  **Active corrections:** CORR-1 + CORR-2 + CORR-3 + CORR-4 + Page 11 (demographic-fiscal)

## 1. Execution & numerical stability
- Completed all 1000 paths (paths 0–999) from 2027 to 2050 with deterministic per-path seeding `SeedSequence([20260815, path_id])`.
- Non-finite (NaN/Inf) values across ALL 24,000 year-path state outputs: **0** (of 360000 field evaluations).
- No NaNs, no Infs, no numerical blow-up, no memory overflow. All four correction loops remain bounded and mutually coherent.

## 2. 2050 marginal distributions (P10 / P50 / P90)

| Metric | P10 | P50 | P90 | Units |
|---|---|---|---|---|
| real_gdp_per_capita | +0.031991 | +0.035840 | +0.039740 | MEUR/person |
| unemployment_rate | 7.64 | 8.26 | 9.04 | % (decimal x100) |
| nairu | 7.67 | 7.92 | 8.25 | % (decimal x100) |
| median_living_standard_real | 24,515 | 25,353 | 26,135 | EUR |
| debt_gdp | +301.759660 | +331.661848 | +369.328666 | % GDP |
| francescope_index_v3 | +97.997845 | +123.776866 | +147.661372 | index (raw, read-only) |
| corporate_credit_gap | +0.030556 | +0.031867 | +0.033657 | decimal vs CCR_REF |
| capital_gap | -0.193598 | -0.187324 | -0.182385 | level gap |
| productivity_growth_dev | -0.001678 | -0.001436 | -0.001257 | decimal/yr |
| fiscal_drag | -0.003128 | -0.003128 | -0.003128 | decimal/yr (<=0) |
| external_structural_drag | -0.001000 | -0.001000 | -0.001000 | decimal/yr (<=0) |
| demographic_fiscal_pressure | +2.384550 | +2.384550 | +2.384550 | pp GDP (primary spend) |
| oadr_impact | +3.974250 | +3.974250 | +3.974250 | pp GDP (primary balance) |

## 3. Comparison vs pre-structural V3 baseline (2050 P50)

Pre-structural V3 baseline = legacy `docs/FRANCESCOPE_V3_MC1000_OFFICIAL_REPORT.md` (same seed, same RNG; before CORR-1..4). V4 includes all four corrections.

| Metric | V3 baseline P10/P50/P90 | V4 P10/P50/P90 | Delta P50 (V4−V3) |
|---|---|---|---|
| real_gdp_per_capita | 0.0384/0.0429/0.0475 | 0.0320/0.0358/0.0397 | -0.0071 |
| unemployment_rate | 6.88/7.37/8.00 % | 7.64/8.26/9.04 % | +0.89 pp |
| median_living_standard_real | 25,885/26,744/27,551 | 24,515/25,353/26,135 | -1,391 EUR |
| debt_gdp | 174.2000/191.7000/213.3000 | 301.7597/331.6618/369.3287 | +139.9618 |
| francescope_index_v3 | 140.5000/167.0000/192.8000 | 97.9978/123.7769/147.6614 | -43.2231 |

## 4. Coherent representative paths (V4)

Selected as the internally-consistent path whose 2050 V3 Index is closest to the 2050 marginal Index percentile target. Path IDs below; full trajectories exported to `data/processed/v4/`.

| Label | Path ID | Index | GDPpc | Unemp % | NAIRU % | Median | Debt % |
|---|---|---|---|---|---|---|---|
| P10_COHERENT_LOWER_V4 | 403 | 98.02 | 0.03190 | 8.87 | 8.20 | 24,497 | 369.3 |
| P50_COHERENT_CENTRAL_V4 | 386 | 123.74 | 0.03567 | 8.00 | 7.84 | 25,302 | 333.0 |
| P90_COHERENT_UPPER_V4 | 959 | 147.65 | 0.03955 | 7.55 | 7.71 | 26,098 | 301.7 |

## 5. Interpretation
- CORR-1 (financing→capital→productivity), CORR-2 (NAIRU hysteresis), CORR-3 (persistent fiscal-pressure drag), CORR-4 (persistent external trend) and Page 11 (aggregate OADR→public-finance pressure) all operate simultaneously and remain bounded under the full 1,000-path ensemble.
- Relative to the pre-structural V3 baseline, V4 shows the intended structural corrections: lower real-GDP-per-capita and median living, higher unemployment/NAIRU, higher debt-to-GDP, and a lower FranceScope Index V3 — the corrections are economically coherent (no artificial runaway; all values finite and bounded).
- `fiscal_drag` ≤ 0 and `external_structural_drag` ≤ 0 are persistent but strictly bounded (defensive clamps); both enter structural growth exactly once and are distinct from the B1 consolidation impulse and the i.i.d. external cycle shock.
- The V3 Index is computed strictly read-only from its three frozen 2010–2019 components; reference statistics, components, and scoring formula are UNCHANGED.

## 6. Classification
**V4 OFFICIAL MC1000 PASSED** — 1,000 paths, 24,000 valid rows, zero numerical instability, coherent representative paths identified. Definitive probabilistic benchmark for FranceScope V4 generated without modifying any correction logic, parameters, tests, or the V3 Index.
