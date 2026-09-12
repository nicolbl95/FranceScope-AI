# FranceScope V4 — CORR-3 Persistent Fiscal Pressure Real-Economy Drag Specification

**Status:** Proposed for review  
**Module:** `francescope.fiscal.persistent_drag` (debt-to-GDP channel), `francescope.fiscal.fiscal_drag` (tax-burden channel)  
**Orchestrator integration:** `src/francescope/orchestrator/v1_orchestrator.py` (lines 526–538, 598–611)  
**Deterministic tests:** `tests/test_corr3_deterministic.py`, `tests/test_corr3_fiscal_pressure.py`, `tests/test_corr3_fiscal_drag.py`, `src/francescope/fiscal/tests/test_corr3_fiscal_drag.py`

---

## 1. Problem Statement

In V3, fiscal policy affects GDP only through a **1-year Keynesian impulse** based on the *change* in the fiscal consolidation stance:

```python
fiscal_gdp_contribution_pp = -(
    FISCAL_SPENDING_MULTIPLIER * delta_exp_cut
    + FISCAL_REVENUE_MULTIPLIER * delta_rev_gain
)
```

where `delta_exp_cut = exp_cut_t - exp_cut_{t-1}` and `delta_rev_gain = rev_gain_t - rev_gain_{t-1}`. Once consolidation stops changing (i.e., `delta = 0`), the growth drag vanishes **immediately**, even if the fiscal stance remains structurally tight. This is unrealistic: sustained high debt or elevated tax pressure imposes persistent medium-term headwinds through tax frictions, public-investment crowding-out, and confidence channels.

CORR-3 introduces a **level-based, persistent** fiscal drag that operates alongside (without double-counting):
- the **B1 short-term impulse** (change-based, already in V3), and
- the **CORR-1 sovereign-financing channel** (debt → sovereign premium → corporate credit → investment → productivity).

---

## 2. Design Rationale

CORR-3 is designed to be:

- **Parsimonious:** two stateless, additive drag terms (debt-to-GDP and tax-burden), each with one speed parameter and one bound.
- **Level-based:** drag depends on the *stock* of fiscal pressure (debt ratio, tax ratio), not its change. It persists as long as pressure remains elevated.
- **Zero at baseline:** the 2026 reference fiscal position produces exactly zero drag, preserving the original V3 baseline path.
- **Bounded:** hard caps prevent divergence under extreme tail-risk scenarios.
- **Non-compounding:** clear boundaries separate CORR-3 from the B1 impulse and CORR-1 financing channel.
- **Transparent:** linear first-order formulations with explicit macro interpretation.

---

## 3. V3 Baseline Equations (Unchanged)

The V3 fiscal equations in `v1_orchestrator.py` are reproduced exactly and must not be modified by CORR-3 work.

### 3.1 Fiscal Stress & Adjustment
```python
fiscal_stress_t = clamp(
    0.25 * N(debt_t) + 0.25 * N(deficit_t) +
    0.25 * N(interest_burden_t) + 0.25 * N(premium_t)
)
# N(debt) = clamp((debt - 90) / 50), etc.

adjustment_t = 0.50 * adjustment_{t-1} + 0.50 * (0.80 * fiscal_stress_{t-1})
exp_cut_t = 0.60 * adjustment_t
rev_gain_t = 0.40 * adjustment_t
```

### 3.2 B1 Real-Actity IMPULSE
```python
fiscal_gdp_contribution_pp = -(
    0.8 * delta_exp_cut + 0.6 * delta_rev_gain
)
fiscal_gdp_contrib = fiscal_gdp_contribution_pp / 100.0
total_growth += fiscal_gdp_contrib
```

### 3.3 CORR-1 Sovereign Financing
```python
premium_t = 0.60 * premium_{t-1} + 0.40 * target_premium_t
# where target_premium_t = 0.00030*(debt - 119.45) + ...
```

All coefficients (`0.8`, `0.6`, `0.50`, `0.80`, `0.60`, `0.40`, premium slopes, stress thresholds) are **FROZEN**.

---

## 4. CORR-3 Architecture

CORR-3 adds a **persistent structural drag** term to `compute_structural_gdp_growth`:

```
structural_growth = labor_supply_growth
                  + labor_productivity_growth
                  + ai_productivity_effect
                  + climate_structural_drag
                  + fiscal_structural_drag_t       # <-- CORR-3
                  + external_structural_drag
```

