# FranceScope V3 — Correction E1: Minimal Climate SPECIFICATION AND CALIBRATION

**Status:** SPEC + CALIBRATION ONLY. V2 forecast engine NOT modified. V3 GDP/fiscal/external/demographic code NOT modified. This document defines the smallest defensible two-channel climate extension of the existing V2 climate logic.

## 1. EXISTING V2 CLIMATE / ENERGY IMPLEMENTATION (inventory)

| Variable | Formula / source | Unit | Downstream | Classification |
|---|---|---|---|---|
| `climate_damage` | `ScenarioDriver(central=0.002, unc=0.002, pers=0.8, bounds=(0.0,0.010))`; in `compute_real_gdp`: `growth -= climate_damage * 0.5` | decimal damage magnitude (0..0.01) | real GDP growth (−0 to −0.005/yr) | LEGACY_REDUNDANT for V3 structural GDP; its CALIBRATION (central 0.002 × load 0.5) is REUSED to anchor the chronic drag |
| `oil_price_shock` / `oil_shock` | `ScenarioDriver(central=0, unc=0.015, pers=0.2)`; `growth -= oil_shock*0.2` | decimal | real GDP (energy) | KEEP (energy/oil channel — NOT climate) |
| `brent_crude_oil_price` / `brent_growth` | `ScenarioDriver(central=0, unc=0.05, pers=0.3)` | decimal price growth | energy_inflation, GDP energy | KEEP (energy channel — NOT climate) |
| `geopolitical_shock` | `ScenarioDriver(central=0, unc=0.012, pers=0.15)`; `growth -= geopolitical_shock*0.15` | decimal | real GDP | KEEP (geopolitical — NOT climate) |
| `carbon_price` | feeds `energy_inflation` (`brent_crude_oil_price, carbon_price, exchange_rate`) | price | energy_inflation only | KEEP (transition/price channel — separate from physical damage) |
| physical climate data (`climate_heat_thresholds`, `climate_station_panel`, `drought_energy_canonical`, `lsh/sqr` raw) | raw physical series | physical | none GDP-linked | MISSING as a GDP-calibrated chronic path (no damage elasticity in repo) |

No historical fit backs `climate_damage`; it is a pure forward scenario draw. No current fiscal use of climate variables exists.

## 2. MEANING OF CURRENT `climate_damage`

It is an **annual persistent random draw** (persistence 0.8), treated as a positive damage magnitude, multiplied by an arbitrary 0.5 GDP weight. It is:
- NOT a deterministic structural trend,
- NOT a one-off disaster,
- a single undifferentiated noise that **conflates chronic drag and acute disaster**.

Why insufficient for V3: V3 separates structural / cyclical / shock. A single mixed random draw cannot (a) enter structural GDP as a persistent trend, nor (b) represent a rare acute event distinctly. It is cleanly **reinterpretable by reusing its calibration** (central 0.002 × 0.5 load = −0.001/yr) as the chronic-drag magnitude, while the disaster is split out.

## 3. MINIMAL TWO-CHANNEL ARCHITECTURE (selected)

```
climate_structural_drag_t      -> structural GDP growth   (persistent, deterministic, tiny)
major_climate_disaster_shock_t -> shock_input (GDP)        (rare acute, one-year)
```

Both physical-climate channels only. Heat/drought/fire/flood/agri/insurance/health/adaptation/infrastructure are NOT separate states; their aggregate macro effect is implicit in the two channels.

## 4. CHRONIC CLIMATE DAMAGE — CALIBRATION

Repository evidence for a GDP-calibrated climate trend is **insufficient** (physical data only, no damage elasticity). Preferring reuse over invention, the selected chronic drag reuses the V2 calibration directly:

```
CLIMATE_DRAG_BASELINE = - (0.002 * 0.5) = -0.001   # decimal annual real-GDP-growth contribution
```

i.e. **−0.10 percentage point per year**, constant (maximally persistent). This is the SELECTED CENTRAL path — zero invented trend.

**Missing calibration need (explicit):** a defensible climate→GDP damage elasticity/path from physical data (or an institutional estimate) to calibrate any slope. Until then the central path is the constant V2-anchored −0.001. A "stronger by 2050" sensitivity (ramp to −0.002) is provided ONLY as diagnostic CASE C, not the central selection.

## 5. DOUBLE-COUNTING PROTECTIONS

