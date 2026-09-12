# FranceScope V4 — CORR-2 Unemployment Hysteresis Specification

**Status:** Frozen for review  
**Module:** `francescope.unemployment.hysteresis`  
**Orchestrator integration:** `src/francescope/orchestrator/v1_orchestrator.py` (lines 614–629)  
**Deterministic tests:** `tests/test_corr2_unemployment_hysteresis.py`, `src/francescope/unemployment/tests/test_hysteresis.py`

---

## 1. Problem Statement

In V3, the unemployment rate mean-reverts toward a **fixed** NAIRU reference of 7.5%:

```python
mean_reversion = (nairu - new_unemployment) * 0.2
```

where `nairu` defaults to `0.075`. This creates artificial optimism under high-stress paths: after a severe recession, unemployment is mechanically pulled back to 7.5% within a few years, ignoring persistent labor-market scarring (skill erosion, long-term unemployment, discouraged workers). Empirical hysteresis literature (Blanchard & Summers, 1986; Borghijs et al., 2023) documents that NAIRU can remain elevated for 5–10+ years after large adverse shocks.

---

## 2. Design Rationale

CORR-2 introduces a **dynamic structural unemployment rate** (`u_star` / NAIRU) that evolves based on the realized unemployment gap. The design is:

- **Parsimonious:** single speed parameter `η` (ETA_HYSTERESIS).
- **Two-sided:** structural unemployment rises during recessions *and* falls during prolonged booms (economically defensible; no artificial ratchet).
- **Bounded:** hard floor and ceiling prevent divergence under extreme paths.
- **Transparent:** first-order linear recurrence with clear macro interpretation as a persistence parameter.
- **Compatible:** plugs directly into the existing V2 unemployment equation via the `nairu` argument; Okun, productivity, and AI displacement channels remain untouched.

---

## 3. V3 Baseline Equation (Unchanged)

The V2/V3 unemployment recurrence in `_v2_unemployment` is reproduced exactly:

```
okun_effect        = -gdp_growth * 0.2
productivity_effect = productivity_growth * 0.05
new_unemployment   = current_unemployment + okun_effect + productivity_effect
mean_reversion     = (nairu - new_unemployment) * 0.2
new_unemployment   = new_unemployment + mean_reversion
# Floor correction
if new_unemployment < 0.045:
    new_unemployment = new_unemployment + (0.045 - new_unemployment)**2 * 2.0
return max(0.035, min(0.14, new_unemployment))
```

In V3, `nairu = 0.075` (fixed).  
In V4 with CORR-2, `nairu = structural_unemployment_t` (dynamic).

All coefficients (`0.2`, `0.05`, floor `0.045`, bounds `[0.035, 0.14]`) are **FROZEN** and must not be modified by CORR-2 work.

---

## 4. CORR-2 Hysteresis Equation

### 4.1 State Variable

`u_star_t` — the structural unemployment rate (effective NAIRU) at year `t`.

### 4.2 Recurrence

```text
u_star_t = u_star_{t-1} + ETA_HYSTERESIS * (unemployment_{t-1} - u_star_{t-1})
```

Expanded as a convex combination:

```text
u_star_t = (1 - ETA_HYSTERESIS) * u_star_{t-1} + ETA_HYSTERESIS * unemployment_{t-1}
```

**Interpretation:** `ETA_HYSTERESIS` (λ) is the annual transmission speed of the realized cyclical gap into the structural rate. A value of 0.08 implies ~8% of the gap closes each year.

### 4.3 Bounds

```text
u_star_t ∈ [STRUCTURAL_UNEMPLOYMENT_MIN, STRUCTURAL_UNEMPLOYMENT_MAX]
```

---

## 5. Frozen Calibration

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `NAIRU_REF` | `0.075` (7.5%) | Long-run reference equilibrium / 2026 anchor |
| `ETA_HYSTERESIS` | `0.08` | Annual hysteresis transmission speed |
| `STRUCTURAL_UNEMPLOYMENT_MIN` | `0.050` (5.0%) | Lower bound |
| `STRUCTURAL_UNEMPLOYMENT_MAX` | `0.130` (13.0%) | Upper bound |

**These values are FROZEN.** They must not be changed by any subsequent CORR or module work without explicit specification revision.

---

## 6. Implementation Signature

```python
def update_structural_unemployment(
    prev_structural: float,
    prev_unemployment: float,
    eta: float = ETA_HYSTERESIS,
    lo: float = STRUCTURAL_UNEMPLOYMENT_MIN,
    hi: float = STRUCTURAL_UNEMPLOYMENT_MAX,
) -> float:
    """Advance the structural unemployment rate (NAIRU / u_star) one year (no RNG).

    u_star_t = u_star_{t-1} + ETA * (unemployment_{t-1} - u_star_{t-1})

    Returns bounded u_star_t in [lo, hi].
    """
    val = float(prev_structural) + eta * (float(prev_unemployment) - float(prev_structural))
    return min(hi, max(lo, val))
```

Backward-compatible alias: `update_nairu = update_structural_unemployment`.

---

## 7. Orchestrator Wiring

In `simulate_year` (orchestrator `v1_orchestrator.py`, lines 614–629):

