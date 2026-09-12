# FRANCESCOPE V3 MC100 DISTRIBUTION + ECONOMIC BEHAVIOR AUDIT

**Scope:** Audit of the existing corrected V3 100-path development Monte Carlo only.
No rerun, no code modification, no recalibration, no Index scoring, no 1,000-path run.
**Gate:** `MC100_DISTRIBUTION_AUDIT_PASS`

## 1. Core-output distribution verdict
- **GDPpc:** 2050 P10/P50/P90 = 37.6k / 42.9k / 47.0k EUR. Dispersion grows with horizon (P90/P10: 1.065 → 1.180 → 1.250). PLAUSIBLE.
- **Unemployment:** 2050 6.84 / 7.41 / 7.92 %. Compressed near ~7.5 % (V2 natural-rate recurrence). EXPECTED LIMITATION.
- **Median living:** 2050 25.7k / 26.7k / 27.5k EUR. Coherent with GDPpc. PLAUSIBLE.
- **Debt/GDP:** 2050 176 / 192 / 217 %. High but diagnostic, not a bug (see §5).

## 2. GDPpc behavior
2050 distribution is the sum of: labor-force/demographic drag, ~1.0 % productivity trend, small AI (~0.18 %), small climate drag (−0.0012), regime cycle, and GFC shocks. Variance diagnostics show **GFC_count is the dominant long-run driver** (corr −0.405 with GDPpc), climate −0.222, AI only +0.135. Long-run dispersion is driven by **persistent state/path effects (GFC + regime)**, not by accumulation of iid yearly external shocks. No implausible permanent iid divergence.

## 3. Unemployment behavior
Mean-reverts to the ~7.5 % anchor via Okun recurrence. Range 6.53–9.04 %. Responds to GFC/regime (GFC next-regime 80.9 % recession/crisis; HIGH path hit 9.78 % in 2030). Cross-path terminal compression is an **accepted limitation** (simple recurrence), not a blocker; adequate for current scope.

## 4. Median-living behavior
Frozen C1 reduced form `0.00009 + 0.288·GDP_growth − 0.0078·(unemp−0.075)`. Trajectories stay coherent with GDPpc (LOW path 28.4k / HIGH path 24.0k mirror GDPpc ordering). No structural issue exposed.

## 5. Debt / fiscal diagnosis (HIGH PRIORITY)
Mean r = 3.1 %, implied nominal growth g = 5.6 % → **r − g = −2.5 %** (mild debt-reducing snowball). Yet debt rises because **total deficit stays ~6.7 % of GDP every year**, of which interest ~4.8 % and primary ~1.9 %.
Representative median path (pid 92): debt 122→130→151→192 %; deficit 5.6→5.7→6.5→8.3 %; interest 3.31→3.60→4.59→6.53 %.
HIGH path (pid 42, 3 GFC): debt 127→153→209→283 %; interest 12.4 % by 2050.

**Counterfactual decomposition:** A = persistent ~6.7 % total deficits — **PRIMARY**; B = weak nominal growth — **NOT APPLICABLE** (g > r); C = interest feedback — **MAJOR SECONDARY**; D = fiscal reaction — **PRESENT BUT CAPPED**; E = stochastic GFC tail — **TAIL CONTRIBUTOR**.

## 6. Does fiscal reaction improve the stock-flow path?
**YES — the wiring is correct.** Traced in `v1_orchestrator.simulate_year` (lines 297–357):
`deficit_t = adj_primary + interest_exp_gdp_t − adj_revenue`,
where `adj_primary = baseline_primary − 0.60·adj` and `adj_revenue = baseline_revenue + 0.40·adj`. The adjustment **does** enter the deficit that feeds the debt recursion (not merely a GDP impulse). The positive `fiscal_adjustment ↔ deficit` correlation (0.847) is a **confound** (both driven by high debt → high stress → high interest), not evidence of failure.
The reaction is **capped at 0.80 pp GDP** and never closes the ~1.9 % primary gap, so debt still rises. This is a **design limitation, not a wiring bug**. → NOT classified `FISCAL_REACTION_STOCK_FLOW_LINK_REVIEW_REQUIRED`.

## 7. Sovereign-risk feedback
ACTIVE and STABLE. debt↔premium r=0.990, debt↔effcost r=0.983, premium↔effcost 0.998. High-debt paths bear higher cost (HIGH oat 9.25 % vs LOW 5.11 %) with no explosive loop. Feedback plausible.

## 8–11. Regime/GFC, external iid, AI, climate
- **Regime/GFC:** 89 triggers; regime shares within calibration; compounding reasonable, no collapse.
- **External iid:** modest contribution; GDPpc P90/P10=1.25 at 2050; acceptable.
- **AI:** LABELING CORRECTED. The "~0.18%" was the **mean of the `ai_productivity_effect` column across all 2400 MC100 path-years (0.178%)** = AVERAGE ANNUAL growth contribution, NOT a cumulative level gain (~4.0% by 2050, matching frozen calibration). `effect = profile × realized amplitude` reconciles exactly to the MC100 amplitude distribution. Implementation correct → **NO_ISSUE (labeling corrected)**; AI_SCALE_VALIDATED.
- **Climate:** drag = −0.001·amp, realized amp 1.1994 → drag −0.0012; **LOW, consistent with frozen calibration**.

## 12–15. Representative paths, coherence, limitations, blockers
Representative paths (low/median/high by 2050 debt) show coherent narratives (0 / 0 / 3 GFC; debt 159 / 192 / 283 %; GDPpc 52.6k / 42.8k / 29.4k). No cross-output incoherence (no high-GDPpc + terrible-median, no low-unemp + recessionary GDP, no debt explosion with low stress).

**Blockers table:** 5 rows — all ACCEPTED_LIMITATION / NO_ISSUE. **No blocker.** Prior AI REVIEW_REQUIRED reclassified to NO_ISSUE_LABELING_CORRECTED (0.18% = mean annual effect, not cumulative). AI_SCALE_VALIDATED.

## 16–17. Distribution width & gate
Width expands with horizon (GDPpc P90/P10 1.065→1.250; debt 1.059→1.237). Reasonable.
**GATE = MC100_DISTRIBUTION_AUDIT_PASS.**

## 19. Files created
- `docs/FRANCESCOPE_V3_MC100_DISTRIBUTION_AUDIT.md`
- `data/audits/economic_system/FRANCESCOPE_V3_MC100_ECONOMIC_BEHAVIOR_AUDIT.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_MC100_FISCAL_DEBT_AUDIT.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_MC100_REPRESENTATIVE_PATHS.csv`
- `data/audits/economic_system/FRANCESCOPE_V3_MC100_AUDIT_BLOCKERS.csv`

## 20. Recommended next task
**V3 INDEX SCORING METHOD EVALUATION / FREEZE** (not dashboard). After freeze: recalculate historical V3 Index 2010–2026, then proceed to official 1,000-path simulation / Index distribution. (Optional pre-official check: verify AI productivity coefficient scale.)

## Final verdict
V3 MC100 DISTRIBUTION AUDIT COMPLETE — MC100_DISTRIBUTION_AUDIT_PASS
