# FranceScope V4 — CORR-1 Calibration: Financing → Investment → Productivity

**Scope:** Calibration / model-design only. No production code modified; no MC/MC1000; no forecast; coefficients not fitted to targets.

## 1. Historical data coverage (repository)
- `investment_growth`: 2011–2026 (n=16), **decimal**, **derived from the V2 investment equation** (not observed). No observed GFCF / capital-formation level exists in repo.
- `corporate_credit_rate`: 2003–2026 (n=24), **observed**, **stored in PERCENT units** (1.09–4.74%); model `_v2_corporate_credit_rate` uses **decimal** → unit conversion required.
- `france_oat`: 1986–2026 observed.
- `real_gdp_growth` 2011–2026; `unemployment_rate` 2010–2026.
- **No labor-productivity or GFCF series exists anywhere in the repository.**

## 2. Existing V2 investment equation (baseline)
`investment_growth = -0.000874 + 1.0179*gdp_growth - 0.019476*unemployment_change_pp` (decimal; unemp_change in percentage points). Reproduction on repo `investment_growth` recovers coefficients exactly.

## 3–6. Financing-augmented investment model
- Financing variable: **`corporate_credit_rate` only**, as a **LEVEL GAP vs reference** (`corporate_credit_rate_decimal − CCR_REF`), NOT a Δ (a Δ would make the penalty vanish once rates stabilize high — exactly the persistence failure CORR-1 must fix).
- Estimation on repo `investment_growth` (2012–2025, n=14): in EVERY specification (full / level-gap / Δ / excl-2020-21) the financing coefficient is **numerically ≈ 0 (1e-16)** and `gdp`/`unemployment` reproduce the V2 equation exactly. `corr(credit, investment) = −0.007`. Collinearity: `corr(credit, unemployment_change) ≈ 0.43`.
- **Result: `beta_credit` is perfectly unidentified from repo data** — the dependent series was *generated* by the V2 equation, which has no credit term, so it contains zero credit variation. COVID/2022–24 tightening dominates the only credit variation and is confounded with macro shocks.

## 7–9. Investment → productivity link & decomposition
No repo productivity series → `beta_inv` **cannot be identified internally**. Proposed parsimonious, reference-centered design (preserves historical 0.825% center, does NOT stack):
`labor_productivity_growth_t = 0.00825 + beta_inv*(investment_growth_t − INVESTMENT_REF) + ai_effect_t + climate_drag`
where `INVESTMENT_REF = mean(2011–2019 investment_growth) = 0.01491`. At normal investment, gap=0 → productivity = 0.00825 (old center reproduced).

## 10–11. Neutrality & persistence
At reference financing/investment the new model collapses to the old V3 central productivity path (no unconditional negative correction). Simple contemporaneous/lagged investment effect preferred; no capital-stock state required.

## 12. Counterfactuals (parametric; betas external)
Using V3 sovereign equations, high-debt (debt≈192%, interest≈4%) → premium≈+222bp → OAT≈6.07% → `corporate_credit_rate≈4.28%` → **+251bp above CCR_REF (1.77%)**. Effect on investment_growth = `beta_credit*+0.0251`; on productivity = `beta_inv*beta_credit*0.0251`; 10-yr cumulative GDP ≈ `beta_inv*beta_credit*0.0251*10`. With prior-audit plausible `beta_credit = −0.3..−0.5` per +100bp, a +251bp gap implies persistent investment depression of ~−0.8 to −1.3pp, transmitted to productivity/GDP via `beta_inv`. (Prior audit judged the *direct* investment→GDP effect "negligible ~0.1pp" but **excluded the new investment→productivity channel**, which is the material addition.)

## 13. High-debt materiality
Current high-debt V3 paths sit ~+251bp above normal financing → through the calibrated (external) chain they would now incur a **persistent, material real-economy penalty** — resolving the debt↔Index decoupling.

## 14. Double-counting prevention
- OLD: `labor_productivity_growth = 0.00825` (constant).
- NEW: `0.00825(BASE) + beta_inv*investment_gap(mean-zero at reference)`.
The 0.825% is retained as the **BASE center**; the investment term is a **deviation**, not an addition on top of the full floor → no double-counting of normal capital deepening.

## 15–16. Parsimony & external requirements
Final CORR-1 uses ONE financing variable, the V2 investment equation + one financing term, ONE `beta_inv`, and ONE reference center. Two coefficients require external evidence:
- **`beta_credit`** (investment elasticity to corporate-credit-rate gap): `EXTERNAL_CALIBRATION_REQUIRED` (plausible −0.3..−0.5 per +100bp per prior audit / macro literature).
- **`beta_inv`** (investment→productivity elasticity): `EXTERNAL_CALIBRATION_REQUIRED` (no repo productivity series; obtain from capital-share / accelerator / EU investment-TFP studies).

## 17. Final contract
```
corporate_credit_rate_gap_t = corporate_credit_rate_decimal_t - CCR_REF   # CCR_REF = 0.01766
investment_growth_t = -0.000874 + 1.0179*gdp_growth_t - 0.019476*unemployment_change_pp
                       + beta_credit * corporate_credit_rate_gap_t        # beta_credit < 0, EXTERNAL
investment_gap_t = investment_growth_t - INVESTMENT_REF                  # INVESTMENT_REF = 0.01491
labor_productivity_growth_t = 0.00825 + beta_inv*investment_gap_t
                             + ai_productivity_effect_t + climate_structural_drag   # beta_inv EXTERNAL
```

## 19. Artifacts
`docs/FRANCESCOPE_V4_CORR1_CALIBRATION.md`; `data/audits/economic_system/FRANCESCOPE_V4_CORR1_INVESTMENT_CALIBRATION.csv`; `_PRODUCTIVITY_CALIBRATION.csv`; `_COUNTERFACTUALS.csv`; `_IMPLEMENTATION_CONTRACT.csv`.

## 17/20. Classification
**B. CORR1_PARTIALLY_CALIBRATED_EXTERNAL_COEFFICIENT_REQUIRED** — equation structure, financing variable, reference centers, and double-count-safe decomposition are fully specified and ready; `beta_credit` and `beta_inv` must be supplied from external evidence before implementation.

## 18. Sanity (no target fitting)
Assessment based on coefficient stability (unidentified→external), economic sign (credit<0, investment→prod>0), historical fit (reproduces V2 + 0.825% center at reference), mechanism magnitude, and neutrality — **not** against GDPpc/Index targets.
