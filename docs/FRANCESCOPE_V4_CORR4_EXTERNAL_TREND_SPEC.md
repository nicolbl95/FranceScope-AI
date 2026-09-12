# FranceScope V4 — CORR-4 Structural External Trend & International Growth Drag Specification

**Status:** Implemented and frozen  
**Module:** `francescope.external.structural_trend`  
**Orchestrator integration:** `src/francescope/orchestrator/v1_orchestrator.py` (lines 560–568, 587, 607, 698–700)  
**Deterministic tests:** `tests/test_corr4_external_trend.py`

---

## 1. Problem Statement

In V3, external trade and international demand shocks enter French GDP **only** through an i.i.d. cyclical shock `z` with zero expected mean:

```python
external_cyclical_input_t = CYC_LOAD * z   # 0.008 * z
```

This shock is a **transient cyclical deviation** — it affects the cyclical GDP hook in `compose_real_gdp_growth` but does **not** alter structural GDP growth. Once the shock passes (`z = 0`), its effect vanishes immediately.

This design misses a key macro-economic reality: long-term structural headwinds (de-globalization, European fragmentation, shift in global demand, slow European partner growth) impose a **persistent drag** on France's structural growth path. CORR-4 introduces this channel as a distinct, bounded, mean-reverting structural drag.

---

## 2. Design Rationale

CORR-4 is designed to be:

- **Parsimonious:** single AR(1) state variable (`external_structural_drag_t`) with two parameters (persistence `ρ`, baseline drag `BASE`).
- **Distinct from cyclical shocks:** the i.i.d. `external_cycle_shock` (z) continues to feed the cyclical hook exactly as in V3. CORR-4 operates on structural GDP only.
- **Mean-reverting:** shocks decay with persistence `ρ = 0.90`, converging back to the baseline structural drag `BASE = -0.0010` (-0.10 pp/yr).
- **Bounded:** hard floor `-0.0050` (-0.50 pp/yr) and ceiling `+0.0010` (+0.10 pp/yr) prevent divergence under extreme scenarios.
- **Zero-drift at baseline:** with `trend_shock_t = 0.0`, the process is stationary at `BASE`, introducing no spurious long-term bias.
- **Compatible:** additive with climate, fiscal, and other structural drags in `compute_structural_gdp_growth` without double-counting.

---

## 3. V3 Baseline Equations (Unchanged)

The V3 external contagion module in `contagion.py` is reproduced exactly:

```python
external_cyclical_input_t = CYC_LOAD * z
# where CYC_LOAD = 0.008, z = external_cycle_shock (default 0.0)
```

This feeds the cyclical component of GDP:
```python
cyclical_input = regime_cyclical_input + external_cyclical_input
total_growth = compose_real_gdp_growth(structural, cyclical_input=cyclical_input, ...)
```

The structural GDP growth in V3 excluded external effects entirely:
```python
structural_growth = labor_supply_growth + labor_productivity_growth + ai_productivity_effect
```

All coefficients (`CYC_LOAD = 0.008`, `GLOBAL_LOAD = 0.006`, `EU_BASE_WEIGHT = 0.6`, etc.) are **FROZEN**.

---

## 4. CORR-4 Structural Trend Equation

### 4.1 State Variable

`external_structural_drag_t` — persistent structural external drag on annual real GDP growth (decimal rate).

### 4.2 AR(1) Recurrence

```python
external_structural_drag_t = ρ * external_structural_drag_{t-1} + (1 - ρ) * BASE + trend_shock_t
external_structural_drag_t = clamp(external_structural_drag_t, DRAG_MIN, DRAG_MAX)
```

Expanded:
```python
raw = RHO_EXTERNAL_TREND * prev_drag + (1.0 - RHO_EXTERNAL_TREND) * EXTERNAL_STRUCTURAL_DRAG_BASE + trend_shock_t
external_structural_drag_t = max(EXTERNAL_DRAG_MIN, min(EXTERNAL_DRAG_MAX, raw))
```

**Interpretation:**
- `ρ = 0.90`: 90% of the previous year's structural drag persists; 10% mean-reverts to baseline.
- `BASE = -0.0010`: long-run structural drag of -0.10 pp/yr from de-globalization/trade fragmentation.
- `trend_shock_t`: exogenous structural innovation (default `0.0` in deterministic runs; Monte Carlo can draw path-specific values).
- **Half-life** of a shock: `n = ln(0.5) / ln(0.90) ≈ 6.6 years`. A one-off adverse shock halves in about 6.6 years.

### 4.3 Bounds

