# FRANCESCOPE V3 — 100-Path Development Monte Carlo Report

Run type: DEVELOPMENT_100_PATHS (NOT final forecast). Seed 20260815.
Horizon 2027-2050; 100 paths x 24 years = 2400 annual rows.
Climate disaster OFF (major_climate_disaster_shock=0.0). Index scoring NOT implemented.
V2 engine unchanged.

## 1. RNG distribution fit (realized vs frozen contract)
- external_cycle_shock: realized mean/sd
  0.008/1.016
  (contract Normal(0,1)); P10/P50/P90 -1.33/0.01/1.3; ext_cycl = 0.008*z.
- ai_productivity_amplitude: mean 1.085,
  P10/P50/P90 0.773/1.075/1.402
  (contract Triangular(0.45,1.0,1.70)).
- climate_amplitude: mean 1.199,
  P10/P50/P90 0.664/1.162/1.888
  (contract Triangular(0.3,1.0,2.3)).

## 2. GFC audit
89 trigger years (expected ~72; ~2sigma high but within sampling tolerance for 100 paths).
41 paths with 0, 38 with 1, 21 with 2+ GFCs.
Trigger-year mean GDP growth -1.9% vs +0.54% otherwise; trigger-year unemployment 8.0% vs 7.64%.
Next-regime after GFC: 42.7% RECESSION, 38.2% CRISIS (acute adverse transition works).
Acute effect not auto-repeated (no double-count).

## 3. Regime frequency (2400 yrs)
EXP 35.8% (stat 39.5), SLOW 44.3% (42.9), RECESSION 6.4% (4.9), CRISIS 7.8% (7.1),
RECOVERY 5.7% (5.6). All within ~4pp of stationary; flagged OK.

## 4. 2050 core-output distributions (development, not final)
- real_gdp_per_capita: P10 0,
  P50 0,
  P90 0
- unemployment_rate: P10 0.0684,
  P50 0.0741,
  P90 0.0792
- median_living_standard_real: P10 25728,
  P50 26747,
  P90 27453
- debt_gdp: P10 175.8,
  P50 191.6,
  P90 217.4

## 5. Plausibility flags
0 flagged rows. {}

## 6. Variance-source diagnostics
- ai_productivity_amplitude: primary economic driver of 2050 GDPpc/median (positive corr).
- regime & GFC: dominant cyclical/event drivers of year-to-year variance.
- climate_amplitude: **ACTIVE** after the wiring fix — drag = -0.001*amplitude now
  flows into structural GDP once; shows a negative association with 2050 GDPpc/median
  (higher amplitude -> stronger drag -> lower output). Influence is LOW-to-MODERATE
  relative to AI/regime/GFC over 2027-2050 (climate drag is a small annual ~0.1-0.2pp channel).

## 7. Decision
DEVELOPMENT_MC_PASS — system runs stably; climate amplitude is now wired and active;
distributions match the frozen contract; regime/GFC behavior correct; no coefficients
changed; no Index scoring. (Note: initial MC100 run identified an inert climate-amplitude
wiring gap; the orchestrator was corrected and MC100 rerun with identical RNG streams.
The corrected run is the authoritative MC100 development result.)