- physical climate damage → `climate_structural_drag` + `major_climate_disaster_shock` (climate channel only)
- energy-price shock → existing `oil_shock` / `brent` channel (unchanged)
- carbon price → existing `energy_inflation` (transition/price channel, unchanged)
- `geopolitical_shock` → unchanged, NOT relabeled as climate

V2 already subtracts climate/oil/geopolitical/fiscal separately; the split preserves that separation. No oil/geopolitical energy shock is relabeled as climate damage.

## 6. DISASTER SHOCK

```
major_climate_disaster_shock = 0.0   # default
unit: decimal contribution to annual real-GDP growth
examples: 0.0 = none; -0.005 = -0.5pp one-year shock
```

No hazard probability / duration / type / location modeled now. The climate module defines only economic transmission; the orchestrator may later draw events.

## 7. PERSISTENCE / RECOVERY

Selected: **one-year shock, no carryover**. No evidence in repo supports multi-year climate disaster dynamics; inventing recovery AR(1) is avoided. `major_climate_disaster_shock` affects only the year it is drawn.

## 8. STRUCTURAL GDP CONTRACT (future implementation)

```
structural_growth_t = labor_force_growth
                    + labor_productivity_growth
                    + ai_productivity_effect
                    + climate_structural_drag          # <- chronic channel

real_gdp_growth_t   = structural_growth
                    + cyclical_input                    # external cyclical (V3-D2)
                    + shock_input                       # major_climate_disaster_shock + others
```

`structural_growth.py` is NOT modified in this task.

## 9. FISCAL HOOK

Assessed and DEFERRED. No existing equation supports a cheap climate fiscal output; reconstruction/adaptation spending would require a new fiscal module. Reuse not available.

```
CLIMATE_FISCAL_PRESSURE = DEFERRED
```

## 10. CANDIDATES (2–3, parsimonious)

- **A. Reuse V2 `climate_damage` driver directly as chronic term** — REJECTED. Conflates chronic+disaster, non-deterministic, arbitrary 0.5 load, not structural.
- **B. Deterministic constant chronic drag = V2 central×load (−0.001) + separate disaster shock** — **SELECTED**. Minimal, zero new data, no invented trend, compatible with V3 GDP contract, clean double-count separation.
- **C. Gradual deterministic trend from physical climate data** — OPTIONAL_FUTURE. No GDP-calibrated elasticity in repo; would require inventing a mapping. Deferred until calibration available.

## 11. DETERMINISTIC DIAGNOSTICS (see CSV; no Monte Carlo)

- CASE A (no climate): drag 0, disaster 0 → total 0.
- CASE B (moderate chronic): drag −0.001, disaster 0 → total −0.001 (−0.10pp/yr).
- CASE C (stronger by 2050, sensitivity): ramp −0.001(2027)→−0.002(2050), avg ≈ −0.0015.
- CASE D (major one-year disaster): drag −0.001 + disaster −0.005 → that year −0.006; next year returns to −0.001.

## 12. LONG-HORIZON CHECK (selected constant path = −0.001)

| Year | climate_structural_drag |
|---|---|
| 2027 | −0.001 |
| 2030 | −0.001 |
| 2040 | −0.001 |
| 2050 | −0.001 |

Averages: 2027–2030 = −0.001; 2031–2040 = −0.001; 2041–2050 = −0.001; 2027–2050 = −0.001.

Checks pass: no explosive negative growth, no permanent collapse, no duplicate energy effect (oil/carbon channels untouched).

## 13. FUTURE MONTE CARLO CONTRACT

Later simulation treats climate as:
- **baseline chronic path** (`climate_structural_drag`, central −0.001) **+ modest path-level amplitude uncertainty** (e.g. ±0.0005 around the drag), and separately
- **`major_climate_disaster_shock`** drawn as rare acute events on `shock_input`.

No five climate scenarios; no stochastic draws implemented in this task. The same `shock_input` already carries external/other shocks, so disaster coherency is preserved.

## 14. IMPLEMENTATION LOCATIONS (future, NOT done here)

- New `src/francescope/climate/...` module exposing `compute_climate_structural_drag(...)` and `major_climate_disaster_shock` input (default 0), deterministic.
- Feed `climate_structural_drag` into `compose_real_gdp_growth` via `structural_growth` (extend `compute_structural_gdp_growth`), and `major_climate_disaster_shock` into `shock_input`.
- Remove V2 `climate_damage` direct GDP term for the V3 path (calibration reused, mechanism replaced).

(End of specification)