```python
EXTERNAL_DRAG_MIN = -0.0050   # -0.50 pp/yr max drag
EXTERNAL_DRAG_MAX = +0.0010   # +0.10 pp/yr max boost
```

---

## 5. Frozen Calibration

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `EXTERNAL_STRUCTURAL_DRAG_BASE` | `-0.0010` | Baseline persistent drag (-0.10 pp/yr) |
| `RHO_EXTERNAL_TREND` | `0.90` | AR(1) persistence coefficient |
| `EXTERNAL_DRAG_MIN` | `-0.0050` | Lower bound (-0.50 pp/yr) |
| `EXTERNAL_DRAG_MAX` | `0.0010` | Upper bound (+0.10 pp/yr) |

**These values are FROZEN.** They must not be changed by any subsequent CORR or module work without explicit specification revision.

---

## 6. State Variables

### 6.1 Persistent State (`V3PersistentState`)

```python
external_structural_drag: float = EXTERNAL_STRUCTURAL_DRAG_BASE  # -0.0010
```

Initialized to the frozen baseline at 2026. Carried forward year-to-year as the lag-1 state for the AR(1) recurrence.

### 6.2 Yearly Input (`V3YearInputs`)

```python
external_trend_shock: float = 0.0  # exogenous structural shock innovation (default off)
```

### 6.3 Diagnostics (`V3YearResult`)

| Field | Meaning |
|-------|---------|
| `external_structural_drag` | Canonical persistent structural drag (decimal rate) |
| `external_structural_trend` | Alias for `external_structural_drag` |
| `external_trade_drag` | Alias for `external_structural_drag` |

---

## 7. Orchestrator Wiring

In `simulate_year` (orchestrator `v1_orchestrator.py`, lines 560–568):

```python
# --- CORR-4: persistent external / de-globalization structural trend (V4) ---
# Dynamic AR(1) structural drag (distinct from the i.i.d. external cycle
# shock that feeds the cyclical GDP hook). The lag-1 drag (prev state) plus
# a mean-reversion to the baseline and the year's i.i.d. trend shock innovate
# the new persistent drag, which is hard-bounded. trend_shock_t = 0 (default)
# mean-reverts the drag to EXTERNAL_STRUCTURAL_DRAG_BASE (-0.0010).
external_drag_t = compute_external_structural_drag(
    prev.external_structural_drag, inputs.external_trend_shock
)
```

The drag is passed to `compute_structural_gdp_growth`:
```python
structural = compute_structural_gdp_growth(
    labor_force_growth,
    productivity_trend,
    ai_productivity_effect=ai_prod,
    climate_structural_drag=climate_drag,
    fiscal_structural_drag=fiscal_structural_drag_t,
    external_structural_drag=external_drag_t,   # <-- CORR-4
    v5_crisis_scarring_drag=scar_drag,
)
```

And recorded in the persistent state:
```python
next_state = V3PersistentState(
    ...
    external_structural_drag=external_drag_t,
)
```

---

## 8. Behavioral Analysis

### 8.1 Baseline Scenario (No Shocks)

With `trend_shock_t = 0.0` and initial `external_structural_drag = -0.0010`:

```python
drag_t = 0.90 * (-0.0010) + 0.10 * (-0.0010) + 0.0 = -0.0010
```

The process is **stationary at -0.0010** in every year. No spurious drift, no ratcheting.

**Structural GDP growth impact:** `-0.0010` (-0.10 pp/yr) subtracted from structural growth every year.

### 8.2 Adverse Structural Shock

A one-off `trend_shock = -0.004` in 2027:
- **2027:** `drag = 0.90*(-0.0010) + 0.10*(-0.0010) + (-0.004) = -0.0050` (hits lower bound)
- **2028:** `drag = 0.90*(-0.0050) + 0.10*(-0.0010) + 0.0 = -0.0046`
- **2029:** `drag = 0.90*(-0.0046) + 0.10*(-0.0010) + 0.0 = -0.0042`
- Decays gradually back toward `-0.0010` with half-life ~6.6 years.

### 8.3 Prolonged Adverse Trend

Sustained `trend_shock = -0.0003` every year:
- Process mean-reverts to a new stationary point below `-0.0010`.
- After 24 years, settles around `-0.0040` (well within bounds).
- Structural GDP growth is persistently depressed by ~-0.40 pp/yr relative to no-trend baseline.

### 8.4 Favorable Structural Shock

A positive `trend_shock = +0.002`:
- Pushes drag toward the upper bound `+0.0010` (capped).
- After the shock ends, decays back to `-0.0010`.
- Maximum boost to structural growth: +0.10 pp/yr.

---

## 9. No Double Counting

CORR-4 is carefully bounded to avoid double-counting with existing channels:

