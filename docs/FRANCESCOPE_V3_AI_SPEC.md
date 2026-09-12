# FranceScope V3 — AI Productivity / Employment Specification (New Mechanism 3A)

Date: 2026-08-23. SPECIFICATION + CALIBRATION ONLY. No code implemented.
This is the FINAL new V3 foundation mechanism. Keep exactly two direct AI
channels: productivity and employment displacement.

## 1. Reusable existing hooks (classification)
- `compute_structural_gdp_growth(labor_supply_growth, labor_productivity_growth, ai_productivity_effect=0.0, climate_structural_drag=0.0)` — AI hook EXISTS (default 0). **KEEP_WITH_EXTENSION**.
- V2 `compute_unemployment_rate(current, gdp_growth, productivity_growth)` adds deltas `-gdp_growth*0.2 + productivity_growth*0.05 + mean_reversion`. AI displacement = an ADDITIONAL decimal-pp delta (separate from Okun/productivity term). **KEEP**.
- `labor_force_growth` (D5A), `employment_rate`, `macro_regime`, `gfc` — **KEEP**.
- V2 generic productivity ScenarioDriver, `TECHNOLOGY_AI_INNOVATION` registry block — **KEEP / LEGACY_OPTIONAL** (not used as AI channel).
- No empirical French GenAI productivity data in repo — **MISSING / EXTERNAL_BENCHMARK_REQUIRED**.

## 2. Two channels only
- A. PRODUCTIVITY: `ai_productivity_effect_t` = decimal annual real-GDP/productivity-growth contribution. Central peak +0.0033 (≈+0.33pp/yr).
- B. EMPLOYMENT: `ai_employment_displacement_effect_t` = decimal annual pp contribution to unemployment-rate change (separate from Okun/productivity term). Central peak +0.00100 (≈+0.10pp).

## 3. No permanent growth floor
Architecture B (diffusion hump): rises, peaks ~2034-2035, decays toward ~0 by 2050. The temporary annual uplift permanently raises the productivity LEVEL, but the annual contribution is NOT held constant.

## 4. Level vs growth
Cumulative productivity LEVEL gain (≈ sum of annual contributions): 2030 ≈ +0.0053 (+0.53%); 2040 ≈ +0.0341 (+3.41%); 2050 ≈ +0.0393 (+3.93%). Annual effect fades to ~0; level gain persists.

## 5. Calibration evidence
Repository contains NO empirical French generative-AI productivity series. Classification: **MODEL_PRIOR / EXTERNAL_BENCHMARK_REQUIRED**. Need: external literature (IMF/OECD/GenAI productivity studies) to benchmark central peak amplitude. No data downloaded.

## 6. Uncertainty / amplitude contract
`ai_productivity_effect_t = central_profile_t * ai_productivity_amplitude` (path-level amplitude supplied by future orchestrator). Distribution: **AI_PRODUCTIVITY_AMPLITUDE_DISTRIBUTION_PENDING**. No RNG inside AI module.

## 7. Employment architecture
Temporary displacement HUMP (architecture B): rises with adoption, peaks mid-adoption, fades to ~0 by 2050. No occupation/skill/sector models. No permanent technological unemployment.

## 8. Macro-regime interaction
`AI_REGIME_DIRECT_EFFECT = DEFERRED`. AI does not alter regime transition probabilities.

## 9. GFC interaction
`AI_GFC_MODIFIER_CALIBRATION = DEFERRED`, default contribution 0. A future AI bubble MAY modify p_gfc or GFC severity, but NO separate AI crisis engine is created.

## 10. Investment / Median living
No AI-investment equation; productivity effect = net realized after adoption. Median living standard NOT modified directly; affected later via productivity→GDP/wages and displacement→unemployment/income.

## 12. Central productivity diagnostics (decimal growth contribution)
2027=0.0005, 2030=0.0022, 2035=0.0033, 2040=0.0020, 2050=0.00002.

## 13. Employment diagnostics (decimal pp)
2027=0.00005, 2030=0.00035, 2035=0.00100, 2040=0.00032, 2050=0.000001; peak ≈ +0.10pp ~2034-2035, returns toward 0.

## 14. Diagnostic cases
- CASE A (no AI): P=0, E=0.
- CASE B (central): peak P≈0.0033, E≈0.00100.
- CASE C (weaker): peak P≈0.00149, E≈0.00050.
- CASE D (stronger): peak P≈0.00561, E≈0.00180.
All: no GFC effect, no regime effect.

## 15. Optimism/pessimism safeguards
Non-AI baseline: labor_force_growth (small) + 0.00825 trend + (-0.001) climate ≈ 0.00725 (0.725%/yr). With AI: early/peak ≈ +0.33pp → ~1.06%/yr (not excessive); late (2050) AI→0 → returns to ~0.73%/yr. Employment displacement max +0.10pp then fades; distinguishes job destruction from net unemployment (reallocation offsets over time). No permanent mass unemployment assumed.

## 17. Selected architecture
Architecture B: simple diffusion productivity hump + temporary displacement hump. Rejected A (less realistic diffusion shape).

## 18. Future implementation contract
New module `src/francescope/ai/ai_effects.py` with `ai_productivity_effect(year, amplitude=1.0)` and `ai_employment_displacement_effect(year, amplitude=1.0)`. Constants: `AI_PRODUCTIVITY_CALIBRATION_STATUS`, `AI_EMPLOYMENT_CALIBRATION_STATUS = MODEL_PRIOR/EXTERNAL_BENCHMARK_REQUIRED`; `AI_PRODUCTIVITY_AMPLITUDE_DISTRIBUTION_PENDING`; `AI_REGIME_DIRECT_EFFECT=DEFERRED`; `AI_GFC_MODIFIER_CALIBRATION=DEFERRED`. No RNG. Future orchestrator provides path-level amplitudes.

## Artifacts
- docs/FRANCESCOPE_V3_AI_SPEC.md (this file)
- data/audits/economic_system/FRANCESCOPE_V3_AI_INPUT_CLASSIFICATION.csv
- data/audits/economic_system/FRANCESCOPE_V3_AI_MODEL_CANDIDATES.csv
- data/audits/economic_system/FRANCESCOPE_V3_AI_DIAGNOSTICS.csv