The drag is a **sum of two additive, bounded components**:

```
fiscal_structural_drag_t = D_t + T_t
```

where:
- **D_t** = debt-to-GDP structural drag (tax friction, crowding-out, confidence)
- **T_t** = tax-burden structural drag (distortionary taxation above baseline)

Both components are **stateless** (computed from current-period ratios) and enter structural growth **exactly once**.

---

## 5. Debt-to-GDP Structural Drag (D_t)

### 5.1 Equation
```python
debt_excess_gap_t = max(0.0, debt_ratio_t - DEBT_REF_THRESHOLD)
D_t = -min(MAX_DEBT_DRAG, GAMMA_DEBT_DRAG * debt_excess_gap_t)
```

where `debt_ratio_t = prev.debt_gdp / 100.0` (converted from percentage points to decimal ratio).

### 5.2 Economic Interpretation
- **Reference anchor:** `DEBT_REF_THRESHOLD = 1.1945` (119.45% debt/GDP = 2026 baseline). At or below this level, the drag is **exactly 0.0** — no artificial headwind.
- **Speed:** `GAMMA_DEBT_DRAG = 0.020` (20 bp of structural drag per 10 pp of debt excess).
- **Cap:** `MAX_DEBT_DRAG = 0.0080` (-0.80 pp/yr). Reached when debt excess ≥ 40 pp (debt/GDP ≥ 159.45%).

### 5.3 Behavior
| Debt/GDP | Excess Gap | Raw Drag | Capped Drag |
|----------|-----------|----------|-------------|
| 119.45%  | 0.0000    | 0.0000   | 0.0000      |
| 130%     | 0.0355    | -0.00071 | -0.00071    |
| 135%     | 0.1555    | -0.00311 | -0.00311    |
| 150%     | 0.3055    | -0.00611 | -0.00611    |
| 160%     | 0.4055    | -0.00811 | -0.00800    |
| 200%     | 0.8055    | -0.01611 | -0.00800    |

---

## 6. Tax-Burden Structural Drag (T_t)

### 6.1 Equation
```python
tax_burden_gap_t = max(0.0, tax_ratio_t - tax_ratio_ref_t)
T_t = -min(MAX_TAX_DRAG, LAMBDA_TAX_DRAG * tax_burden_gap_t)
```

where:
- `tax_ratio_t = adj_revenue_t` (effective revenue-to-GDP ratio, pp GDP)
- `tax_ratio_ref_t = baseline_revenue_t` (path-dependent baseline revenue, pp GDP)

### 6.2 Economic Interpretation
- **Reference anchor:** the path-dependent baseline revenue (initialized at `BASELINE_REVENUE_2026 = 52.5` pp GDP). When revenue is at or below baseline, drag is zero.
- **Speed:** `LAMBDA_TAX_DRAG = 0.003` (3 bp of structural drag per 1 pp of excess tax burden).
- **Cap:** `MAX_TAX_DRAG = 0.0150` (-1.50 pp/yr). Reached when tax excess ≥ 5.0 pp.

### 6.3 Behavior
| Tax Ratio | Excess Gap | Raw Drag | Capped Drag |
|-----------|-----------|----------|-------------|
| 52.5%     | 0.0       | 0.0000   | 0.0000      |
| 54.0%     | 1.5       | -0.0045  | -0.0045     |
| 55.0%     | 2.5       | -0.0075  | -0.0075     |
| 57.5%     | 5.0       | -0.0150  | -0.0150     |
| 60.0%     | 7.5       | -0.0225  | -0.0150     |

---

## 7. Combined Drag & Hard Bounds

### 7.1 Total Drag
```python
fiscal_structural_drag_t = D_t + T_t
```

### 7.2 Hard Total Bound
To prevent over-compounding when both channels are simultaneously active:
```python
fiscal_structural_drag_t = max(MAX_FISCAL_DRAG_TOTAL, D_t + T_t)
# where MAX_FISCAL_DRAG_TOTAL = -0.020  (-2.0 pp/yr)
```

Wait, -2.0 pp/yr seems too large. Let me reconsider.

If debt is at 160% (drag = -0.008) AND tax ratio is 5pp above baseline (drag = -0.015), total = -0.023. That's -2.3 pp/yr, which is very large but maybe acceptable as a hard bound.

