# FRANCESCOPE V3 — Median-Living Correction Calibration

## Selected model
**C1 re-estimated, gap form, Covid-excluded (stable) coefficients:**

```
median_growth_t = b0
                + b1 * gdp_growth_t
                + b2 * (unemployment_rate_t - 0.075)

b0 = 0.00009
b1 = 0.2880      (higher GDP growth raises median living)
b2 = -0.0078      (unemployment above 7.5% reference lowers it, small in this sample)
unemployment_rate = decimal (0.08 = 8%); reference 0.075 = V2 natural rate
productivity/real-wage: not entered separately (constants in historical sample;
                       real_wage = 0.7*productivity by V2 construction)
```

The original heuristic productivity/real-wage terms (0.4·prod + 0.3·rw) are replaced
by the data-estimated intercept (which absorbs the constant productivity contribution).

## Why not A or B
- **A (current level):** mean pred −0.55%/yr vs actual +0.54% → bias −1.08pp/yr;
  cumulative −8.6% vs +8.8%; constant-economy at reference u=7.5% still declines
  (−1.0pp/yr). REJECTED.
- **B (gap, same −0.2 coefficient):** mean pred +0.95%/yr → bias **+0.42pp/yr**
  (over-corrects; cum +16.2% vs +8.8%). REJECTED as final.
- **C2 (add productivity+real-wage regressors):** REJECTED — both are constants in
  the 2011–2026 sample and `real_wage = 0.7·productivity`, so perfectly collinear
  with the intercept (VIF-singular). Parsimony rejected it.

## Backtest comparison (2011–2026, n=16; unemployment DECIMAL, gap = u − 0.075)
| model | mean pred | bias | MAE | RMSE | cum pred | cum actual |
|-------|-----------|------|-----|------|----------|-----------|
| A level | −0.0055 | −0.0108 | 0.0166 | 0.0265 | −0.086 | +0.088 |
| B gap   | +0.0095 | +0.0042 | 0.0156 | 0.0246 | +0.162 | +0.088 |
| C1 robust (SEL) | +0.0034 | −0.0020 | 0.0104 | 0.0167 | +0.055 | +0.088 |

**IMPORTANT — full-sample vs robust-window distinction (corrected):**
- **FULL-SAMPLE evaluation** (robust coefs applied to all 16 yrs 2011–2026):
  mean pred +0.34%/yr, bias −0.20pp/yr, RMSE 1.67pp/yr,
  **cum pred ≈ +5.53%**, cum actual ≈ +8.84%.
- **ROBUST-WINDOW evaluation** (excl 2020–2021, n=14):
  mean pred +0.40%/yr, bias ≈ 0, RMSE 0.80pp/yr,
  cum pred ≈ +5.81%, cum actual ≈ +5.77%.
- The previously cited **+0.089 / +0.088** figures were a MISLABEL and must NOT be
  reported as the full-sample predicted cumulative (correct full-sample value ≈ +5.53%).

C1 full-sample was rejected: b1(gdp) = **−0.239** (perverse negative sign, Covid-
dominated). Excluding 2020–2021 gives stable, economically sensible signs.
corr(gdp_growth, unemployment_gap) = −0.06 (no harmful collinearity in C1).

## Constant-economy / reference sanity
gdp=prod=rw=0, u=7.5%: C1 → ≈ +0.0001/yr (no perpetual decline). PASS.
(A fails at −1.0pp/yr; B passes at +0.5pp/yr.)

## Long-horizon diagnostic (deterministic V3 control, not a forecast)
Median living (EUR): 2026 → 2030 → 2040 → 2050
- A: 25,848 → 24,824 → 22,986 → 21,076  (collapse — REJECT)
- B: 25,848 → 26,364 → 28,362 → 30,219  (explosive — REJECT)
- C1 robust: 25,848 → 25,893 → 26,266 → 26,476  (modest, stable — SELECTED)

## Economic sign verdict
- GDP growth: positive (0.288) — OK.
- Unemployment gap: negative-sign (correct direction), small magnitude — OK.
- No perverse signs in the selected (robust) specification.

## Pensions / transfers / taxes
Deferred. The defect was internal (unemployment specification), not missing household
channels. Adding negative channels would worsen an already-corrected model.
**CURRENT_REDUCED_FORM_SUFFICIENT** with the gap correction.

## Credit→investment
Unchanged: OAT→credit = PASS; credit→investment = FAIL_NOT_WIRED.

## Files
Created: `docs/FRANCESCOPE_V3_MEDIAN_LIVING_CORRECTION_CALIBRATION.md`,
`data/audits/economic_system/FRANCESCOPE_V3_MEDIAN_LIVING_MODEL_CANDIDATES.csv`,
`data/audits/economic_system/FRANCESCOPE_V3_MEDIAN_LIVING_CORRECTION_DIAGNOSTICS.csv`,
`scripts/v3_median_living_correction_calibration.py`.
Updated: `FRANCESCOPE_V3_PRE_MONTE_CARLO_BLOCKERS.csv` (median-living → RESOLVED_CALIBRATION_DEFINED).
No model code modified.

## Next task
Implement the C1-robust formula in `src/francescope/orchestrator/v1_orchestrator.py`
(replace the level term), then re-run the median-living validation and the earlier
fiscal Test F to confirm no regression.
