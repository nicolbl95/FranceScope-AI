# FranceScope V5 — Architecture, Scenario Profiles & Sensitivity Results

**Status:** V5 development, testing, the MC100 audit, scenario profiling, and
sensitivity analysis are **100% complete and validated** (688 deterministic
passing tests). This document is documentation-only — no V4/V5 core code,
frozen parameters, or test definitions were modified to produce it.

---

## 1. Design Philosophy: Non-Breaking Opt-In

V5 is a strictly **additive, opt-in** extension of the frozen V4 engine
(`v1_orchestrator.simulate_year` + `monte_carlo_v3`). Every V5 mechanism is
gated behind a per-year boolean flag that **defaults to `False`**, so:

- `V3YearInputs()` with no flags set is **byte-equivalent to V4** — the
  stochastic stream, all CORR-1..4 logic, frozen parameters, and datasets are
  untouched.
- Enabling a flag only *overlays* the V5 mechanism on top of the existing V4
  channel; each V5 function takes an `enabled` argument and returns the exact
  V4 identity (or zero contribution) when `False`.
- No V4 frozen parameter, dataset, or `CORR-1..4` code path is modified by any
  V5 module.

The four V5 opt-in flags (declared on `V3YearInputs`):

| Flag | Default | Module |
|------|---------|--------|
| `enable_v5_ai_regimes` | `False` | AI Stochastic Regimes |
| `enable_v5_crisis_scarring` | `False` | Crisis Scarring |
| `enable_v5_advanced_climate` | `False` | Advanced Climate Drag |
| `enable_v5_eurozone_contagion` | `False` | Eurozone Contagion |

---

## 2. The Four Core V5 Modules

### 2.1 AI Stochastic Regimes — `src/francescope/ai/v5_ai_regimes.py`
Deterministic, RNG-free regime scaler for the *existing* fading AI profile.

- A latent regime (`slow` / `central` / `fast`) resolves an **amplitude
  multiplier** relative to the V4 central = 1.0:
  `V5_AI_REGIME_AMPLITUDES = {"slow": 0.45, "central": 1.0, "fast": 1.70}`.
- `ai_productivity_effect_v5(...)` calls the V4 `ai_productivity_effect` with
  the resolved amplitude. When `enabled=False` it returns the **static V4
  amplitude unchanged** (identity).
- **Anti-double-counting guardrails:**
  - The regime **only multiplies** the existing central-profile amplitude.
  - No permanent productivity-growth floor is added.
  - The contribution still **fades to ~0 by 2050** (inherited from the V4
    profile), so the decay-curve shape is preserved across all regimes.
  - Stochastic regime *switching* (per-path RNG transitions) is deferred
    scaffolding; the carried regime state is supplied by the orchestrator.

### 2.2 Crisis Scarring — `src/francescope/gdp/v5_crisis_scarring.py`
Persistent capital/productivity **hysteresis** following severe recessions.

- Mechanism (deterministic, RNG-free):
  - Recession signal = provisional real-GDP growth shortfall below
    `SCAR_TRIGGER_GROWTH = 0.0`. The orchestrator supplies the **pre-scar**
    total growth so the scar never suppresses its own trigger.
  - On a recession year an incremental negative drag is added; the accumulator
    then partially heals each year (`SCAR_DECAY = 0.80`), leaving a **lingering
    persistent drag** on potential productivity / GDP growth.
  - `SCAR_SENSITIVITY = 0.25` (new drag per unit of recession depth).
- The accumulated gap (`v5_scar_gap`) is applied **once** as an additive
  structural drag term via `compute_structural_gdp_growth(
  v5_crisis_scarring_drag=...)`.
- **Anti-double-counting guardrails:**
  - Separate state (`v5_scar_gap`); does **NOT** feed `CORR-1` `capital_gap`.
  - Strictly a productivity / capital-channel drag; does **NOT** touch
    `CORR-2` NAIRU / labor-market hysteresis.

### 2.3 Advanced Climate Drag — `src/francescope/climate/v5_climate_drag.py`
Replaces the V4 *linear* chronic climate drag with a **non-linear convex
damage function** when enabled.

- V4 (disabled): `drag = BASELINE_DRAG * amplitude`
  (`BASELINE_DRAG = -0.001`, the V4 linear reference).
