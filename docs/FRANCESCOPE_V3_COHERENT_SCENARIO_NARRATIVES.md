# FranceScope V3 — Coherent Scenario Economic Narratives

Date: 2026-08-24. Narrative + data extraction layer only. No simulation rerun, no trajectory change, no invented mechanisms.

Authoritative sources: `data/processed/scenarios/francescope_v3_coherent_p10_p50_p90_paths.parquet` (72 rows), `docs/FRANCESCOPE_V3_COHERENT_P10_P50_P90_PATHS.md`, `data/processed/index/francescope_v3_historical_index_2010_2026.csv`, `docs/FRANCESCOPE_V3_MC1000_OFFICIAL_REPORT.md`, `docs/FRANCESCOPE_V3_MC100_DISTRIBUTION_AUDIT.md`.

## Permanent Technical Labels (do not rename)

| Technical label | Plain-language subtitle | path_id |
|-----------------|-------------------------|---------|
| P10_COHERENT_LOWER | "Adverse external conditions and high climate drag on a high-debt path" | 856 |
| P50_COHERENT_CENTRAL | "Central trajectory: steady drift under a mostly benign but unexciting environment" | 524 |
| P90_COHERENT_UPPER | "Favorable external environment and low climate drag lift the upper path" | 367 |

Subtitles are derived from actual path behavior, not from the quantile name.

## Historical Setup — Common 2027 Starting Point

France enters 2027 from the 2026 bridge estimate (OFFICIAL HISTORICAL V3 INDEX 2010–: 2026 Index ≈ 140.95; GDPpc ≈ 0.03912 MEUR/person; unemployment ≈ 8.10%; median living standard ≈ 25,848.70 EUR; debt/GDP ≈ 123.3%). Demographic structure is aging with slow labor-force growth, capping potential output. All three scenarios share this identical start; they diverge only through stochastic drivers (external shocks, regime draws, AI/climate amplitudes).

## Modeling Convention: Exogenous vs Endogenous

**Exogenous / stochastic drivers** (drawn per path, not determined by other variables): macro-regime sequence, `external_cycle_shock`, `ai_productivity_amplitude`, `climate_amplitude`, GFC trigger.

**Endogenous consequences** (produced by the implemented architecture): real GDP growth, unemployment (Okun + AI displacement), median living (reduced form), debt/deficit/interest (stock-flow), sovereign premium / fiscal stress, and the FranceScope Index (frozen 3-component score). A variable is said to affect another ONLY where the implemented equations contain that link (e.g., climate drag → structural GDP; external shock → cyclical GDP; debt → sovereign premium → fiscal stress). No other causal claims are made.

---

## P10_COHERENT_LOWER — path_id 856

**Profile:** AI amplitude 1.497 · climate amplitude 1.794 · GFC 0 · mean external shock −0.146 · regimes SLOWDOWN 13 / EXPANSION 4 / CRISIS 3 / RECESSION 2 / RECOVERY 2.

**Milestones:** Index 118.02 (2030) → 130.52 (2040) → 142.52 (2050); GDPpc 0.0357 → 0.0370 → 0.0386; unemployment 9.04% → 8.18% → 7.50%; median 25,239.8 → 25,591.0 → 25,909.3 EUR; debt 142.9% → 172.8% → 212.3%.

**Narrative.** This is the lower Index trajectory. It opens with RECESSION (2028) and a CRISIS (2029–30) amplified by an adverse external shock (2029 external −1.10), driving the Index to its 2030 trough of 118.0. A 2031–33 RECOVERY/EXPANSION lifts it back to ~136, but 2034 brings another CRISIS and then **eight consecutive SLOWDOWN years (2036–2043)** with mostly negative external shocks, keeping the Index stalled in the 124–132 band. A late EXPANSION (2044, 2049–50) carries it to 142.5 by 2050. The Index still rises because unemployment falls (9.0%→7.5%) and real incomes edge up, not because conditions are good.

**Why lower despite HIGHER AI.** AI amplitude here is the HIGHEST of the three (1.497) and contributes a genuine positive productivity offset each year. But AI is a bounded, modest channel. It cannot overcome: (a) the most adverse average external environment (−0.146), (b) the LARGEST climate drag (amplitude 1.794 → structural GDP drag −0.0018/yr), and (c) the worst regime mix (13 slowdowns, 3 crises, 2 recessions). Higher AI is therefore a helpful tailwind on a path that is otherwise the most stressed — it is NOT portrayed as bad.