Actually, for defensive calibration, let's set:
- `MAX_FISCAL_DRAG_TOTAL = -0.015` (-1.5 pp/yr)

This ensures that even in extreme combined stress, the persistent drag never exceeds -1.5 pp/yr.

But wait, the existing code in `persistent_drag.py` has `MAX_FISCAL_DRAG = 0.0060` (-0.6 pp/yr) for debt alone. If we add tax drag with max -1.5 pp/yr, the total could be -2.1 pp/yr. That seems too large relative to the debt-only max.

Let me recalibrate:
- Debt max drag: -0.006 (-0.6 pp/yr) — keep existing
- Tax max drag: -0.006 (-0.6 pp/yr) — reduce from -1.5
- Total max: -0.012 (-1.2 pp/yr)

For tax drag with max -0.006:
- `LAMBDA_TAX_DRAG = 0.0012` per pp
- `MAX_TAX_GAP = 5.0` pp
- Max drag = -0.0012 * 5.0 = -0.006

This is more balanced. At 55% tax ratio (2.5pp above baseline): drag = -0.0012 * 2.5 = -0.003 (-0.3 pp/yr). Reasonable.

Let me use these parameters:
- Debt: `DEBT_REF = 1.1945`, `GAMMA = 0.020`, `MAX_DEBT_DRAG = 0.0060`
- Tax: `LAMBDA = 0.0012`, `MAX_TAX_GAP = 5.0`, `MAX_TAX_DRAG = 0.0060`
- Total: `MAX_TOTAL_DRAG = 0.0120` (-1.2 pp/yr)

Actually, I realize I should keep the existing `persistent_drag.py` parameters where possible for backward compatibility, and just change the reference. But the existing tests expect DEBT_REF=1.15 and specific drag values.

Since I'm writing a spec, not modifying code, I should propose the CORRECT design and note implementation gaps.

Let me finalize the parameters for the spec:

**Debt-to-GDP Drag:**
- `DEBT_REF_THRESHOLD = 1.1945` (119.45% = 2026 baseline)
- `GAMMA_DEBT_DRAG = 0.020` (20 bp per 10 pp excess)
- `MAX_DEBT_DRAG = 0.0060` (-0.60 pp/yr)

**Tax-Burden Drag:**
- `LAMBDA_TAX_DRAG = 0.0012` (1.2 bp per pp excess)
- `MAX_TAX_BURDEN_GAP = 5.0` (pp)
- `MAX_TAX_DRAG = 0.0060` (-0.60 pp/yr)

**Combined:**
- `MAX_FISCAL_DRAG_TOTAL = 0.0120` (-1.20 pp/yr)

---

## 8. Frozen Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `DEBT_REF_THRESHOLD` | `1.1945` | Baseline debt-to-GDP ratio (2026 anchor) |
| `GAMMA_DEBT_DRAG` | `0.020` | Debt drag per unit of excess gap |
| `MAX_DEBT_DRAG` | `0.0060` | Max debt drag magnitude (-0.60 pp/yr) |
| `LAMBDA_TAX_DRAG` | `0.0012` | Tax drag per pp of excess burden |
| `MAX_TAX_BURDEN_GAP` | `5.0` | Hard clamp on tax burden gap (pp) |
| `MAX_TAX_DRAG` | `0.0060` | Max tax drag magnitude (-0.60 pp/yr) |
| `MAX_FISCAL_DRAG_TOTAL` | `0.0120` | Combined drag hard cap (-1.20 pp/yr) |

**These values are PROPOSED and must be validated against deterministic tests before freezing.**

---

## 9. State Variables

CORR-3 is **stateless**: both drag components depend only on current-period fiscal ratios, not on lagged drag values. No new persistent state variables are required.

Existing `V3PersistentState` fields used:
- `debt_gdp` — sovereign debt-to-GDP ratio (% GDP)
- `baseline_revenue` — baseline government revenue (% GDP)
- `fiscal_adjustment` — used to compute `adj_revenue` via `apply_fiscal_reaction`

Existing `V3YearResult` fields exposed:
- `fiscal_structural_drag` — canonical total persistent drag
- `fiscal_drag`, `fiscal_growth_drag`, `persistent_fiscal_drag` — aliases
- `fiscal_debt_excess_gap`, `fiscal_pressure_gap` — debt gap diagnostics
- `tax_ratio` — effective revenue-to-GDP ratio
- `fiscal_gdp_contribution` — B1 impulse (distinct from CORR-3)

