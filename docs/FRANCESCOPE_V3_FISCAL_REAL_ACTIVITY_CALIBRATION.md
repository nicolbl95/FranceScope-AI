# FRANCESCOPE V3 — Fiscal Real-Activity Transmission Calibration

## Status
V3 FISCAL REAL-ACTIVITY CALIBRATION COMPLETE — READY FOR IMPLEMENTATION.

The prior direct V2 term `-0.3*fiscal_stress` was scale-invalid (V2 stress
~+/-0.01 shock vs V3 [0,1] index) and has been removed. No V2 demand equation
ingests V3 adjusted fiscal quantities, so a minimal, externally-calibrated
transmission is defined here.

## 1. Level vs Impulse decision
**CHANGE/IMPULSE architecture is selected.** A constant fiscal-adjustment LEVEL
multiplied every year imposes a permanent annual GDP-growth penalty even when
policy stops tightening — economically wrong. Fiscal consolidation is a *change
in stance*; its growth-rate effect should occur when the stance moves, not
forever. The CHANGE form yields a one-time growth drag during tightening and a
lasting GDP *level* difference, but no permanent negative growth contribution
after the stance stabilizes.

## 2. Architecture
fiscal_gdp_contrib_pp_t =
    - SPENDING_MULT * delta_exp_cut_t
    - REVENUE_MULT  * delta_rev_gain_t
delta_exp_cut_t  = exp_cut_t  - exp_cut_{t-1}
delta_rev_gain_t = rev_gain_t - rev_gain_{t-1}
fiscal_gdp_contrib_decimal = fiscal_gdp_contrib_pp_t / 100.0
total_growth += fiscal_gdp_contrib_decimal

exp_cut/revenue_gain are already in **percentage points of GDP**; the /100
converts to decimal growth. Normalized fiscal_stress is NOT used.

## 3. Central constants (implementation contract)
FISCAL_SPENDING_MULTIPLIER = 0.8   # GDP pp per 1 pp GDP spending impulse
FISCAL_REVENUE_MULTIPLIER = 0.6     # GDP pp per 1 pp GDP revenue impulse
(No ranges in the contract; ranges below are for later sensitivity only.)

## 4. Sign convention
expenditure_cut>0 (tighter) and revenue_gain>0 (tighter) both -> NEGATIVE GDP
contribution (via the leading minus). If consolidation reverses (delta<0), the
contribution turns positive.

## 5. Authoritative evidence
- Banque de France WP (2016), France: govt-expenditure multiplier ~1.0 on impact,
  insignificant after ~3 years.
- ECB WP 1760 (2015), France: spending-reduction multiplier -0.92 (Y1), -0.71 (Y2);
  revenue -1.05 (Y1), -0.87 (Y2).
- European Commission (2015): avg multiplier "a bit below unity"; expenditure >
  revenue shocks.
- Bank of Greece / euro-area panel: aggregate ~0.5; revenue more costly in recession.
Central spending 0.8 (conservative vs 1.0 impact), revenue 0.6 (conservative).

## 6. Double-counting guard
Only the deliberate exp_cut / rev_gain reaction quantities are used. Automatic
stabilizers (deficit/debt/stress responses to GDP) are already handled by
existing identities; they are NOT a second fiscal multiplier.

## 7. Unemployment / median living
Untouched. Transmission is fiscal impulse -> GDP growth -> Okun -> median living
via the existing recurrence. No fiscal->unemployment or fiscal->median coefficient.

## 8. Level-vs-impulse proof (high stress)
First-year growth drag ~-0.22 pp GDP; from year 2
onward delta_exp_cut=0 so CHANGE contribution = 0 (LEVEL would keep ~-0.22 pp
EVERY year = rejected). No return of the -10/-20pp artifact.

## 9. Control vs high stress (first 5 yrs, CHANGE)
- yr1: control contrib -0.00117 dec (exp_cut 0.097); high contrib -0.00216 dec (exp_cut 0.180)
- yr2: control contrib -0.00058 dec (exp_cut 0.146); high contrib -0.00108 dec (exp_cut 0.270)
- yr3: control contrib -0.00029 dec (exp_cut 0.170); high contrib -0.00054 dec (exp_cut 0.315)
- yr4: control contrib -0.00015 dec (exp_cut 0.182); high contrib -0.00027 dec (exp_cut 0.338)
- yr5: control contrib -0.00007 dec (exp_cut 0.189); high contrib -0.00013 dec (exp_cut 0.349)

## 10. Long-run (high stress to 2050)
Consolidation converges (adj -> 0.600 pp, exp_cut -> 0.360 pp).
After convergence delta=0, so the annual GDP-growth contribution returns to 0:
temporary drag during tightening, permanent *level* difference, no permanent
growth penalty.

## 11. Sensitivity contract
Later: LOW (spending 0.5 / revenue 0.3), CENTRAL (0.8 / 0.6), HIGH (1.0 / 0.9).
Central is deterministic in the first orchestrator; stochastic amplitude is a
later Monte-Carlo concern, not now.

## 12. Credit->investment (unchanged)
OAT->credit = PASS; credit->investment = FAIL_NOT_WIRED. Out of scope here.
