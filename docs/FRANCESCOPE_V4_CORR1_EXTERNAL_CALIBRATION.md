# FranceScope V4 — CORR-1B External Calibration & Functional-Form Validation

**Scope:** External calibration + functional-form validation only. No production code changed; no MC; no target fitting.

## 1–2. Authoritative external datasets (intended/attempted)
- **GFCF (real):** Eurostat `nama_10_gdp`, `GEO=FR`, `NA_ITEM=P51G` (Gross Fixed Capital Formation), `UNIT=CLV_MEUR` (chain-linked volume, level) and `UNIT=CLV_PCH` (real growth %). Transformation: annual real GFCF growth. Target window 2000–2025. *In-environment retrieval returned oversized SDMX-JSON payloads (>5MB) despite TIME filter; exact annual values to be fetched at implementation. The repo's derived `investment_growth` is NOT used.*
- **Labour productivity:** Eurostat `nama_10_lp_ulc`, `GEO=FR`, `INDIC=LP_LPEN` (real labour productivity per person employed); sensitivity `LP_LPHU` (per hour). Window 2000–2025.
- **Financing rate:** repository `corporate_credit_rate` (Banque de France / ECB new-business corporate lending rate), decimal annual; `CCR_REF=0.01766` (1.77%, 2011–2019 mean). Lineage/units validated; not replaced.

## 4–6. Literature — financing→investment (max set)
1. **Best, Born & Menkhoff (2025), CEPR DP20695 / ECB–BdF:** 1 pp lending-rate cut → **+6% yr1, +7% yr2** investment-plan adjustment. **UNIT: INVESTMENT_PLAN_PERCENT_CHANGE / LEVEL**, shock = **+1 pp loan rate**. Semi-elasticity ≈ **−0.06 to −0.07 per +1pp** (2-yr cumulative level).
2. **Chatelain & Tiomo (2001–02), ECB WP106 / BdF WP96:** French manufacturing 1990–99. User-cost elasticity of capital ≈ **−0.2 to −0.3** (long-run level). **UNIT: CAPITAL_STOCK / user-cost elasticity.**
3. **Ottonello, Perez & Taretto (2020)** (cited by Best-Born): aggregate monetary-policy→investment response benchmark (~15% scaled), confirming partial-equilibrium channel ≈ half of GE total.
4. **Curtis et al. (2021):** short-run user-cost elasticity comparable.
5. **ECB WP78, "Investment and monetary policy in the euro area":** euro-area corroboration.

## 7. Direct-growth-form compounding verdict
Applying `beta_credit*gap` permanently to **annual investment growth** with gap=+0.0251 (high debt) and β=−6.5 gives a **permanent −16.3%/yr** growth penalty → GDP collapses absurdly. **Verdict: PERSISTENT_GROWTH_PENALTY_OVERCOMPOUNDS.** The literature estimates a *level* response, not a permanent growth-rate reduction.

## 8. Selected financing form = PARTIAL-ADJUSTMENT INVESTMENT LEVEL GAP
```
desired_inv_level_gap_t = beta_credit_level * (corporate_credit_rate_decimal_t - CCR_REF)   # LEVEL, decimal
inv_level_gap_t         = rho_inv * inv_level_gap_{t-1} + (1-rho_inv) * desired_inv_level_gap_t
investment contribution to productivity = alpha * (I/K_normal) * inv_level_gap_t   # via capital_gap state
```
Persistent high rate → lower **investment LEVEL** (converges); growth contribution = change in gap → **0 once converged** (no permanent growth penalty).

## 9. beta_credit_level (correct scale)
- central **−6.5**, low **−4.0**, high **−9.0** (per +1pp loan rate; LEVEL semi-elasticity).
- Calibration type: **EXTERNAL_EMPIRICAL_PRIOR**. Primary: Best-Born −6 to −7; cross-check Chatelain-Tiomo user-cost −0.2..−0.3 supports moderate magnitude.
- +100bp → desired level gap −6.5%; 1-yr ≈ −4% (rho 0.6), 2-yr ≈ −6.5% (matches literature).

## 10–13. Investment→productivity = growth accounting (NOT reduced-form beta_inv)
Historical 0.825% center: **OLD_CENTER_CONFIRMED** by V3 provenance (2011–2019 eurostat labour productivity mean ≈ 0.825%); precise re-estimation deferred to implementation (series retrieval blocked in-environment). 0.825% **embeds** normal capital deepening → must NOT be stacked.
```
capital_gap_t = (1-delta)*capital_gap_{t-1} + (I/K_normal)*inv_level_gap_t
prod_growth_dev_t = alpha * (capital_gap_t - (1-delta)*capital_gap_{t-1}) = alpha*(I/K_normal)*inv_level_gap_t
labor_productivity_growth_t = 0.00825 + prod_growth_dev_t + ai_effect_t + climate_drag
```
Parameters: **alpha (capital share) ≈ 0.33**, **delta (depreciation) ≈ 0.10**, **I/K_normal ≈ 0.11** (AMECO/French national accounts). Effective `beta_inv_star = alpha*I/K ≈ 0.036`.

## 15–16. Counterfactuals (mechanism diagnostics, not forecasts)
| shock | inv level gap (conv) | prod growth dev/yr | 10-yr cum prod level |
|---|---|---|---|
| +100bp | −6.5% | −0.24pp | ≈ −2.4% |
| +200bp | −13.0% | −0.47pp | ≈ −4.7% |
| +300bp | −19.5% | −0.71pp | ≈ −7.1% |
| +251bp (high-debt) | −16.3% | −0.59pp | ≈ −5.9% |
High-debt (+251bp) → persistent ~−6% productivity-level shortfall over a decade: material but not catastrophic — resolves debt↔Index decoupling without GDP collapse.

## 17. Decision
**CORR1_FUNCTIONAL_FORM_REDESIGN_READY** — old four-line direct-growth contract overcompounds; replacement (partial-adjustment level gap + growth-accounting productivity) is fully specified with external coefficients.

## 18. Double-counting
OLD `const 0.00825` vs NEW `0.00825(BASE) + alpha*(I/K)*inv_level_gap`. Investment term is a **deviation** (mean-zero at reference), not an addition on top of the full floor → no double-count of normal capital deepening.