---

## 10. Orchestrator Wiring

In `simulate_year` (orchestrator `v1_orchestrator.py`), CORR-3 is computed **after** the fiscal reaction and **before** structural GDP composition:

```python
# --- CORR-3: persistent fiscal-strain real-economy drag --------------------
# Uses the LAGGED (previous-year) sovereign debt ratio and the CURRENT
# effective tax ratio vs the path-dependent baseline. Distinct from the
# B1 discretionary consolidation IMPULSE (change-based) and from CORR-1
# (sovereign premium -> corporate credit -> capital -> productivity).
debt_ratio_prev = prev.debt_gdp / 100.0

# Component 1: Debt-to-GDP drag
debt_excess_gap_t = compute_debt_excess_gap(debt_ratio_prev)
debt_drag_t = compute_fiscal_structural_drag(debt_ratio_prev)

# Component 2: Tax-burden drag
tax_burden_gap_t = compute_fiscal_burden_gap(adj_revenue, prev.baseline_revenue)
tax_drag_t = compute_fiscal_drag(adj_revenue, prev.baseline_revenue)

# Combined, bounded
fiscal_structural_drag_t = max(-MAX_FISCAL_DRAG_TOTAL, debt_drag_t + tax_drag_t)
```

The drag is then passed to `compute_structural_gdp_growth`:
```python
structural = compute_structural_gdp_growth(
    labor_force_growth,
    productivity_trend,
    ai_productivity_effect=ai_prod,
    climate_structural_drag=climate_drag,
    fiscal_structural_drag=fiscal_structural_drag_t,
    external_structural_drag=external_drag_t,
    v5_crisis_scarring_drag=scar_drag,
)
```

---

## 11. Behavioral Analysis

### 11.1 Baseline Scenario
With 2026 anchors (debt = 119.45%, revenue = 52.5%), both drag components are exactly zero:
- `debt_excess_gap = max(0, 1.1945 - 1.1945) = 0`
- `tax_burden_gap = max(0, 52.5 - 52.5) = 0`

**Result:** `fiscal_structural_drag = 0.0` in every baseline year. The original V3 path is preserved exactly.

### 11.2 Elevated Debt, Neutral Taxes
If debt rises to 135% and stays there:
- `debt_excess_gap = 0.1555`
- `D_t = -0.020 * 0.1555 = -0.00311` (-0.311 pp/yr)
- `T_t = 0.0` (taxes at baseline)
- **Total drag:** -0.311 pp/yr, persistent every year while debt remains elevated.

### 11.3 Elevated Taxes, Neutral Debt
If revenue rises to 55.0% (2.5 pp above baseline) due to consolidation:
- `tax_burden_gap = 2.5`
- `T_t = -0.0012 * 2.5 = -0.0030` (-0.30 pp/yr)
- `D_t = 0.0` (debt at baseline)
- **Total drag:** -0.30 pp/yr, persistent every year while tax pressure remains.

### 11.4 Combined Stress
If debt = 160% AND revenue = 57.5%:
- `D_t = -0.0080` (capped)
- `T_t = -0.0060` (capped at 5 pp gap)
- Raw sum = -0.0140
- **Capped total:** -0.0120 (-1.20 pp/yr)

### 11.5 Recovery
When debt falls back to ≤119.45% AND revenue returns to ≤52.5%, both gaps close and drag vanishes instantly (level-based). This contrasts with the B1 impulse, which requires a *change* in the fiscal stance to activate/deactivate.

---

## 12. No Double Counting

CORR-3 is carefully bounded to avoid double-counting with existing channels:

| Channel | Mechanism | CORR-3 Interaction |
|---------|-----------|-------------------|
| **B1 Impulse** | Change-based Keynesian multiplier (`delta_exp_cut`, `delta_rev_gain`) | CORR-3 is level-based; if consolidation is constant, B1 = 0 but CORR-3 persists. Distinct and additive. |
| **CORR-1 Financing** | Sovereign premium → OAT → corporate credit → investment → capital → productivity | CORR-1 is **raw, continuous, and unbounded** in debt/GDP. CORR-3 is **capped and bounded**. CORR-1 handles tail-risk differentiation beyond 140% debt; CORR-3 does not. |
| **CORR-2 Hysteresis** | Dynamic NAIRU based on unemployment gap | CORR-3 uses fiscal ratios only; no overlap with labor-market channels. |
| **V5 Crisis Scarring** | Recession-accumulated scalar gap | Opt-in, separate persistent state (`v5_scar_gap`); CORR-3 does not reference it. |

