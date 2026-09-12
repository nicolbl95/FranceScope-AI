# FRANCESCOPE V3 — RNG Distribution Calibration (100-path dev MC)

## 1. External cycle shock
**Selected: z ~ Normal(0,1), iid yearly.** Supported by V2: global-growth
uncertainty = 0.008 (decimal) and `external_cyclical_input = 0.008*z`, so
z~N(0,1) reproduces V2's external uncertainty scale exactly. Magnitudes:
z=P10/-1.28 -> -1.02pp; z=P90/+1.28 -> +1.02pp external cyclical.
V2 external residuals are drawn iid per year; macro_regime already supplies
persistent domestic cyclical dynamics, so NO AR(1) persistence (avoids double
count). Bounded/truncated alternative rejected as unnecessary.

## 2. AI productivity amplitude
**Selected: Triangular(low=0.45, mode=1.0, high=1.70).** Uses the project's
own weak/central/strong MODEL_PRIOR (0.45/1.0/1.70). Bounded against absurd
gains, centered at 1.0, transparent. Path-level draw.

## 3. AI employment displacement amplitude
**Selected: SAME amplitude as AI productivity (option A).** Simplest defensible
joint relationship; no independent residual retained. Profile already fades to 0
(no permanent unemployment). Path-level (same draw).

## 4. Climate amplitude
**Selected: Triangular(low=0.3, mode=1.0, high=2.3).** Mapped from V2 climate
damage: central 0.002, uncertainty 0.002, bounds 0-0.010, GDP loading 0.5 ->
V3 drag -0.001*amp (amp=1 matches V2 central). Triangular bounds keep worst
100-path drag at ~-0.0023 (adverse but not absurd). Path-level.

## 5. Climate disaster
**major_climate_disaster_shock = 0.0 for first 100 paths (DETERMINISTIC_ZERO).**
Intentional scope control; not forgotten.

## 6. GFC / regime
Unchanged: regime_uniform_draw ~ Uniform(0,1) yearly; gfc_uniform_draw ~
Uniform(0,1) yearly event, p_gfc=0.03. No correlation.

## 7. Correlation structure (minimum)
Independent: external, GFC, climate, AI productivity. AI displacement = AI
productivity amplitude (causal joint). Regime transitions conditionally affected
by GFC via existing architecture. No covariance matrix.

## 8. Draw frequency
YEARLY: regime_uniform_draw, gfc_uniform_draw, external_cycle_shock.
PATH_LEVEL: climate_amplitude, ai_productivity_amplitude, ai_employment_amp.
FIXED_FIRST_MC: major_climate_disaster_shock = 0.

## 9. P10/P50/P90 (input / translated)
- external z: -1.28 / 0 / +1.28  -> ext_cycl -1.02pp / 0 / +1.02pp
- AI prod amp: 0.712 / 1.000 / 1.404 -> 2035 effect +0.24 / +0.33 / +0.46pp
- AI disp amp: = prod amp -> 2035 +0.07 / +0.10 / +0.14pp (fades)
- climate amp: 0.674 / 1.000 / 1.926 -> drag -0.07 / -0.10 / -0.19pp

## 10. Combined extreme sanity
FAVORABLE (ext+1.02pp, AI+0.46pp, climate-0.07pp, no GFC): finite, reasonable.
ADVERSE (ext-1.02pp, AI+0.24pp, climate-0.19pp): finite, reasonable.

## 11. Reproducibility contract
Future RNG ownership: orchestrator-level `numpy.random.Generator`. ONE master
seed. Per-path stream via `np.random.SeedSequence([master_seed, path_i])` ->
`np.random.default_rng(seq)`. No global random state, no legacy `random`.

## 12. First-100-path purpose
Development test only (not final output): path diversity, regime/GFC frequency,
GDP/unemployment/median distributions, numerical stability, causal variation,
variance-source dominance. Do NOT retune distributions for aesthetics.

## Gate
V3 RNG CALIBRATION COMPLETE — READY FOR 100-PATH DEVELOPMENT MONTE CARLO
IMPLEMENTATION.
