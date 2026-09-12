# FranceScope V3 — Correction C1: Debt / Spread / Fiscal-Reaction SPECIFICATION AND CALIBRATION
**Status:** SPEC + CALIBRATION ONLY. Engine NOT modified. Narrow unit/benchmark sanity gate applied.

## UNIT CONVENTION (authoritative)
- **RATES (decimal fractions):** `france_10y` (V2 OAT), `effective_rate`, `sovereign_fiscal_risk_premium`, ECB. `0.0385 = 3.85% = 385 bps`. bps = decimal×10 000.
- **FISCAL RATIOS (percentage points of GDP):** `public_debt_gdp` (119.45 = 119.45%), `public_deficit_gdp`, `public_revenue_gdp`, `primary_expenditure_gdp`, `public_interest_expenditure_gdp`, `interest_burden`, `fiscal_adjustment`, `exp_cut`, `rev_gain`. `5.48 = 5.48% of GDP`.
- `fiscal_stress`: unitless 0..1.

## 1. V2 PUBLIC-FINANCE REUSED
| Variable | V2 equation | Unit | Reuse |
|---|---|---|---|
| `ecb_policy_rate` | exogenous (anchor 2.25%) | decimal | KEEP |
| `france_10y_government_rate` | `0.017959 + 0.889655*ecb` | decimal | **KEEP** — this IS the full historical French OAT 10Y (ECB source REF_AREA=FR). Do NOT relabel as Bund. |
| `effective_rate` | `0.014541 + 0.342344*france_10y_{t-1}` | decimal | KEEP (gradual lag-1 refinancing) |
| `public_interest_expenditure_gdp` | `effective_rate * public_debt_gdp_{t-1}` | pp GDP | KEEP (non-discretionary) |
| `public_revenue_gdp` | AR(1)+gdp+unemp | pp GDP | KEEP_WITH_EXTENSION (+tax-pressure) |
| `primary_expenditure_gdp` | AR(1)+eps | pp GDP | KEEP_WITH_EXTENSION (−consolidation) |
| `public_expenditure/deficit/debt_gdp` | identities / stock-flow | pp GDP | KEEP |

## 2. MISSING FEEDBACKS (verified)
1–3 debt/deficit/interest → premium: **MISSING**. 4 OAT←premium: **MISSING** (OAT purely ECB). 5 OAT→effective cost: **KEEP** (lag-1). 6–7 stress→exp/rev: **MISSING**.

## 3. FINANCING ARCHITECTURE — SELECTED: B (incremental fiscal-risk premium)
No genuine German-Bund series exists; `france_10y` is itself the French OAT. Relabeling it as a Bund + adding a "France-Germany spread" would double-count French sovereign risk. Therefore:
```
V3 france_oat_10y_t = V2_baseline_t + sovereign_fiscal_risk_premium_t
V2_baseline_t       = 0.017959 + 0.889655*ecb_t          (full French OAT, decimal)
```
The premium is **incremental** and **re-centered at the 2026 reference** (premium≈0 there) so the V2 OAT, which already prices 2026 French risk, is not double-counted.

## 4. SOVEREIGN-RISK PREMIUM (C2, corrected & re-centered)
```
premium_t = PHI*premium_{t-1} + (1-PHI)*[
              B_DEBT*(debt_gdp_t     - 119.45)
            + B_DEF *(deficit_gdp_t  -   5.48)
            + B_INT *(interest_burden_t - 3.31) ]
```
- `PHI=0.60`; `B_DEBT=0.00030` (per +1pp debt → +3 bps decimal), `B_DEF=0.00080` (per +1pp deficit → +8 bps), `B_INT=0.00060` (per +1pp int burden → +6 bps).
- Anchors = 2026 reference (debt 119.45pp, deficit 5.48pp, int burden = `effective_rate_2026`×119.45 ≈ 3.31pp). Premium = 0 at reference → NO permanent intercept premium. Documented calibration (no Bund data for regression).

## 5. ONE CONTINUOUS `fiscal_stress` (0..1)
`fiscal_stress = clamp(0.25·N(debt)+0.25·N(deficit)+0.25·N(int_burden)+0.25·N(premium))`,
`N(debt)=clamp((debt-90)/50)`, `N(deficit)=clamp((deficit-2)/5)`, `N(int)=clamp((int-2)/3)`, `N(premium)=clamp(premium/0.030)`. Engine-only; never an Index component.

## 6. FISCAL REACTION (R2, units explicit)
```
adj_t      = RHO*adj_{t-1} + (1-RHO)*(CAP * fiscal_stress_{t-1})   # CAP = 0.80 PERCENTAGE POINTS GDP/yr
exp_cut_t  = adj_t * 0.60                                          # pp GDP, subtracted from primary
rev_gain_t = adj_t * 0.40                                          # pp GDP, added to revenue
```
`CAP=0.80` means **0.80 pp of GDP**, NOT 80% (fiscal ratios are pp). `RHO=0.50`. Lagged, bounded, stronger under high premium/int burden; no hard `debt>X` austerity; no tax microsim.

## 7. ACCOUNTING DISCIPLINE
Primary vs interest separate; sign conventions preserved; interest never cut as austerity; single consolidated `adj` split → no double-count.

## 8. FUTURE HOOKS (defined, not wired)
`fiscal_spending_drag`=−`exp_cut` (→GDP cyclical ↓); `tax_pressure_effect`=+`rev_gain` (→disposable income/consumption/median ↓); `sovereign_financing_effect`=`premium`/effective-rate change.

## 9. CRISIS HOOK
Reserve `sovereign_risk_shock = 0.0` (default off).

## 10. DETERMINISTIC DIAGNOSTICS (see CSV; Architecture B, no intercept premium)
- **A moderate/near-ref:** premium ≈ 0→+51 bps, OAT 3.67%→4.31%, adj 0.12→0.50 pp. No spurious permanent premium.
- **B high debt/int:** premium 24→181 bps, OAT 4.70%→7.26%, adj 0.23→0.71 pp, debt 178pp.
- **C severe (shock +250 bps):** premium 288→217 bps, OAT ~7.1–7.8%, stress saturates, adj caps 0.735 pp.

## 11. STABILITY
Gradual lag-1 refinancing (weight 0.34); premium mean-reversion (PHI=0.6); capped/saturating reaction (CAP 0.80pp, stress≤1); bounded adjustment (RHO=0.5); ECB-anchored baseline. Loop active but non-explosive; no clipping.

## 12. IMPLEMENTATION LOCATIONS
State dict: add `sovereign_fiscal_risk_premium`, `fiscal_stress`, `fiscal_adjustment`, `sovereign_risk_shock`. New `compute_sovereign_fiscal_risk_premium(...)`. Refactor `compute_france_10y_government_rate` to add premium (L685–697). Insert stress/reaction after interest block (~L1092) before deficit identity (L1104). Expose hooks.