| Channel | Mechanism | CORR-4 Interaction |
|---------|-----------|-------------------|
| **V3 Cyclical Shock** | i.i.d. `external_cycle_shock` → `external_cyclical_input` → cyclical GDP hook | CORR-4 is structural, not cyclical. The cycle shock never touches `external_structural_drag`. Verified by `test_shock_independence_orthogonal`. |
| **CORR-1 Financing** | Sovereign premium → OAT → corporate credit → investment → capital → productivity | CORR-1 operates through financing costs; CORR-4 operates through external demand/trends. Distinct channels, additive in structural GDP. |
| **CORR-2 Hysteresis** | Dynamic NAIRU based on unemployment gap | CORR-4 uses external drag only; no overlap with labor-market channels. |
| **CORR-3 Fiscal** | Debt-to-GDP + tax-burden persistent drag | CORR-3 is domestic fiscal pressure; CORR-4 is external/global. Distinct channels, additive in structural GDP. |
| **Climate Drag** | Chronic climate structural drag | Climate is environmental; CORR-4 is trade/external demand. Distinct, additive. |

---

## 10. Implementation Summary

### 10.1 Module: `francescope.external.structural_trend`

```python
EXTERNAL_STRUCTURAL_DRAG_BASE = -0.0010
RHO_EXTERNAL_TREND = 0.90
EXTERNAL_DRAG_MIN = -0.0050
EXTERNAL_DRAG_MAX = 0.0010

def compute_external_structural_drag(prev_drag, trend_shock_t=0.0, ...):
    raw = RHO * prev_drag + (1-RHO) * BASE + trend_shock_t
    return clamp(raw, DRAG_MIN, DRAG_MAX)
```

### 10.2 Module: `francescope.external.external_trend` (Legacy/Amplitude Variant)

A simpler amplitude-based variant exists in `external_trend.py`:
```python
EXTERNAL_STRUCTURAL_DRAG = -0.001
MAX_EXTERNAL_DRAG = 0.01

def compute_external_structural_drag(amplitude=1.0):
    return clamp(EXTERNAL_STRUCTURAL_DRAG * amplitude, -MAX_EXTERNAL_DRAG, MAX_EXTERNAL_DRAG)
```

This variant is **not** used by the orchestrator (which imports from `structural_trend.py`). It may be retained for backward compatibility or removed if no callers exist.

### 10.3 Orchestrator Integration

- **Input:** `inputs.external_trend_shock` (default `0.0`)
- **State:** `prev.external_structural_drag` (initialized to `-0.0010`)
- **Output:** `external_drag_t` → `compute_structural_gdp_growth(..., external_structural_drag=external_drag_t)`
- **Diagnostics:** `external_structural_drag`, `external_structural_trend`, `external_trade_drag`

---

## 11. Deterministic Test Coverage

| Test | Purpose |
|------|---------|
| `test_frozen_parameters_untouched` | Constants are at specified values |
| `test_baseline_convergence` | Zero shock → converges to `-0.0010` |
| `test_persistence_and_decay` | AR(1) decay verified; shock halves in ~6.6 years |
| `test_shock_innovation_applied` | Trend shock added before clamp |
| `test_bounds_safeguard` | Extreme inputs stay within `[-0.0050, 0.0010]` |
| `test_structural_growth_integrates_external_drag` | Drag enters structural GDP exactly |
| `test_orchestrator_converges_to_baseline` | Full path with zero shock stays at `-0.0010` |
| `test_orchestrator_shock_persists_and_reduces_growth` | Persistent shock depresses growth |
| `test_orchestrator_distinct_from_iid_cyclical_shock` | Cycle shock does not affect structural drag |
| `test_orchestrator_diagnostic_recorded` | Diagnostics present and correct |
| `test_baseline_zero_drift` | No spurious drift under neutral conditions |
| `test_persistent_multi_decade_drag` | Sustained adverse trend produces multi-decade drag |
| `test_shock_independence_orthogonal` | Cycle shock and trend shock are orthogonal |

---

## 12. Summary

CORR-4 replaces the V3 external-only-cyclical-shock design with a **persistent, mean-reverting structural external trend**:

```text
external_structural_drag_t = clamp(
    0.90 * drag_{t-1} + 0.10 * (-0.0010) + trend_shock_t,
    -0.0050,
    +0.0010
)
```

This is parsimonious (one state variable, two parameters), transparent (AR(1) with clear macro interpretation as external demand persistence), macro-economically defensible (bounded, mean-reverting, baseline-anchored), and fully backward-compatible with the frozen V3 external cycle shock and all existing structural GDP channels.