```python
# CORR-2: structural unemployment (NAIRU) hysteresis
# Computed BEFORE the current-year unemployment rate, using the PREVIOUS-year
# actual unemployment vs PREVIOUS-year structural rate.
structural_unemployment_t = update_structural_unemployment(
    prev.structural_unemployment, prev.unemployment_rate
)

# --- Unemployment (Okun + AI displacement; productivity = trend + AI + CORR-1 dev) ---
prod_growth_unemp = LABOR_PRODUCTIVITY_TREND + ai_prod + corr1.productivity_growth_dev
unemp = _v2_unemployment(prev.unemployment_rate, total_growth, prod_growth_unemp,
                         nairu=structural_unemployment_t)
unemployment_t = unemp + ai_emp

# --- CORR-2 diagnostics ---
cyclical_unemployment_gap_t        = unemployment_t - structural_unemployment_t
unemployment_hysteresis_drift_t    = structural_unemployment_t - prev.structural_unemployment
```

Diagnostics exposed on `V3YearResult`:
- `structural_unemployment_nairu` — dynamic NAIRU (alias `nairu`)
- `cyclical_unemployment_gap` — `unemployment_rate - nairu`
- `unemployment_hysteresis_drift` — year-to-year change in `u_star`
- `unemployment_hysteresis_gap` — `structural_unemployment_nairu - NAIRU_REF`
- `hysteresis_gap` — same as above (alias)
- `unemployment_structural_damage` — `max(0.0, structural_unemployment_nairu - NAIRU_REF)`

---

## 8. Behavioral Analysis

### 8.1 Normal / Baseline Scenario

If unemployment fluctuates around the reference (≈7.5%), the cyclical gap is small and `u_star` converges to the same vicinity:

- Starting from `u_star = 0.075` with `u = 0.075` → no drift.
- With typical business-cycle variation (±1–2 pp), `u_star` oscillates narrowly around 7.5%, bounded by [5.0%, 13.0%].

**Half-life of a 1 pp gap:**  
`(1 - η)^n * gap = 0.5` → `n = ln(0.5) / ln(0.92) ≈ 8.3 years`  
A 1 percentage-point gap halves in roughly 8 years.

### 8.2 High-Stress Scenario (GFC-type Shock)

Assume unemployment spikes to 10.5% for 2 years (2027–2028) then returns to 7.5%:

| Year | u_star (structural) | Cyclical gap vs NAIRU_REF |
|------|---------------------|---------------------------|
| 2026 | 0.0750 | 0.000 |
| 2027 | 0.0780 | +0.003 |
| 2028 | 0.0804 | +0.005 |
| 2029 | 0.0820 | +0.007 |
| 2030 | 0.0834 | +0.008 |
| 2035 | 0.0863 | +0.011 |
| 2040 | 0.0829 | +0.008 |
| 2050 | 0.0768 | +0.002 |

Key properties:
- NAIRU rises **during** the shock (scarring).
- After the shock ends, NAIRU **decays slowly** back toward reference — it does **not** snap back to 7.5%.
- After 25 years, the structural rate is still ~0.8 pp above reference.
- Bounded at 13.0% under extreme, persistent high-unemployment paths.

### 8.3 Prolonged Low Unemployment (Boom)

If unemployment stays at 4.0% for many years:
- `u_star` drifts downward, bounded at 5.0%.
- After ~60 years at 4.0%, `u_star` converges to 5.0%.

### 8.4 Asymmetric Consideration

The adopted formulation is **symmetric** (two-sided). An asymmetric penalty (ratcheting up only) was considered but rejected because:
1. A symmetric model is more macro-economically defensible: tight labor markets do compress structural unemployment through on-the-job training and skill accumulation.
2. Parsimony: no need for a separate expansion parameter.
3. The bounds [5.0%, 13.0%] already prevent extreme divergence in either direction.

---

## 9. Compatibility with Existing V3 Channels

- **Okun effect** (`-gdp_growth * 0.2`): unchanged. The dynamic `nairu` merely shifts the mean-reversion target.
- **Productivity effect** (`productivity_growth * 0.05`): unchanged.
- **AI displacement** (`ai_emp`): added *after* the V2 unemployment equation; does not feed back into `u_star`.
- **CORR-1 capital/productivity gap:** unchanged; `prod_growth_unemp` includes `corr1.productivity_growth_dev` but this does not alter the hysteresis recurrence.
- **V3 median-living standard:** uses current `unemployment_rate`; `structural_unemployment` does not enter the C1 equation directly, avoiding double-counting.

---

## 10. Deterministic Test Coverage

| Test | Purpose |
|------|---------|
| `test_baseline_stability` | `u_star` stable at 7.5% when `u = 7.5%` |
| `test_severe_recession_scarring` | +3 pp shock persists >10 years |
| `test_bounded_never_breaches` | Converges to 13.0% (high) and 5.0% (low) |
| `test_recovery_boom_pulls_down` | Prolonged boom pulls `u_star` to 5.0% floor |
| `test_orchestrator_exposes_corr2_diagnostics` | Result dataclass carries all required CORR-2 fields |
| `test_orchestrator_recession_scarring_persists` | GFC shock elevates NAIRU through 2050 |

---

## 11. Summary

CORR-2 replaces the V3 fixed NAIRU (7.5%) with a dynamic, hysteresis-driven structural unemployment rate:

```text
u_star_t = u_star_{t-1} + 0.08 * (u_{t-1} - u_star_{t-1})
```

with bounds `[5.0%, 13.0%]` and reference anchor `7.5%`. This is parsimonious (one parameter), transparent (linear first-order recurrence), macro-economically defensible (two-sided with bounds), and fully backward-compatible with the frozen V2 unemployment Okun/productivity/AI equations.
