from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


def main() -> None:
    baseline = {"unemployment_rate": 7.725, "real_gdp_per_capita": 38360.0, "real_median_living_standard": 25952.514017}
    current = {
        "OPTIMISTIC": {"unemployment_rate": [9.0, 10.5, 12.0], "real_gdp_per_capita": [39700, 39500, 36500], "real_median_living_standard": [26500, 26200, 25200]},
        "CENTRAL": {"unemployment_rate": [9.7, 12.0, 14.0], "real_gdp_per_capita": [38500, 36500, 34000], "real_median_living_standard": [25800, 25300, 23900]},
        "PESSIMISTIC": {"unemployment_rate": [11.3, 14.7, 17.8], "real_gdp_per_capita": [37000, 34000, 30000], "real_median_living_standard": [25000, 23500, 22000]},
    }
    episodes = [
        ["France", "early 1990s unemployment stress", 1990, 1997, "about 9-12%", "N/A", "N/A", "slow", "labor-market persistence", "High unemployment can persist without GDP collapse.", "Moderate"],
        ["France", "global financial crisis", 2008, 2010, "about 7-9%", "negative", "N/A", "partial", "demand shock", "Short-run joint downturn; median series not forced.", "High"],
        ["France", "COVID shock", 2019, 2021, "about 8%", "sharp 2020 fall", "median rose in canonical series", "rapid policy-supported", "shutdown and fiscal support", "Policy support weakens one-for-one mapping.", "Moderate"],
        ["France", "2022-2026 slowdown", 2022, 2026, "7.2-8.3%", "stagnation/slow growth", "recent median data", "ongoing", "inflation, energy and weak demand", "Current official anchor reaches 8.3% in Q2 2026.", "High"],
        ["Spain", "euro-area sovereign/banking crisis", 2008, 2013, ">26%", "large decline", "income damage", "multi-year", "housing, banking and sovereign stress", "Stress analogue, not a France forecast.", "Moderate"],
        ["Greece", "sovereign crisis", 2008, 2013, ">27%", "severe collapse", "large household damage", "long", "sovereign adjustment and depression", "Upper-bound severe analogue.", "Moderate"],
        ["Portugal", "euro-area adjustment", 2008, 2013, ">16%", "decline", "income pressure", "multi-year", "external adjustment and credit", "Intermediate stress analogue.", "Moderate"],
        ["Italy", "post-2008 stagnation", 2008, 2020, "about 12%", "weak/flat", "persistent weakness", "long", "productivity and fiscal constraints", "Long stagnation analogue.", "Moderate"],
        ["Japan", "demographic stagnation", 1995, 2020, "generally <5%", "low growth", "mixed", "long", "ageing with labor absorption", "Shows unemployment can stay low despite stagnation.", "Moderate"],
    ]
    pd.DataFrame(episodes, columns=["country", "episode", "start_year", "end_year", "peak_or_range_unemployment", "real_gdp_per_capita_impact", "median_income_impact", "recovery_duration", "mechanism", "comparability_to_france", "evidence_confidence"]).to_csv(OUT / "V8_joint_coherence_historical_episodes.csv", index=False)

    defensibility = [
        ["OPTIMISTIC", "2030", 9.0, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Above the 2026 Q2 anchor but compatible with gradual structural deterioration and contained events."],
        ["OPTIMISTIC", "2040", 10.5, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Persistent hysteresis is possible, but this requires weaker reform/offset performance than the prior optimistic architecture."],
        ["OPTIMISTIC", "2050", 12.0, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Historically intelligible as a structural regime, but conflicts with the least-bad low-scarring interpretation and is not inside the approved range."],
        ["CENTRAL", "2030", 9.7, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Material early deterioration is consistent with the central crisis timing."],
        ["CENTRAL", "2040", 12.0, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Persistent unemployment can follow repeated shocks and medium hysteresis."],
        ["CENTRAL", "2050", 14.0, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Plausible only with sustained structural mismatch and repeated scarring; stronger than current frozen central path."],
        ["PESSIMISTIC", "2030", 11.3, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Substantial early damage is compatible with the pessimistic compound-shock architecture."],
        ["PESSIMISTIC", "2040", 14.7, "DEFENSIBLE_BUT_STRONG_ASSUMPTION", "Severe but historically intelligible under repeated crisis and high hysteresis."],
        ["PESSIMISTIC", "2050", 17.8, "TOO_HIGH", "Exceeds the approved V8.04 upper bound of 17.5%; would require explicit range revision before adoption."],
    ]
    pd.DataFrame(defensibility, columns=["scenario", "year", "candidate_unemployment", "classification", "justification"]).to_csv(OUT / "V8_unemployment_defensibility.csv", index=False)
    gdppc = [
        ["OPTIMISTIC", "COHERENT", "GDP per capita can improve through 2040 while unemployment rises through labor-force participation, productivity and sectoral composition; 2050 decline reflects scarring."],
        ["CENTRAL", "COHERENT", "The 2040 and 2050 declines are consistent with earlier unemployment deterioration and medium structural scarring."],
        ["PESSIMISTIC", "COHERENT", "A 21.8% 2025-2050 real decline is severe but remains below collapse-scale analogues; it is compatible with high unemployment if shocks cluster."],
    ]
    pd.DataFrame(gdppc, columns=["scenario", "classification", "justification"]).to_csv(OUT / "V8_gdppc_defensibility.csv", index=False)
    median = [
        ["OPTIMISTIC", "TOO_HIGH", "With 12% unemployment by 2050, EUR25,200 is strongly protected and requires unusually effective transfers, wage protection and distributional insulation."],
        ["CENTRAL", "COHERENT", "EUR23,900 reflects medium scarring while allowing transfers and household smoothing to limit the GDP-per-capita decline."],
        ["PESSIMISTIC", "COHERENT", "EUR22,000 reflects substantial unemployment, inflation, fiscal adjustment and housing/energy burden without one-for-one GDP transmission."],
    ]
    pd.DataFrame(median, columns=["scenario", "classification", "justification"]).to_csv(OUT / "V8_median_living_defensibility.csv", index=False)

    matrix = []
    for scenario, values in current.items():
        for idx, year in enumerate([2030, 2040, 2050]):
            u, g, m = values["unemployment_rate"][idx], values["real_gdp_per_capita"][idx], values["real_median_living_standard"][idx]
            score = "ACCEPTABLE"
            caveat = "Candidate unemployment is not the frozen V8.05 path."
            if scenario == "OPTIMISTIC" and year == 2050:
                score, caveat = "WEAK", "Higher unemployment and protected median living strain the least-bad low-scarring narrative."
            if scenario == "PESSIMISTIC" and year == 2050:
                score, caveat = "INCONSISTENT", "17.8% exceeds approved unemployment range; adoption requires range review."
            matrix.append([scenario, year, u, g, m, "Spain/Greece upper stress; Italy stagnation; France policy-supported episodes", score, "Candidate path can be explained by the stated crisis/scarring mechanisms.", caveat])
    pd.DataFrame(matrix, columns=["scenario", "year", "unemployment", "gdp_per_capita", "median_living", "historical_analogue_range", "internal_coherence_score", "primary_justification", "main_caveat"]).to_csv(OUT / "V8_joint_coherence_matrix.csv", index=False)

    review = """# FranceScope V8.06 Joint-Coherence Review

## Scope and evidence

The candidate unemployment paths were tested against the canonical V8 framework,
official INSEE/Eurostat anchors, French historical episodes, and international
stress analogues. INSEE reports 8.1% unemployment in Q1 2026 and 8.3% in Q2
2026, France excluding Mayotte, under the BIT/ILO definition. OECD and IMF
research support hysteresis and structural persistence after shocks.

## Finding

The candidate paths are economically intelligible as strong assumptions, but
they are not all admissible under the frozen V8.04 range layer. Pessimistic
2050 unemployment of 17.8% exceeds the approved upper bound of 17.5%. The
optimistic 2050 unemployment path is also stronger than the least-bad narrative,
and its median-living outcome is highly protected relative to 12% unemployment.

The frozen GDP-per-capita paths remain jointly coherent with the candidate
unemployment paths at a qualitative level. The central and pessimistic median
paths remain coherent; the optimistic median path is weakly coherent because
of its protection under higher unemployment.

No forecast artifact was modified because the candidate unemployment path
requires an explicit human decision about whether to revise the approved
V8.04 ranges and scenario architecture. This is not evidence that the frozen
GDP-per-capita path is invalid.

## Counterargument

AI/productivity gains, labor shortages from ageing, immigration, successful
labor-market reform, EU support, nuclear resilience and social insurance could
keep unemployment materially below the candidate paths. Conversely, repeated
crises and hysteresis could make the central path closer to the candidates.
The evidence supports plausibility judgments, not a unique correction.
"""
    (OUT / "V8_joint_coherence_analysis.md").write_text(review, encoding="utf-8")
    manifest = {
        "official_anchor": {"2025_annual": 7.725, "2026_q1": 8.1, "2026_q2": 8.3, "definition": "BIT/ILO, France excluding Mayotte"},
        "candidate_paths_reviewed": 9,
        "gdp_per_capita_revision_required": False,
        "median_living_revision_required": False,
        "candidate_pessimistic_2050_inside_approved_range": False,
        "approved_forecast_artifacts_modified": False,
        "index_calculated": False,
    }
    (OUT / "V8_06_joint_coherence_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
