# FranceScope V3 — New Mechanism 1A: MACRO-REGIME SPECIFICATION AND CALIBRATION

**Status:** SPEC + CALIBRATION ONLY. No engine code modified. This defines the smallest defensible persistent macro-cycle mechanism (an internal simulation STATE) to replace V2's "positive trend + independent noise" behavior with realistic EXPANSION→SLOWDOWN→RECESSION→CRISIS→RECOVERY persistence.

## 1. HISTORICAL DATA USED

- Source: `data/raw/eurostat/external/namq_10_gdp_FR.json` (Eurostat `namq_10_gdp`, FR, `CLV20_MEUR`, `SCA`, `B1GQ`).
- Aggregated quarterly → annual; annual real-GDP growth computed 2011–2025 (15 obs; 2010 is the base year).
- Coverage is the **longest reliable French annual real-GDP growth series in the repository** (no older French series present; no download).
- Observed growth (%): 2011=2.48, 2012=0.23, 2013=0.93, 2014=1.00, 2015=1.00, 2016=0.74, 2017=2.27, 2018=1.58, 2019=2.10, 2020=−7.61, 2021=6.79, 2022=2.80, 2023=1.82, 2024=1.43, 2025=0.89. Mean normal (non-crisis/non-recovery) growth = **1.482%** (used as structural baseline).

## 2. OPERATIONAL REGIME DEFINITIONS

Transparent thresholds calibrated to the observed distribution (no arbitrary cuts):
- **CRISIS**: growth ≤ −3% (severe contraction). → 2020.
- **RECESSION**: −3% < growth < 0 (mild/moderate contraction). → not observed 2011–2025 (no sub-zero non-crisis year).
- **SLOWDOWN**: 0 ≤ growth < 1.3% (weak positive). → 2012,2013,2014,2015,2016,2025.
- **EXPANSION**: growth ≥ 1.3% (clearly above weak territory). → 2011,2017,2018,2019,2022,2023,2024.
- **RECOVERY**: positive growth in the year immediately following a RECESSION/CRISIS → 2021 (after 2020 CRISIS).

RECOVERY is distinct from EXPANSION (it is the rebound state). CRISIS is a macro state, NOT a hazard.

## 3. HISTORICAL LABELS (summary)

2011 EXP, 2012–2016 SLOW, 2017–2019 EXP, 2020 CRISIS, 2021 RECOV, 2022–2024 EXP, 2025 SLOW. The labels reasonably capture the 2020 crash and 2021 rebound and the 2022+ slowdown. (2008–2009 not in sample → CRISIS-state frequency is an upper bound; GFC handled later via trigger.)

## 4. SELECTED TRANSITION ARCHITECTURE

**A. Historical Markov transitions + state-specific cyclical GDP gaps — SELECTED.** Transparent empirical 5×5 matrix, shrunk for unobserved transitions. (B. Rule-based deterministic persistence rejected: more ad hoc, no empirical frequencies.)

## 5. BASE TRANSITION MATRIX (from → to), shrunk (λ=2 toward structural prior)

| from \ to | EXP | SLOW | REC | CRISIS | RECOV |
|---|---|---|---|---|---|
| EXPANSION | 0.567 | 0.289 | 0.011 | 0.133 | 0.000 |
| SLOWDOWN | 0.286 | 0.657 | 0.043 | 0.014 | 0.000 |
| RECESSION | 0.150 | 0.350 | 0.250 | 0.150 | 0.100 |
| CRISIS | 0.000 | 0.067 | 0.200 | 0.067 | 0.667 |
| RECOVERY | 0.733 | 0.200 | 0.000 | 0.000 | 0.067 |

Raw counts: EXP→[4,2,0,1,0]; SLOW→[1,4,0,0,0]; RECESSION→none (interpolated via prior); CRISIS→[0,0,0,0,1]; RECOV→[1,0,0,0,0]. Adjustments: RECESSION row has zero observations, so it is taken from the structural prior (transparent shrinkage, documented). CRISIS/RECOV rows have 1 obs each, shrunk. No unrealistic EXP→CRISIS-every-few-years (P=0.133 reflects 1/9 historic + prior), no immediate RECESSION→EXP dominance.

## 6. REGIME DURATIONS (expected years)

EXPANSION 2.31, SLOWDOWN 2.92, RECESSION 1.33, CRISIS 1.07, RECOVERY 1.07.

## 7. SELECTED regime_cyclical_input (decimal annual GDP-growth contribution)

**Calibration gate (regularization):** CRISIS and RECOVERY in the raw sample are single-observation extremes (2020 pandemic −7.61%; 2021 rebound +6.79%) and RECESSION has zero observations in 2011–2025. These are NOT robust empirical means, and V3 implements no dedicated pandemic model. The acute event severity is therefore reserved for the future event-shock channel (GFC/climate disaster → `shock_input`), while `regime_cyclical_input` represents the *persistent cyclical environment*. Regularized (conservative shrinkage toward economically related neighbors + threshold ranges):
- CRISIS: −0.0856 → **−0.0364** (−3.64pp persistent; full −8.56pp reserved for the acute event shock)
- RECOVERY: +0.0584 → **+0.0186** (+1.86pp moderate rebound)
- RECESSION: −0.0197 → **−0.0214** (−2.14pp, unobserved → interpolated)
- EXPANSION: kept empirical **+0.0098** (+0.98pp)
- SLOWDOWN: kept empirical **−0.0029** (−0.29pp)