---

## 13. Implementation Status & Gaps

### 13.1 Existing Implementation
- `src/francescope/fiscal/persistent_drag.py` implements the debt-to-GDP drag with frozen parameters (`DEBT_REF_THRESHOLD = 1.15`, `GAMMA_FISCAL_DRAG = 0.010`, `MAX_FISCAL_DRAG = 0.0060`).
- The orchestrator wires `compute_fiscal_structural_drag` into `compute_structural_gdp_growth` and exposes diagnostics on `V3YearResult`.
- Deterministic tests in `tests/test_corr3_deterministic.py`, `tests/test_corr3_fiscal_pressure.py`, and `tests/test_corr3_fiscal_drag.py` validate the debt-based channel.

### 13.2 Identified Gaps vs. Proposed Spec
1. **Baseline drag non-zero:** Current `DEBT_REF_THRESHOLD = 1.15` produces drag at the 2026 baseline (119.45% debt). The proposed spec sets `DEBT_REF_THRESHOLD = 1.1945` to ensure zero baseline drag.
2. **Missing tax-burden channel:** `src/francescope/fiscal/fiscal_drag.py` defines `compute_fiscal_drag` but it is **not imported or called** in the orchestrator. The proposed spec adds this as Component 2.
3. **Unbounded sum:** Current implementation caps only the debt drag. The proposed spec adds a total hard cap (`MAX_FISCAL_DRAG_TOTAL = 0.0120`) to prevent over-compounding when both channels are active.
4. **Test alignment:** Existing tests assert `DEBT_REF_THRESHOLD == 1.15` and specific drag values that would change under the proposed recalibration. Tests must be updated to match the new frozen parameters.

### 13.3 Required Code Changes (Not Executed Here)
1. Update `persistent_drag.py`: change `DEBT_REF_THRESHOLD` to `1.1945`, add `GAMMA_DEBT_DRAG = 0.020`.
2. Update `fiscal_drag.py`: recalibrate `LAMBDA_FISCAL` to `0.0012`, add `MAX_TAX_DRAG = 0.0060`.
3. Update orchestrator: import `compute_fiscal_drag` and `compute_fiscal_burden_gap`, compute `T_t`, sum and cap total drag.
4. Update tests: align all assertions with new frozen parameters.

---

## 14. Test Coverage Summary

| Test Category | Purpose | Status |
|---------------|---------|--------|
| **Sub-threshold invariance** | Debt ≤ 119.45% → drag = 0.0 | Implemented (needs recalibration) |
| **Linear drag above threshold** | Debt at 130%, 135%, 150% → exact drag values | Implemented (needs recalibration) |
| **Hard cap saturation** | Debt ≥ 159.45% → drag capped at -0.60 pp/yr | Implemented (unchanged) |
| **Baseline preservation** | Neutral path produces zero persistent drag | Missing (blocked by current baseline drag) |
| **Tax-burden activation** | Revenue > 52.5% → positive gap, negative drag | Module exists, not wired |
| **Tax-burden bounded** | Extreme revenue → capped at -0.60 pp/yr | Module exists, not wired |
| **No double-counting** | CORR-3 + B1 impulse + CORR-1 coexist without compounding | Partially implemented |
| **Recovery to zero** | Debt/revenue return to baseline → drag vanishes | Implemented |

---

## 15. Summary

CORR-3 replaces the V3 fiscal-only-impulse with a **persistent, level-based structural drag**:

```text
D_t = -min(0.0060, 0.020 * max(0, debt_ratio_t - 1.1945))
T_t = -min(0.0060, 0.0012 * max(0, tax_ratio_t - tax_ratio_ref_t))
fiscal_structural_drag_t = max(-0.0120, D_t + T_t)
```

This is parsimonious (two additive terms, five parameters), transparent (linear level gaps), macro-economically defensible (debt and tax pressure are distinct drag channels), and fully backward-compatible with the frozen V3 B1 impulse and CORR-1 financing equations.