---

## P50_COHERENT_CENTRAL — path_id 524

**Profile:** AI amplitude 1.008 · climate amplitude 1.136 · GFC 0 · mean external shock −0.220 · regimes SLOWDOWN 15 / EXPANSION 7 / CRISIS 1 / RECOVERY 1.

**Milestones:** Index 142.76 → 155.39 → 166.63; GDPpc 0.0391 → 0.0409 → 0.0428; unemployment 7.85% → 7.50% → 7.32%; median 25,905.9 → 26,347.8 → 26,716.7 EUR; debt 131.5% → 157.9% → 191.8%.

**Narrative.** This path is central because, across the whole 24-year span, its annual Index rank sits near the median of the 1000-path distribution. It starts mixed (SLOWDOWN/EXPANSION), dips at a 2032 CRISIS and an extreme 2033 external shock (−3.19) to 135.6, then enjoys a sustained EXPANSION-dominated climb (2034–2041) to 157.7. From 2042 it settles into chronic SLOWDOWN but keeps drifting higher to 166.6 by 2050. Average external shock is slightly negative (−0.220), yet the full-path regime balance (7 expansions vs 1 crisis) and moderate climate drag (1.136) more than compensate. Judgment is on the whole path, not one driver.

---

## P90_COHERENT_UPPER — path_id 367

**Profile:** AI amplitude 0.786 · climate amplitude 0.828 · GFC 0 · mean external shock +0.450 · regimes SLOWDOWN 15 / EXPANSION 6 / CRISIS 1 / RECESSION 1 / RECOVERY 1.

**Milestones:** Index 151.39 → 177.28 → 190.34; GDPpc 0.0403 → 0.0446 → 0.0471; unemployment 7.48% → 7.11% → 7.17%; median 26,140.7 → 27,029.0 → 27,486.5 EUR; debt 127.8% → 146.4% → 175.8%.

**Narrative.** This is the upper Index trajectory. It climbs favorably through 2035 (Index 170.3), suffers a single 2036 CRISIS dip (160.2), recovers, and ascends to a 2041 peak of 182.9 on a strongly positive external shock (+1.97). A 2042 RECESSION briefly pulls it to 176.3, after which it holds a high plateau (190.3 by 2050). It outperforms **despite the LOWEST AI amplitude (0.786)** because it benefits from the most favorable external environment (+0.450 average), the lowest climate drag (0.828), and a benign regime history (6 expansions, only 1 crisis). No "high AI = good scenario" story is imposed.

---

## Turning Points (derived from annual path data)

| Scenario | Phase | Period | What changed (driver) | Index consequence |
|----------|-------|--------|-----------------------|-------------------|
| P10 | A | 2027–2030 | RECESSION+CRISIS; adverse external shocks (2029 −1.10) | Trough 118.0 (2030) |
| P10 | B | 2031–2033 | RECOVERY→EXPANSION; positive shocks | Rebound to 136.1 |
| P10 | C | 2034–2040 | CRISIS(2034)+8 SLOWDOWN(2036–43); negative shocks | Stall 124–132; debt 173% |
| P10 | D | 2041–2043 | Brief EXPANSION; favorable shocks | 136.7 |
| P10 | E | 2044–2050 | Late EXPANSION; large climate drag | 142.5; debt 212% |
| P50 | A | 2027–2031 | SLOWDOWN/EXPANSION mix | 145.6 |
| P50 | B | 2032–2033 | CRISIS + extreme external −3.19 | Dip 135.6 |
| P50 | C | 2034–2041 | Sustained EXPANSION | Climb to 157.7 |
| P50 | D | 2042–2050 | Chronic SLOWDOWN, steady drift | 166.6; debt 192% |
| P90 | A | 2027–2035 | EXPANSION episodes; positive shocks | 170.3 |
| P90 | B | 2036 | One-year CRISIS | Dip 160.2 |
| P90 | C | 2037–2041 | RECOVERY+EXPANSION; +1.97 (2041) | Peak 182.9 |
| P90 | D | 2042–2043 | RECESSION; adverse shock | Dip 176.3 |
| P90 | E | 2044–2050 | Chronic SLOWDOWN, high level | 190.3; debt 176% |