- V5 (enabled): `drag = BASELINE_DRAG * (a + c*(a-1)^2)` for the clamped
  amplitude `a`, with `CONVEXITY = c = 0.5` and `CAP_AMPLITUDE = 3.0`.
  This is equal to V4 at amplitude 1.0, **convex** (accelerating marginal
  damage) for amplitudes > 1.0, monotonically decreasing in amplitude, and
  **bounded** (amplitudes clamped at `CAP_AMPLITUDE`).
- **Anti-double-counting guardrail (SINGLE ENTRY POINT):**
  - The result is the **`climate_structural_drag`** argument of
    `compute_structural_gdp_growth`. There is **NO second parallel continuous
    climate term**.
  - Does not touch `CORR-1` capital gap, crisis scarring, or any frozen
    parameter / dataset / `CORR-1..4` logic.

### 2.4 Eurozone Contagion — `src/francescope/external/v5_eurozone_contagion.py`
Persistent external/cyclical shock amplifier and sovereign-spread spillover
from Eurozone stress events.

- Mechanism (deterministic, RNG-free):
  - A caller-supplied `eurozone_stress_shock` updates a persistent
    `v5_eurozone_stress_state` that decays gradually
    (`STRESS_DECAY = 0.7`) — i.e. the contagion **persists** after the event.
    `STRESS_SENSITIVITY = 1.0`, `CONTAGION_CYC_LOAD = 0.5`,
    `CONTAGION_PREMIUM_LOAD = 0.01`.
  - The persistent state **amplifies the existing single external cyclical
    hook** (`external_cyclical_input`) and adds a spillover to the **existing
    single sovereign premium path**. No new parallel cyclical or shock variable
    is introduced into GDP composition.
- **Anti-double-counting guardrails (SINGLE HOOKS):**
  - Only `external_cycl` (fed to `compose_real_gdp_growth`) is scaled; no
    second cyclical/shock term is created.
  - Sovereign spread reuses the single `premium_t` → OAT → rates chain.
  - Acute climate shocks stay in `shock_input`; structural drags stay in
    structural growth.

---

## 3. Single Entry Point & Orchestration

All V5 mechanisms converge in **one place**: `v1_orchestrator.simulate_year`.
The orchestrator:

1. Reads the four `enable_v5_*` flags from `V3YearInputs`.
2. Resolves each module's contribution, defaulting to the V4 identity when the
   flag is `False`.
3. Routes every module through its **single designated channel**
   (`climate_structural_drag`, `external_cycl` + `premium_t`,
   `v5_crisis_scarring_drag`, `ai_productivity_effect`), guaranteeing that each
   V5 mechanism is counted **exactly once**.

Scenario configuration is centralized in
`src/francescope/config/v5_profiles.py` via the frozen `V5Profile`
dataclass:

- `apply_to_inputs(inputs)` returns a **copy** of the yearly inputs with the
  profile's flags applied. The eurozone stress proxy is derived per-year from
  the already-drawn `external_cycle_shock`
  (`ez_stress_scale * max(0, -external_cycle_shock)`), so the **stochastic
  stream stays unchanged** and comparisons isolate each mechanism.
- Profiles are `@dataclass(frozen=True)` → immutable and safe to share across
  simulations and tests.

---

## 4. V5 Scenario Profiles

### 4.1 Named Presets (spec-defined)

| Profile | AI | Crisis Scarring | Climate | Eurozone | `ez_stress_scale` |
|---------|----|-----------------|---------|----------|-------------------|
| `BASELINE_V4`       | – | – | – | – | 1.0 |
| `V5_TECH_BOOST`     | ✅ | – | – | – | 1.0 |
| `V5_STRESS_SCAR`    | – | ✅ | – | ✅ | 1.0 |
| `V5_CLIMATE_FOCUS`  | – | – | ✅ | – | 1.0 |
| `V5_BALANCED`       | ✅ | ✅ | ✅ | ✅ | **0.5** (moderate) |
| `V5_FULL`           | ✅ | ✅ | ✅ | ✅ | 1.0 (full) |

Legend: ✅ = flag enabled.

- **`BASELINE_V4`** — all V5 flags `False`; identical to the frozen V4 engine.
  Used as the reference scenario for all sensitivity deltas.
- **`V5_TECH_BOOST`** — AI Regimes only; tests productivity-upsie / -downside
  from slow/central/fast AI adoption paths.
- **`V5_STRESS_SCAR`** — Crisis Scarring + Eurozone Contagion; a
  stress-and-contagion scenario that combines the two downside channels.
- **`V5_CLIMATE_FOCUS`** — Advanced Climate Drag only; tests convex
  accelerating climate damage.
