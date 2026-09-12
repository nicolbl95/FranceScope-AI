from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"
PROBABILITIES = OUT / "V8_crisis_probability_estimates_final.csv"


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    pd.DataFrame(rows).to_csv(OUT / name, index=False)


def main() -> None:
    probabilities = pd.read_csv(PROBABILITIES)
    event_names = sorted(probabilities.risk.unique())
    assert "combinations of the above" in event_names
    structural = [
        ("ageing/demographics", "MILDLY NEGATIVE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("structural fiscal deficit", "MILDLY NEGATIVE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("debt-interest pressure", "MILDLY NEGATIVE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("taxation/spending constraints", "FAVORABLE", "MILDLY NEGATIVE", "NEGATIVE"),
        ("under-investment", "FAVORABLE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("capital weakness", "MILDLY NEGATIVE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("productivity", "FAVORABLE", "MILDLY NEGATIVE", "NEGATIVE"),
        ("competitiveness", "FAVORABLE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("deindustrialisation", "MILDLY NEGATIVE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("education/human capital", "FAVORABLE", "MILDLY NEGATIVE", "NEGATIVE"),
        ("infrastructure", "FAVORABLE", "MILDLY NEGATIVE", "NEGATIVE"),
        ("welfare/health burden", "MILDLY NEGATIVE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("migration", "FAVORABLE", "MILDLY NEGATIVE", "NEGATIVE"),
        ("chronic energy costs", "FAVORABLE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("chronic climate damage", "MILDLY NEGATIVE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("political reform constraints", "FAVORABLE", "NEGATIVE", "STRONGLY NEGATIVE"),
        ("AI", "FAVORABLE", "MILDLY NEGATIVE", "NEGATIVE"),
        ("non-AI technological progress", "FAVORABLE", "MILDLY NEGATIVE", "NEGATIVE"),
    ]
    write_csv(
        "V8_scenario_structural_assumptions.csv",
        [
            {"risk_or_force": name, "optimistic": opt, "central": cen, "pessimistic": pes, "common_core": "Structural pressure remains in every scenario."}
            for name, opt, cen, pes in structural
        ],
    )
    clusters = [
        ("GLOBAL_MACRO_RECESSION", "global recession", "One or more global recession realizations; not ordinary slowdown.", "2-3 years", "medium to high", "partial to meaningful", "FINANCIAL_CREDIT; TRADE"),
        ("FRENCH_SOVEREIGN_FISCAL_STRESS", "French sovereign/debt crisis; severe funding/refinancing crisis; formal default/restructuring", "Separate spread/funding/default layers; default is tail only.", "1-5 years", "medium to very high", "high if disorderly", "FINANCIAL_CREDIT; POLITICAL"),
        ("FINANCIAL_CREDIT_CRISIS", "banking/financial crisis; asset-price crash; credit crisis", "Correlated channels, not three independent shocks.", "1-4 years", "medium to high", "medium to high", "SOVEREIGN; HOUSING"),
        ("ENERGY_GEOPOLITICAL_SHOCK", "major geopolitical conflict; energy shock; oil/gas shock", "One causal geopolitical-to-energy episode may contain several channels.", "1-3 years", "medium to high", "medium", "TRADE; CLIMATE_FOOD"),
        ("CLIMATE_FOOD_SHOCK", "major climate/food-price shock", "Acute event layered onto chronic climate deterioration.", "1-4 years", "medium to high", "medium to high", "ENERGY_GEOPOLITICAL"),
        ("DOMESTIC_POLITICAL_INSTITUTIONAL", "domestic political crisis", "Broad political instability is not automatically macro catastrophe.", "1-5 years", "low to high", "medium", "SOVEREIGN; GLOBAL"),
        ("TRADE_DEGLOBALISATION", "trade fragmentation shock", "Protectionism, sanctions, and supply-chain disruption.", "2-5 years", "medium", "medium", "GLOBAL; GEOPOLITICAL"),
        ("HOUSING_PROPERTY_STRESS", "housing/real-estate shock", "Property correction with macro-relevant credit transmission.", "1-4 years", "low to high", "medium", "FINANCIAL_CREDIT"),
    ]
    write_csv("V8_event_clusters.csv", [
        {"cluster": c, "constituent_risks": r, "evidence_note": e, "typical_duration": d, "severity_range": s, "scarring_range": sc, "interaction_partners": i}
        for c, r, e, d, s, sc, i in clusters
    ])
    timing = []
    timing_logic = {
        "OPTIMISTIC": {
            "2026-2030": "Structural pressure continues; one high-probability mild event may occur, but contained.",
            "2031-2040": "Later mild recession or correction with relatively effective adaptation and recovery.",
            "2041-2050": "Late shocks remain possible; accumulated scarring is limited by recovery quality.",
        },
        "CENTRAL": {
            "2026-2030": "Cooling and fiscal pressure; material recession, political disruption, or financial tightening is plausible.",
            "2031-2040": "At least one significant clustered episode is plausible; partial recovery leaves persistent damage.",
            "2041-2050": "Further event realization remains possible as ageing and debt amplify vulnerability.",
        },
        "PESSIMISTIC": {
            "2026-2030": "Early severe recession, energy/geopolitical shock, or funding stress triggers reinforcing feedback.",
            "2031-2040": "Repeated or overlapping clusters interrupt recovery and deepen capital, credit, and labor scarring.",
            "2041-2050": "Late shocks compound already weak resilience; formal restructuring remains only an extreme branch.",
        },
    }
    for scenario, periods in timing_logic.items():
        for period, logic in periods.items():
            timing.append({"scenario": scenario, "period": period, "structural_backdrop_and_event_logic": logic, "formal_default_assumed": "NO"})
    write_csv("V8_scenario_event_timing.csv", timing)
    recovery = [
        {"scenario": "OPTIMISTIC", "recovery_quality": "relatively fast", "cyclical_loss_recovered": "much", "hysteresis": "LOW", "investment_repair": "partial to strong", "policy_response": "relatively effective", "repeated_shocks": "limited"},
        {"scenario": "CENTRAL", "recovery_quality": "partial", "cyclical_loss_recovered": "some", "hysteresis": "MEDIUM", "investment_repair": "partial", "policy_response": "mixed and delayed", "repeated_shocks": "plausible"},
        {"scenario": "PESSIMISTIC", "recovery_quality": "slow/incomplete", "cyclical_loss_recovered": "little", "hysteresis": "HIGH", "investment_repair": "weak", "policy_response": "late or disorderly", "repeated_shocks": "frequent or clustered"},
    ]
    write_csv("V8_scenario_recovery_rules.csv", recovery)
    scarring = []
    for scenario, values in [
        ("OPTIMISTIC", ("LOW", "LOW", "LOW")),
        ("CENTRAL", ("MEDIUM", "MEDIUM", "MEDIUM")),
        ("PESSIMISTIC", ("HIGH", "HIGH", "HIGH")),
    ]:
        scarring.append({"scenario": scenario, "unemployment_scarring": values[0], "gdp_per_capita_scarring": values[1], "median_living_scarring": values[2], "channels": "hysteresis; lost capital; foregone investment; productivity; debt; prices; taxes; services"})
    write_csv("V8_scenario_scarring_ledger.csv", scarring)
    offsets = [
        ("AI productivity", "upper plausible range; broad diffusion", "partial diffusion", "weak diffusion; gains overwhelmed", "positive offsets exist in all scenarios"),
        ("automation", "reallocation with manageable displacement", "mixed transition", "displacement exceeds absorption", "not assumed zero in pessimistic case"),
        ("nuclear/energy improvements", "strong reliability and cost mitigation", "partial improvement", "delayed or disrupted", "energy cluster remains possible"),
        ("reform success", "gradual credible adjustment", "partial and delayed", "blocked then abrupt", "not treated as guaranteed"),
        ("education improvement", "meaningful skill adaptation", "incremental progress", "weak progress", "affects productivity and hysteresis"),
        ("productive green investment", "crowds in capacity", "partial delivery", "insufficient delivery", "scenario driver, not forecast endpoint"),
        ("technological breakthroughs", "several useful advances", "normal diffusion", "few or late gains", "uncertain positive tail"),
        ("EU support/integration", "effective risk sharing", "available but conditional", "limited or politically constrained", "can contain but not erase shocks"),
    ]
    write_csv("V8_scenario_positive_offsets.csv", [{"offset": a, "optimistic": b, "central": c, "pessimistic": d, "interpretation": e} for a,b,c,d,e in offsets])
    directions = []
    labels = {
        "OPTIMISTIC": [("MILD DETERIORATION", "MILD IMPROVEMENT", "MILD IMPROVEMENT"), ("STAGNATION", "MILD IMPROVEMENT", "MILD IMPROVEMENT"), ("STAGNATION", "MILD IMPROVEMENT", "STAGNATION")],
        "CENTRAL": [("MODERATE DETERIORATION", "STAGNATION", "STAGNATION"), ("MILD DETERIORATION", "STAGNATION", "MILD DETERIORATION"), ("MILD DETERIORATION", "MILD DETERIORATION", "MILD DETERIORATION")],
        "PESSIMISTIC": [("SEVERE DETERIORATION", "MODERATE DETERIORATION", "MODERATE DETERIORATION"), ("SEVERE DETERIORATION", "MODERATE DETERIORATION", "MODERATE DETERIORATION"), ("SEVERE DETERIORATION", "SEVERE DETERIORATION", "MODERATE DETERIORATION")],
    }
    for scenario, periods in labels.items():
        for period, directions_for_targets in zip(
            ["2026-2030", "2031-2040", "2041-2050"], periods, strict=True
        ):
            directions.append({"scenario": scenario, "period": period, "unemployment": directions_for_targets[0], "real_gdp_per_capita": directions_for_targets[1], "real_median_living_standard": directions_for_targets[2]})
    write_csv("V8_target_direction_matrix.csv", directions)
    methodology = """# FranceScope V8.03 Scenario Architecture

V8.03 approves scenario architecture only. It selects no unemployment,
real-GDP-per-capita, or median-living numerical forecasts. The only event
probability source is `V8_crisis_probability_estimates_final.csv`.

## Compound-risk rule

`combinations of the above` is a derived outcome, never an independently
sampled event. Correlated risks are grouped into eight clusters to prevent
double counting. A geopolitical event may transmit through oil and gas, but
those channels are not counted as three independent crises.

## Common structural core

All scenarios retain ageing, fiscal and debt pressure, under-investment,
productivity and competitiveness constraints, climate costs, and political
frictions. They differ in intensity and in the quality of positive offsets.
Optimistic means least bad, not crisis-free.

## Scenario narratives

### OPTIMISTIC / LEAST BAD

France remains under demographic and fiscal pressure, but gradual adjustment,
credible reforms, useful AI and non-AI technology, and partial investment
repair prevent a disorderly feedback loop. A global recession or correction
can still occur, preferably later and with fast recovery. Energy and climate
events are manageable through adaptation and EU integration. Unemployment may
rise during shocks but hysteresis is limited; GDP per capita and median living
standard recover most cyclical losses and retain mild long-run improvement.

### CENTRAL / MOST PLAUSIBLE

Existing structural weaknesses continue: ageing becomes more binding, fiscal
constraints intensify, investment remains insufficient, and productivity gains
are partial. A material recession, political disruption, or financial episode
is plausible in the early or middle band, with partial recovery. Sovereign
stress can appear without formal default, and energy, trade, climate and
political episodes can overlap. Employment and living standards bear
persistent but not catastrophic scarring; positive technology offsets remain
real but insufficient to reverse all structural pressure.

### PESSIMISTIC / ADVERSE COMPOUND

Structural problems reinforce one another. Fiscal correction is delayed and
then abrupt, an early severe recession or energy/geopolitical event interacts
with credit or sovereign stress, and repeated clusters interrupt recovery.
Capital, skills, businesses and confidence are damaged; reforms are blocked or
late. AI, energy, education and green investment still produce some gains, but
their effects are overwhelmed. Formal restructuring is an extreme branch, not
an automatic scenario ingredient.

## Recovery and scarring

Optimistic recovery is relatively fast with low hysteresis. Central recovery is
partial with medium scarring. Pessimistic recovery is slow and incomplete with
high hysteresis, lost capital, productivity damage, debt accumulation and
business failures.

## Plausibility and limits

The optimistic scenario is plausible because high-probability events can be
mild, late or contained. The central scenario is not a mechanical average: it
uses moderate structural deterioration and partial recovery. The pessimistic
scenario is adverse but plausible, not apocalyptic. Direction labels are
qualitative and do not imply selected endpoint values.
"""
    (OUT / "V8_scenario_architecture.md").write_text(methodology, encoding="utf-8")
    manifest = {
        "probability_source": PROBABILITIES.name,
        "independent_event_selection_excludes_compound_row": True,
        "event_clusters": 8,
        "scenarios": 3,
        "target_endpoints_selected": False,
        "target_direction_rows": len(directions),
        "formal_default_assumed_in_central": False,
        "v7_artifacts_modified": False,
    }
    (OUT / "V8_03_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
