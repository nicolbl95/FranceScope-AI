# FranceScope V3 — New Mechanism 2A: GLOBAL FINANCIAL CRISIS SPECIFICATION AND CALIBRATION

**Status:** SPEC + CALIBRATION ONLY. No code modified. GFC is modeled as ONE aggregate rare systemic event: `GFC trigger → acute external shock + adverse regime-transition probabilities`. Persistence comes from `macro_regime`, not a GFC state machine.

## 1. REUSABLE EXISTING HOOKS (classified)
- `global_financial_crisis_shock` (V3 external): KEEP_WITH_EXTENSION — feeds `effective_external_shock = external_cycle_shock + global_financial_crisis_shock`.
- `compute_external_cyclical_input(z) = 0.008 * z` (V3 external): KEEP_WITH_EXTENSION — GFC z → external GDP cyclical hook.
- `transition_probabilities(current, adjustments=None)` (V3 macro_regime): KEEP_WITH_EXTENSION — accepts external `adjustments` dict (next-state deltas), clipped ≥0, renormalized.
- `regime_cyclical_input` (V3 macro_regime): KEEP — CRISIS = −0.0364 persistent (NOT the acute GFC loss).
- `sovereign_risk_shock` / `fiscal_stress` (V3 fiscal): KEEP — direct `sovereign_risk_shock` hook exists (default 0); `fiscal_stress` feeds endogenous premium.
- V2 `external_stress_index` (AR(1) z-score, mean 0.6632, noise 0.5971): NOT_NEEDED as GFC hazard input (backward-looking, circular); used only as generic stress.
- V2 `credit_to_households_growth`, `credit_to_nfc_growth`, `ecb_rate`: NOT_NEEDED (no separate banking/credit model).

## 2. GFC ROLE
ACUTE EVENT. Trigger year: acute external shock (via external system) + adverse regime-transition probabilities. Following years: macro_regime carries persistence. `acute GFC shock ≠ CRISIS regime effect` (−0.0364 persistent).

## 3. ANNUAL HAZARD — EMPIRICAL vs PRIOR
Repository history (one 2008 global crisis; 2020 was pandemic, not GFC; France-specific systemic crisis absent) is **insufficient** for an empirical annual probability. → Calibration = **MODEL_PRIOR**, not EMPIRICAL_ESTIMATE. Candidate annual probabilities:
- p=0.02: E(triggers)=0.48; P₀=(0.98)²⁴=0.616; P(≥1)=0.384; P(≥2)=0.083.
- p=0.03: E=0.72; P₀=0.481; P(≥1)=0.519; P(≥2)=0.162.
- p=0.04: E=0.96; P₀=0.375; P(≥1)=0.625; P(≥2)=0.249.

## 4. HAZARD ARCHITECTURE
**A. CONSTANT RARE HAZARD** — SELECTED. `external_stress_index` (B) is backward-looking with noise and would create circularity; evidence for B is weak, so A is preferred. `p_gfc = constant`.

## 5. SELECTED HAZARD
**p_gfc = 0.03** (≈1-in-33 yrs; ~0.72 expected triggers, 52% chance ≥1, 16% chance ≥2 over 2027–2050 — rare but materially possible). Labeled MODEL_PRIOR.

## 6. ACUTE SEVERITY (via external transmission)
`external_cyclical_input = 0.008 * z`. Candidates: MODERATE z=−2→−0.016; CENTRAL z=−3→−0.024; SEVERE z=−4→−0.032. SELECTED **CENTRAL z = −3 → external_cyclical_input = −0.024 (−2.4pp)**, benchmarked to a 2008-type global financial crisis (not Covid).

## 7. REGIME TRANSITION ADJUSTMENT (GFC)
`macro_regime.transition_probabilities(current, adjustments)` interprets `adjustments` as **additive per-next-state probability deltas**: `p' = max(0, base + delta)`, then the row is **renormalized** if it no longer sums to 1 (verified against the implemented API).

The originally proposed vector {EXP −0.45, SLOW +0.10, REC +0.20, CRIS +0.25, RECOV −0.10} is **INCONSISTENT** with that API: applied to SLOWDOWN it yields [EXP 0.000, SLOW 0.599, REC 0.192, CRIS 0.209, RECOV 0.000] — NOT the previously reported 0.106/0.354/0.192/0.348 (those were mistakenly computed from the EXPANSION base). That result also fails the calibration principle (RECESSION+CRISIS = 0.401 < SLOWDOWN 0.599).

**CORRECTED GFC_ADJUSTMENT = {EXPANSION:−0.45, SLOWDOWN:−0.30, RECESSION:+0.30, CRISIS:+0.35, RECOVERY:−0.10}** (additive, clip ≥0, renormalize). Full base→GFC adjusted rows (verified via the module):
- EXPANSION → [E 0.128, S 0.000, R 0.341, C 0.530, Rec 0.000]
- SLOWDOWN  → [E 0.000, S 0.336, R 0.322, C 0.342, Rec 0.000]
- RECESSION → [E 0.000, S 0.045, R 0.500, C 0.455, Rec 0.000]
- CRISIS    → [E 0.000, S 0.000, R 0.337, C 0.281, Rec 0.382]
- RECOVERY  → [E 0.303, S 0.000, R 0.322, C 0.375, Rec 0.000]

For GFC during SLOWDOWN, RECESSION+CRISIS = **0.664** (dominant adverse), with residual SLOWDOWN probability — strong but not deterministic. P(EXPANSION) falls, P(RECESSION)/P(CRISIS) rise materially, CRISIS < 1, rows sum to 1, same rule for every current regime; base matrix unchanged when no GFC.

## 8. CREDIT CHANNEL
**GFC_CREDIT_CHANNEL = DEFERRED_TO_INTEGRATION** — no defensible coefficient; GFC already acts via external shock + regime deterioration. No separate credit shock invented.

## 9. SOVEREIGN-RISK CHANNEL
Direct `sovereign_risk_shock = 0`. GFC → GDP↓ → deficit/debt↑ → endogenous `sovereign_fiscal_risk_premium`↑ (avoid double counting financial stress).

## 10. EVENT DURATION
GFC trigger = ONE YEAR. No multi-year GFC state; persistence via macro_regime.

## 11. RNG CONTRACT
Module deterministic: `gfc_probability(p)`, `gfc_effects(triggered, severity)`. Orchestrator: `u = RNG; triggered = u < p_gfc`.

## 12. DOUBLE-COUNTING MAP
GFC → `global_financial_crisis_shock` → external system → `external_cyclical_input` (acute) AND → regime `adjustments` → possible RECESSION/CRISIS (persistent). NOT added three times. Each output one distinct role.

## 13. DIAGNOSTICS (see CSV)
A no GFC; B central acute external only; C central + regime adjustment; D central while fiscal stress high. Acute (−0.024) vs persistent (regime −0.0364 if CRISIS) kept separate.

## 14. LONG-HORIZON CHECK
p=0.03 → E=0.72 triggers/24y, P₀=0.481, P(≥1)=0.519, P(≥2)=0.162 — reasonable for 2027–2050.

## 15. FUTURE AI-BUBBLE CONTRACT
If considered, AI bubble modifies `p_gfc` or GFC severity — NOT a second crisis engine.

## 16. FUTURE IMPLEMENTATION
`src/francescope/gfc/...`: `gfc_probability`, `gfc_effects(triggered, severity=−3)` returning z and `adjustments` for `transition_probabilities`. RNG in orchestrator. No code this session.
