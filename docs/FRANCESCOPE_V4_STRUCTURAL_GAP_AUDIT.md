# FranceScope V4 — Structural Gap Audit

**Scope:** Diagnostic / architectural only. No code, coefficients, MC, forecasts, historical data, Index, or variables changed.

## 1. Original economic thesis (reconstructed)
FranceScope was intended to represent: demographic aging / shrinking labor force; end of easy tertiary productivity growth; debt–deficit–interest feedback; sovereign financing pressure; credit conditions; investment; capital/productivity feedback; unemployment persistence (hysteresis); income/median-living pressure; de-globalization / weak external demand; European contagion; geopolitical/energy stress; chronic climate damage; crisis persistence; AI productivity upside. The V3 engine implements *foundations* for several of these but leaves the real-economy transmission incomplete.

## 2. Current V3 causal chains (traced in code)
- **Debt loop:** debt/deficit/interest → `compute_target_sovereign_premium` → AR(1) `premium` → `compose_v3_france_oat` → `mortgage_rate`/`corporate_credit_rate` (computed, **stored, never consumed**). `interest_exp = eff_debt_cost * debt` → deficit → debt.
- **Fiscal:** `compute_fiscal_adjustment` (AR1 0.5, cap 0.8) → `apply_fiscal_reaction` → deficit; GDP impact uses **Δ(exp_cut/rev_gain) only** → `fiscal_gdp_contribution`.
- **Unemployment:** `_v2_unemployment` → Okun + 0.05·prod + mean-reversion to `natural_rate=0.075` (0.2/yr). No hysteresis.
- **External:** `CYC_LOAD*z` (mean 0) + GFC; `global_growth_dev` is a deviation; China load = 0.
- **Climate:** constant `-0.001/yr`; disasters OFF.
- **AI:** +~4% cumulative, fades to 0.
- **Median:** derivative of GDP/unemp only.

## 3–11. Mechanism verdicts
- **Productivity trend:** `LABOR_PRODUCTIVITY_TREND=+0.825%/yr` is **unconditional** (not investment/capital/fiscal/credit/recession/aging dependent). Verdict: **TOO_STRONG_EXOGENOUS_FLOOR / STRUCTURAL_LINK_MISSING**. Alone it lifts GDP level **+21.8%** by 2050.
- **Debt→real economy:** high debt raises premium/OAT/credit rates but the chain **dead-ends** — credit rate never enters investment, and `investment_growth` is never used in GDP. Verdict: **missing transmission**; this fully explains debt→192% while Index rises.
- **Fiscal feedback depth:** adjustment is persistent but GDP effect is the *change* only → stabilizes to **zero drag**. Verdict: **impulse-only, not persistent pressure** (unintended property confirmed).
- **Unemployment mean reversion:** strong 0.2/yr pull to 7.5%, no hysteresis. Verdict: **MISSING_HYSTERESIS_CHANNEL** (also mechanical excessive reversion).
- **External structural pressure:** only zero-mean cyclical. Verdict: **STRUCTURAL_EXTERNAL_TREND missing**.
- **Crisis scarring:** one-year acute shock + temporary regime persistence; no capacity damage. Verdict: **MISSING_SCARRING_CHANNEL**.
- **Climate:** constant small drag, no worsening/adaptation. Verdict: **ADEQUATE_SMALL_STRUCTURAL_DRAG** (underrepresents thesis but small).
- **Median living:** optimistic because the **engine** is optimistic (verdict A), not an independent calibration error. Flagged as limitation; no new microsim.
- **AI:** +4% cumulative, small vs trend. Verdict: **MATERIAL_UPSIDE_BUT_NOT_PRIMARY_DRIFT_SOURCE**.

## 12. Positive-drift decomposition (diagnostic, central path 2027–2050)
Net structural GDP level gain ≈ **+16.3%**, composed of: productivity trend **+21.8%**, labor-force decline **−6.1%**, AI **+4.0%**, climate **−2.4%**. Regime and external are zero-mean → no trend. **The persistent expected growth is entirely exogenous productivity + AI, never slowed by debt/fiscal/credit stress.** This is the mathematical source of the upward drift.

## 13. Gap matrix
See `data/audits/economic_system/FRANCESCOPE_V4_STRUCTURAL_GAP_MATRIX.csv` (9 mechanisms, columns: mechanism, original_economic_logic, current_V3_implementation, current_chain_complete, missing_link, likely_bias_direction, affected_core_outputs, materiality, evidence, candidate_action).

## 14–15. Recommended corrections (≤5; mechanisms NOT restored)
Recommended (4): **CORR-1** (P0) close debt→credit→investment→productivity (A+B); **CORR-2** (P1) unemployment hysteresis (C); **CORR-3** (P1) persistent fiscal-pressure drag (G); **CORR-4** (P1) external structural trend (D). Deferred (P2): **CORR-5** crisis scarring (E); **CORR-6** time-varying climate (F).
**Not recommended for restoration:** the old large V3 architecture; China competitive channel; housing/debt/tariff submodels; climate-disaster probability model; AI→GFC/regime; sovereign direct GFC shock; external-stress loadings; full income microsimulation.

## 16. Double-counting
- CORR-1 must **replace** (not add to) the 0.825% floor → otherwise double-counts embedded capital deepening (HIGH risk).
- CORR-2/3/1 all reach unemployment via Okun/GDP → keep natural-rate shift, level drag, and investment channel distinct (MEDIUM).
- CORR-4 trend is a level, distinct from existing cyclical deviation (LOW).
- CORR-5 overlaps regime persistence (MEDIUM).

## 17. No target-based calibration
Corrections are mechanism-driven; outcomes must emerge from mechanisms, not tuned to Index 110 / GDPpc €36k / unemployment 10%.

## 18. Directional impact (direction only)
- CORR-1: GDPpc DOWN, unemployment UP, median DOWN, debt AMBIGUOUS.
- CORR-2: GDPpc DOWN, unemployment UP, median DOWN, debt UP.
- CORR-3: GDPpc DOWN, unemployment UP, median DOWN, debt AMBIGUOUS.
- CORR-4: GDPpc DOWN, unemployment UP, median DOWN, debt AMBIGUOUS.

## 19. Artifacts
- `docs/FRANCESCOPE_V4_STRUCTURAL_GAP_AUDIT.md`
- `data/audits/economic_system/FRANCESCOPE_V4_STRUCTURAL_GAP_MATRIX.csv`
- `data/audits/economic_system/FRANCESCOPE_V4_CORRECTION_PRIORITIES.csv`

## 20. Final decision
**V4_TARGETED_STRUCTURAL_CORRECTIONS_REQUIRED** — the unconditional productivity floor plus dead-end debt/credit and impulse-only fiscal channels produce a structurally optimistic drift inconsistent with ~190% debt/GDP.
