# FRANCESCOPE V3 — Pre-Monte-Carlo Decision

## Part A — Credit->Investment Materiality: DEFER_ACCEPTED_LIMITATION

- No annual investment-growth historical series exists in the repository; the V2
  investment coefficients were pre-estimated externally and hardcoded:
  `inv_growth = -0.000874 + 1.0179*gdp_growth - 0.019476*unemp_change_pp`.
- Financing rates ARE available (corp credit 2003-2026 monthly; OAT 1986-2026):
  2011-2025 corp credit rate 1.09-4.74% (mean 2.20%); 2015-2021 compressed 1.09-1.52%.
- corr(credit, gdp_growth)=0.115 (weak/perverse); corr(credit, unemployment)=-0.486
  (collinear with the slack channel already in the V2 equation).
- Identification is weak/unstable: the only large financing move (2022-24 ECB
  tightening) is confounded with the energy/Covid shock; excluding 2020-21 leaves
  almost no variation. Adding credit would largely double-count the cyclical
  channel already embedded in GDP growth.
- Candidate sign would be negative (correct) but unstable and not robust.
- Counterfactual +100bp: plausible elasticity -0.3..-0.5 -> -0.3..-0.5pp
  investment growth -> ~0.1pp GDP (investment ~21.5% of GDP) -> negligible for
  real_gdp_per_capita / unemployment / median_living.
- Decision: DEFER_ACCEPTED_LIMITATION (known, accepted limitation; not a blocker).

## Part B — RNG Readiness

Stochastic inputs (all currently fixed/default in deterministic V1):
| input | class | draw | note |
|-------|-------|------|------|
| regime_uniform_draw | CALIBRATED_READY | YEARLY | Uniform(0,1) |
| gfc_uniform_draw | CALIBRATED_READY | EVENT/YR | p=0.03 prior |
| external_cycle_shock | DISTRIBUTION_PENDING | YEARLY | needs dist |
| climate_amplitude | DISTRIBUTION_PENDING | PATH | needs dist |
| major_climate_disaster_shock | DISTRIBUTION_PENDING | EVENT/YR | can stay 0 first MC |
| ai_productivity_amplitude | DISTRIBUTION_PENDING | PATH | needs dist |
| ai_employment_displacement_amplitude | DISTRIBUTION_PENDING | PATH | tie to prod amp |

Correlations: NONE required for first MC — regime/GFC/external/climate/AI are
independent high-level drivers; GFC already propagates through one external system.

Minimum RNG calibration (4 tasks + 1 deferral): external_cycle_shock,
ai_productivity_amplitude, climate_amplitude, ai displacement (joint with prod);
climate disaster may remain deterministic (0) in first 100-path run.

## Gate
READY_AFTER_RNG_CALIBRATION — no demonstrated core-output blocker remains;
credit->investment is a deferred, immaterial limitation.