(Exact anchors in `francescope_v3_coherent_scenario_turning_points.csv`.)

---

## Debt / Fiscal Interpretation

Debt is economically important but **NOT an Index component**. For each path it rises across the horizon as deficits and interest burdens accumulate, yet the Index also rises — because the Index measures GDPpc, median living, and (inversely) unemployment, not fiscal sustainability.

- **P10 (856):** debt 142.9%→212.3% (2050). Deficits 5.9%→9.4%, interest burden 3.8%→7.7%. Sovereign premium (OAT 0.038→0.068) and fiscal stress (0.46→1.00) rise endogenously with debt. Highest debt of the three.
- **P50 (524):** debt 131.5%→191.8%. Deficits 5.7%→8.4%, interest 3.6%→6.6%. Fiscal stress 0.46→0.94.
- **P90 (367):** debt 127.8%→175.8% — the LOWEST, because stronger nominal growth contains the ratio. Deficits 5.6%→7.5%, interest 3.5%→5.8%.

The debt ordering is the inverse of the Index ordering: the worst Index path carries the highest debt. This is a coherent stochastic outcome, not a contradiction.

---

## Index Component Interpretation

Frozen V3 Index = arithmetic mean of three RAW component scores (base 100, 10 pts/SD, equal 1/3, no clipping): GDPpc (+1), median living (+1), unemployment (−1). Exact component scores are in the source parquet.

- **P10 2050:** GDPpc score 136.4, median score 158.5, unemployment score 132.7 → Index 142.5.
- **P50 2050:** 183.5 / 180.9 / 135.5 → 166.6.
- **P90 2050:** 230.9 / 202.2 / 137.9 → 190.3.

Unemployment improvement is the main contributor to P10's rise; P90's lead comes from the highest GDPpc and median scores. **GDPpc and median living become highly correlated in future paths** (both driven by the same real-income engine), so their scores move together; the Index effectively weights a near-duplicated real-income signal twice against unemployment. This correlation is a known feature of the simulation and is stated openly, not hidden.

---

## What Most Separates the Three Paths

Ranked by evidence (not assumed in advance):

1. **External environment** — mean external shock −0.146 / −0.220 / +0.450 is the single largest differentiator and directly moves cyclical GDP.
2. **Climate drag** — amplitude 1.794 / 1.136 / 0.828 scales a persistent structural-GDP subtraction.
3. **Regime history** — crisis count 3 / 1 / 1 and expansion count 4 / 7 / 6 shape the cyclical input year by year.
4. **Fiscal/debt feedback** — 2050 debt 212% / 192% / 176% (endogenous, not an Index input but a real-economy burden).
5. **AI amplitude** — 1.497 / 1.008 / 0.786 is the WEAKEST differentiator; it is a modest positive offset everywhere and does not rank the paths.

Stochastic interactions matter: the same AI amplitude would produce different outcomes under different external/regime draws. No driver is independently optimized.

---

## Limitations (accepted, not hidden defects)

- Climate disasters are OFF (acute shock disabled); only chronic drag is active.
- Credit→investment channel is DEFERRED.
- Unemployment is a mean-reverting reduced form (Okun + AI displacement).
- Median living is a simplified reduced form.
- Fiscal adjustment is capped (bounded reaction).
- Coherent paths are representative Index trajectories, NOT marginal P10/P50/P90 quantile envelopes for every variable.
- None of the three selected paths contains a GFC event, even though GFC exists in the MC1000 distribution (valid stochastic outcome, P(no GFC)≈0.48).
- GDPpc and median living are highly correlated in future paths.

---

## Explanatory-LLM Data Contract

Machine-readable summary: `data/processed/scenarios/francescope_v3_coherent_scenario_summary.json` (per-scenario fields: `scenario_label`, `path_id`, `target_quantile`, `subtitle`, `starting_context`, `milestones`, `major_drivers`, `turning_points`, `index_component_story`, `fiscal_debt_story`, `key_risks`, `limitations`, `narrative_summary`). Tabular companions: `francescope_v3_coherent_scenario_milestones.csv` (9 rows) and `francescope_v3_coherent_scenario_turning_points.csv` (14 rows).

All facts are extracted from existing artifacts; no fabricated events or synthetic forecasts.
