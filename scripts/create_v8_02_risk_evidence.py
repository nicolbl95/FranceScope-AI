from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


RISKS = [
    (
        "French sovereign/debt crisis",
        "France spread blowout, rating shock or ECB/EU support without default",
        [(0.03, 0.08, 0.15, 0.35), (0.01, 0.04, 0.10, 0.25)],
        "Tier 1",
        "D",
        "medium",
    ),
    (
        "severe funding/refinancing crisis",
        "Inability to refinance normally, requiring exceptional official or market stabilization",
        [(0.01, 0.03, 0.07, 0.18), (0.005, 0.02, 0.05, 0.12)],
        "Tier 2",
        "D",
        "low",
    ),
    (
        "formal default/restructuring",
        "Missed payment or coercive restructuring of French sovereign obligations",
        [(0.001, 0.003, 0.01, 0.04), (0.0005, 0.002, 0.008, 0.03)],
        "Tier 3",
        "D",
        "low",
    ),
    (
        "banking/financial crisis",
        "Systemic bank or financial-intermediary distress with material credit contraction",
        [(0.04, 0.10, 0.19, 0.40), (0.02, 0.06, 0.14, 0.30)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "euro-area sovereign crisis",
        "Multi-country sovereign stress causing French funding or demand spillovers",
        [(0.04, 0.12, 0.23, 0.45), (0.02, 0.08, 0.18, 0.36)],
        "Tier 1",
        "C",
        "medium",
    ),
    (
        "global recession",
        "Global recession under a broad macro definition, not an ordinary slowdown",
        [(0.12, 0.25, 0.45, 0.80), (0.08, 0.20, 0.38, 0.70)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "asset-price crash",
        "Equity or property repricing large enough to impair demand or financial balance sheets",
        [(0.08, 0.20, 0.38, 0.70), (0.04, 0.12, 0.28, 0.58)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "credit crisis",
        "Abrupt tightening or rationing of credit outside a full banking crisis",
        [(0.06, 0.16, 0.30, 0.60), (0.03, 0.10, 0.23, 0.48)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "energy shock",
        "Large European energy supply or price shock affecting France",
        [(0.10, 0.25, 0.45, 0.75), (0.05, 0.18, 0.35, 0.65)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "oil/gas shock",
        "Oil or gas disruption producing a material French price and supply shock",
        [(0.08, 0.20, 0.38, 0.70), (0.04, 0.14, 0.30, 0.60)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "major geopolitical conflict",
        "Conflict escalation, sanctions or security shock materially affecting France",
        [(0.08, 0.20, 0.38, 0.70), (0.04, 0.15, 0.32, 0.62)],
        "Tier 1",
        "C",
        "low",
    ),
    (
        "trade fragmentation shock",
        "Abrupt protectionism or supply-chain fragmentation reducing external demand",
        [(0.10, 0.25, 0.48, 0.78), (0.05, 0.18, 0.38, 0.68)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "major climate/food-price shock",
        "Acute climate or agricultural event causing material food/output shock",
        [(0.08, 0.22, 0.45, 0.80), (0.03, 0.14, 0.32, 0.68)],
        "Tier 1",
        "B",
        "medium",
    ),
    (
        "domestic political crisis",
        "Government/parliamentary crisis that materially disrupts policy or confidence",
        [(0.15, 0.35, 0.60, 0.90), (0.06, 0.20, 0.42, 0.75)],
        "Tier 1",
        "C",
        "medium",
    ),
    (
        "housing/real-estate shock",
        "Large residential or commercial property correction with macro credit effects",
        [(0.07, 0.18, 0.35, 0.65), (0.03, 0.12, 0.26, 0.52)],
        "Tier 2",
        "B",
        "medium",
    ),
    (
        "combinations of the above",
        "Two or more qualifying shocks interact within a recovery period",
        [(0.08, 0.22, 0.48, 0.85), (0.03, 0.14, 0.34, 0.72)],
        "Tier 1",
        "D",
        "low",
    ),
]


def probability_table() -> pd.DataFrame:
    rows = []
    horizons = ["2y", "5y", "10y", "25y"]
    for risk, definition, ranges, tier, grade, confidence in RISKS:
        for idx, horizon in enumerate(horizons):
            low, high = ranges[0][idx], ranges[1][idx]
            central = round((low + high) / 2, 3)
            rows.append(
                {
                    "risk": risk,
                    "definition": definition,
                    "horizon": horizon,
                    "probability_type": "cumulative at least one qualifying event",
                    "probability_low": low,
                    "central_estimate": central,
                    "probability_high": high,
                    "estimate_basis": "D expert synthesis anchored to official evidence; not an official probability",
                    "tier": tier,
                    "evidence_grade": grade,
                    "confidence": confidence,
                    "main_sources": "V8_risk_sources.csv",
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    probability_table().to_csv(OUT / "V8_crisis_probability_estimates.csv", index=False)
    definitions = []
    for risk, definition, _, _tier, _, _ in RISKS:
        event_type = (
            "sovereign"
            if "sovereign" in risk or "funding" in risk or "default" in risk
            else "event/crisis"
        )
        definitions.append(
            {
                "risk": risk,
                "event_type": event_type,
                "qualifying_definition": definition,
                "observable_criteria": "Material effect on French output, unemployment, credit, sovereign financing, prices or real household income; ordinary volatility excluded.",
                "primary_transmission": "Unemployment via labor demand; GDP per capita via output/productivity; median living via real income, prices and transfers.",
                "formal_default_distinguished": "yes" if "default" in risk else "not applicable",
            }
        )
    pd.DataFrame(definitions).to_csv(OUT / "V8_risk_definitions.csv", index=False)
    timing = []
    for risk, _, _, _tier, _, _ in RISKS:
        timing += [
            {
                "risk": risk,
                "conditional_timing_band": "EARLY 2026-2030",
                "conditional_share": 0.40,
                "basis": "judgment",
            },
            {
                "risk": risk,
                "conditional_timing_band": "MID 2031-2040",
                "conditional_share": 0.35,
                "basis": "judgment",
            },
            {
                "risk": risk,
                "conditional_timing_band": "LATE 2041-2050",
                "conditional_share": 0.25,
                "basis": "judgment",
            },
        ]
    pd.DataFrame(timing).to_csv(OUT / "V8_timing_estimates.csv", index=False)
    severity = []
    for risk, _, _, _, _, _ in RISKS:
        severity.append(
            {
                "risk": risk,
                "unemployment_severity": "medium-high",
                "gdp_per_capita_severity": "medium-high",
                "median_living_severity": "medium",
                "typical_duration": "1-3 years",
                "recovery": "partial recovery over 2-7 years",
                "scarring": "PARTLY PERSISTENT",
                "scarring_channels": "hysteresis; foregone investment; debt accumulation; productivity loss; business failures",
                "confidence": "medium-low",
            }
        )
    pd.DataFrame(severity).to_csv(OUT / "V8_severity_scarring.csv", index=False)
    names = [x[0] for x in RISKS]
    matrix = []
    for a in names:
        for b in names:
            if a >= b:
                continue
            score = (
                "++"
                if {"energy shock", "oil/gas shock"} <= {a, b}
                or {"banking/financial crisis", "credit crisis"} <= {a, b}
                else "+"
                if a != b
                else "0"
            )
            if {"formal default/restructuring", b} <= {a, b} or {
                "French sovereign/debt crisis",
                b,
            } <= {a, b}:
                score = "++"
            matrix.append(
                {
                    "risk_a": a,
                    "risk_b": b,
                    "interaction": score,
                    "mechanism": "Common financing, demand, supply, confidence or policy channels.",
                }
            )
    pd.DataFrame(matrix).to_csv(OUT / "V8_compound_risk_matrix.csv", index=False)
    structural = [
        ("ageing/demography", "up", "down", "down", "HIGH", "HIGH"),
        ("fiscal deficits", "up", "down", "down", "HIGH", "HIGH"),
        ("debt/interest feedback", "up", "down", "down", "HIGH", "MEDIUM"),
        ("taxation/spending constraints", "up", "down", "down", "MEDIUM", "MEDIUM"),
        ("under-investment", "up", "down", "down", "HIGH", "MEDIUM"),
        ("capital weakness", "up", "down", "down", "HIGH", "MEDIUM"),
        ("productivity", "up", "down", "down", "VERY HIGH", "HIGH"),
        ("competitiveness", "up", "down", "down", "MEDIUM", "MEDIUM"),
        ("deindustrialisation", "up", "down", "down", "HIGH", "MEDIUM"),
        ("education/human capital", "up", "down", "down", "HIGH", "MEDIUM"),
        ("infrastructure", "up", "down", "down", "MEDIUM", "MEDIUM"),
        ("welfare/health burden", "up", "down", "down", "MEDIUM", "MEDIUM"),
        ("migration", "mixed", "mixed", "mixed", "MEDIUM", "LOW"),
        ("political/institutional constraints", "up", "down", "down", "HIGH", "MEDIUM"),
        ("structural inflation/energy", "up", "down", "down", "MEDIUM", "MEDIUM"),
        ("chronic climate damage", "up", "down", "down", "HIGH", "MEDIUM"),
        ("AI/automation", "mixed", "mixed", "mixed", "MEDIUM", "LOW"),
        ("technology outside AI", "down", "up", "up", "MEDIUM", "LOW"),
    ]
    pd.DataFrame(
        structural,
        columns=[
            "risk",
            "unemployment_direction",
            "gdp_per_capita_direction",
            "median_living_direction",
            "severity_by_2050",
            "confidence",
        ],
    ).to_csv(OUT / "V8_structural_risk_assessment.csv", index=False)
    scenario = []
    for risk, _, _, _, _, _ in RISKS:
        scenario += [
            {
                "risk": risk,
                "scenario": "OPTIMISTIC",
                "event_logic": "late, mild or contained; high-probability events remain possible",
            },
            {
                "risk": risk,
                "scenario": "CENTRAL",
                "event_logic": "most probable timing and moderate severity with partial recovery",
            },
            {
                "risk": risk,
                "scenario": "PESSIMISTIC",
                "event_logic": "early, severe, persistent or compounded realization",
            },
        ]
    pd.DataFrame(scenario).to_csv(OUT / "V8_scenario_event_map_preliminary.csv", index=False)
    sources = [
        [
            "ACPR/EBA/ECB",
            "2025 stress tests",
            "2025",
            "banking/financial crisis",
            "A",
            "https://acpr.banque-france.fr/en/press-release/results-2025-stress-tests-led-eba-and-ecb",
        ],
        [
            "IMF",
            "France Financial System Stability Assessment",
            "2025-07",
            "banking/financial crisis",
            "A",
            "https://www.imf.org/en/publications/cr/issues/2025/07/11/france-financial-system-stability-assessment-568525",
        ],
        [
            "ECB",
            "Financial Stability Review",
            "2025-11",
            "banking/financial crisis; asset-price crash",
            "A",
            "https://www.ecb.europa.eu/press/financial-stability-publications/fsr/pdf/ecb.fsr202511~263b5810d4.en.pdf",
        ],
        [
            "IMF",
            "World Economic Outlook",
            "2025-10",
            "global recession; trade fragmentation",
            "A",
            "https://www.imf.org/en/publications/weo/issues/2025/10/14/world-economic-outlook-october-2025",
        ],
        [
            "World Bank",
            "Global Economic Prospects",
            "2025-06",
            "global recession",
            "A",
            "https://www.worldbank.org/en/news/press-release/2025/06/10/global-economic-prospects-june-2025-press-release",
        ],
        [
            "European Commission",
            "2024 Ageing Report France fiche",
            "2024-05",
            "ageing; fiscal; long-run structural risk",
            "A",
            "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf",
        ],
        [
            "European Commission",
            "Autumn 2025 France forecast",
            "2025-11",
            "fiscal; energy; trade; unemployment",
            "A",
            "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en",
        ],
        [
            "Banque de France",
            "Macroeconomic projections June 2026",
            "2026-06",
            "energy; unemployment; growth",
            "A",
            "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf",
        ],
        [
            "IPCC",
            "AR6 Synthesis Report",
            "2023-03",
            "chronic climate damage",
            "A",
            "https://www.ipcc.ch/report/ar6/syr/",
        ],
        [
            "IEA",
            "World Energy Outlook",
            "2025",
            "energy shock",
            "A",
            "https://www.iea.org/reports/world-energy-outlook-2025",
        ],
        [
            "EEA",
            "European climate risk assessment",
            "2024-03",
            "climate/food-price risk",
            "A",
            "https://www.eea.europa.eu/publications/european-climate-risk-assessment",
        ],
        [
            "OECD",
            "Economic Outlook Interim Report",
            "2025-09",
            "global recession; trade fragmentation",
            "A",
            "https://www.oecd.org/en/publications/oecd-economic-outlook-interim-report-september-2025_67b10c01-en/full-report.html",
        ],
    ]
    pd.DataFrame(
        sources,
        columns=[
            "institution",
            "document",
            "publication_date",
            "risk_relevance",
            "quality_grade",
            "source_url",
        ],
    ).to_csv(OUT / "V8_risk_sources.csv", index=False)
    methodology = """# FranceScope V8.02 Risk Evidence Methodology

This is a risk-evidence layer, not a target-forecast selection. V8 retains
exactly three eventual numerical targets: unemployment, real GDP per capita and
real median living standard. No V8.02 endpoint values are selected.

Probabilities are cumulative probabilities of at least one qualifying event
within each horizon. Official sources rarely publish France-specific event
probabilities, so the ranges are transparent D-grade synthesis judgments
anchored to A/B-grade official stress tests, macro outlooks, historical
frequencies and risk assessments. Confidence is reduced where evidence is
indirect. Ranges are not independent annual probabilities.

The optimistic event map is not crisis-free: high-probability events can occur
in every scenario, with differences in timing, severity, persistence, recovery
and interaction. Structural deterioration is present in all scenarios.

Formal default is distinct from fiscal deterioration, spread stress and
refinancing crisis. The evidence does **not** support the statement “France
will default within 25 years.” The defensible wording is: “France faces a
material long-run risk of sovereign funding stress, while formal default or
restructuring remains a low-probability tail event and is not established as
inevitable.”

The five most dangerous compound combinations are: sovereign stress × banking
stress; sovereign stress × recession; energy shock × inflation/rates; climate
shock × food prices; and geopolitical shock × energy. Scarring is generally
PARTLY PERSISTENT through unemployment hysteresis, foregone investment, debt,
productivity and business failures; formal-default scarring is potentially
HIGHLY PERSISTENT.
"""
    (OUT / "V8_02_methodology.md").write_text(methodology, encoding="utf-8")
    manifest = {
        "event_risks": 15,
        "probability_rows": len(RISKS) * 4,
        "structural_risks": len(structural),
        "official_source_rows": len(sources),
        "v8_target_forecasts_selected": False,
        "formal_default_certain": False,
    }
    (OUT / "V8_02_validation_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