A single transparent common re-centering (drift = +0.00143) is applied so the stationary-weighted mean = 0 (no permanent trend re-introduced). Final set:
- EXPANSION: **+0.0098**
- SLOWDOWN: **−0.0029**
- RECESSION: **−0.0214**
- CRISIS: **−0.0364**
- RECOVERY: **+0.0186**

Ordering holds: CRISIS ≪ RECESSION < SLOWDOWN < EXPANSION; RECOVERY positive. Method: per-state mean growth minus the 1.482% structural baseline, regularized for poorly-identified states, then centered. No production-function/HP-filter/HMM dependence.

## 8. IMPLIED LONG-RUN FREQUENCIES (stationary distribution)

EXPANSION 0.395, SLOWDOWN 0.429, RECESSION 0.049, CRISIS 0.071, RECOVERY 0.056. Recessions occur with realistic frequency; crisis share is modest (upper bound from small sample); expansion is not permanent (≈40%). Documented adjustment: shrinkage keeps CRISIS/RECOV rows from degenerating with 1 obs.

## 9. 2026 INITIAL REGIME

**SLOWDOWN (retained).** Evidence: 2025 growth = 0.89% (<1.3% threshold, weak), and a clear deceleration 2.80%(2022)→1.82→1.43→0.89. Calibration-gate check: the repository's 2026 bridge/Index artifacts contain no 2026 annual real-GDP-growth figure that contradicts weak growth, so SLOWDOWN is retained as the 2027 simulation anchor.

## 10. DOUBLE-COUNTING PROTECTIONS

- **External contagion:** `external_cyclical_input` is the contemporaneous external shock; the regime captures its *persistence/propagation* (external pressure can raise adverse transition probabilities) but does NOT repeat the same contemporaneous GDP effect.
- **Fiscal stress:** fiscal hooks affect GDP directly; fiscal stress may shift future transition probabilities, not the same-year cyclical term.
- **Climate:** chronic drag is structural; disaster is a shock. A severe disaster may raise adverse transition probability, but its direct GDP shock stays separate.

## 11. FUTURE GFC TRANSITION INTERFACE

`global_financial_crisis_trigger` (later mechanism) will: (a) sharply raise P(CRISIS)/P(RECESSION) from the current regime, and (b) separately drive the external system shock. This gives both immediate external effect and persistent macro-regime effect. Not implemented now; default neutral.

## 12. FUTURE UNEMPLOYMENT INTERFACE

`macro_regime` → `regime_cyclical_input` → GDP growth → existing Okun/unemployment mechanism. No second arbitrary unemployment shock per regime (avoids double counting).

## 13. DETERMINISTIC A/B/C/D PATH DIAGNOSTICS (vs structural baseline, regularized effects)

- CASE A (EXP×10): cumulative +0.098 (+9.8pp over a decade).
- CASE B (EXP→SLOW→REC): −0.015 (−1.5pp).
- CASE C (REC→RECOV→EXP): +0.007 (+0.7pp).
- CASE D (SLOW→CRISIS→RECOV): −0.021 (−2.1pp, persistent regime effect only; acute event shock is additional).

**CRISIS double-count test:** CRISIS regime alone = −0.0364 (persistent weakness only). Hypothetical −3pp acute GFC shock + CRISIS regime = −0.0664, where the acute external/shock_input (−0.03) is SEPARATE from the persistent regime effect (−0.0364). Same separation holds for major_climate_disaster (−0.005) + CRISIS regime = −0.0414. The two channels are distinct; the regime never repeats the full acute event. (GFC not implemented; hypothetical diagnostic only.)

## 14. FUTURE IMPLEMENTATION LOCATIONS (not done here)

`src/francescope/regime/macro_regime.py` (pure deterministic):
- `classify_regime(growth, prev_regime) -> state`
- `transition_probabilities(current_regime, modifiers=neutral) -> dict` (deterministic; RNG stays in orchestrator)
- `regime_cyclical_input(state) -> float`
- hooks: `external_cycle_pressure`, `fiscal_stress`, `global_financial_crisis_trigger`, `major_climate_disaster`, `sovereign_risk_shock` (all default neutral).

## 15. ARTIFACTS

`docs/FRANCESCOPE_V3_MACRO_REGIME_SPEC.md` (this file); `FRANCESCOPE_V3_MACRO_REGIME_HISTORICAL_LABELS.csv`; `FRANCESCOPE_V3_MACRO_REGIME_TRANSITION_CANDIDATES.csv`; `FRANCESCOPE_V3_MACRO_REGIME_DIAGNOSTICS.csv`.