- **`V5_BALANCED`** — all four modules on, but with **moderate** contagion
  exposure (`ez_stress_scale = 0.5`). A holistic "realistic opt-in" profile.
- **`V5_FULL`** — all four modules on at full intensity; the maximal V5
  downside envelope.

### 4.2 Isolated Sensitivity Profiles
Used by the module sensitivity harness to measure each mechanism's *marginal*
impact against `BASELINE_V4`:

| Profile | Enables |
|---------|---------|
| `V5_SCAR_ONLY`     | Crisis Scarring only |
| `V5_EUROZONE_ONLY` | Eurozone Contagion only |

(These reuse the same RNG draws as `BASELINE_V4`; only the flag overlay
differs, so deltas are clean marginal effects.)

---

## 5. Sensitivity & Audit Results

All results below come from the **MC100 comparative audit** (`scripts/
v5_mc100_audit.py`) and the **module sensitivity harness** (`scripts/
v5_module_sensitivity.py`), both run at `seed = 20260815`, `N_PATHS = 100`
(reusing the frozen RNG draws from `monte_carlo_v3.build_path_inputs`). No
MC1000/MC10000 reruns were performed; the audit compares V4 Baseline (all flags
off) against V5 opt-in (flags on) using identical stochastic streams.

### 5.1 Safety Guarantees (validated)
Both `BASELINE_V4` and `V5_FULL` ran with:
- **Zero NaN / Inf** across all metrics.
- **Positive** real GDP per capita and median living standards.
- **Bounded** debt-to-GDP tails.
- **No regressions** introduced into the V4 baseline path.

### 5.2 Main Downside Drivers
Sensitivity analysis isolates **Crisis Scarring** and **Eurozone Contagion** as
the principal downside contributors. Enabling both (`V5_STRESS_SCAR`) and the
full envelope (`V5_FULL`) materially widen the downside distribution:

- Median **FranceScope Composite V3** falls from **145.6 (V4 Baseline) to
  79.2 (Full V5 opt-in)** — a large ordinal contraction of the composite
  index.
- **P90 debt-to-GDP** rises from **235.8% (V4 Baseline) to 554.2% (Full V5
  opt-in)** — a substantially heavier fiscal tail.
- By contrast, **AI Regimes** and **Advanced Climate Drag** (in isolation)
  produce comparatively milder median shifts, confirming that the scarring /
  contagion persistence channels — not the convex climate or AI regime scaling
  alone — dominate the V5 downside.

### 5.3 Interpretation
- The persistence / hysteresis design of Crisis Scarring (`SCAR_DECAY = 0.80`)
  and Eurozone Contagion (`STRESS_DECAY = 0.70`) means shocks leave **lingering
  drags**, compounding over the 2027–2050 horizon.
- `V5_BALANCED` (moderate contagion, `ez_stress_scale = 0.5`) sits between the
  Baseline and `V5_FULL` envelopes, offering a calibrated "realistic opt-in"
  reference for downstream reporting.

---

## 6. Validation

- **Deterministic test suite:** 688 passing tests, including the dedicated
  `tests/v5/` battery (`test_v5_ai_regimes`, `test_v5_crisis_scarring`,
  `test_v5_climate_drag`, `test_v5_eurozone_contagion`, `test_v5_profiles`).
- Profiles are verified as **frozen dataclasses**; `BASELINE_V4` produces
  identity inputs (all flags `False`, `eurozone_stress_shock == 0.0`); each
  named profile matches its spec'd flag set; and `get_profile` / `V5_PROFILES`
  correctly register all six presets.
- No V4 frozen parameter, dataset, or `CORR-1..4` logic was modified by V5
  work, and no Monte Carlo reruns were required to produce this documentation.

---

## 7. File Map

| Concern | Path |
|---------|------|
| AI Regimes | `src/francescope/ai/v5_ai_regimes.py` |
| Crisis Scarring | `src/francescope/gdp/v5_crisis_scarring.py` |
| Advanced Climate Drag | `src/francescope/climate/v5_climate_drag.py` |
| Eurozone Contagion | `src/francescope/external/v5_eurozone_contagion.py` |
| Scenario profiles | `src/francescope/config/v5_profiles.py` |
| Single orchestration point | `src/francescope/orchestrator/v1_orchestrator.py` (`simulate_year`) |
| MC100 comparative audit | `scripts/v5_mc100_audit.py` |
| Module sensitivity harness | `scripts/v5_module_sensitivity.py` |
| Tests | `tests/v5/` |
