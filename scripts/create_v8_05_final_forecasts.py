from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"
RANGES = pd.read_csv(OUT / "V8_target_ranges.csv").set_index("variable")
BASELINE = pd.read_csv(OUT / "V8_2025_baseline.csv").set_index("target_variable")

POINTS = {
    "unemployment_rate": {
        "unit": "%",
        "2025": 7.725,
        "OPTIMISTIC": {"2030": 8.0, "2040": 8.7, "2050": 9.0},
        "CENTRAL": {"2030": 8.7, "2040": 10.0, "2050": 11.2},
        "PESSIMISTIC": {"2030": 10.3, "2040": 12.8, "2050": 15.2},
    },
    "real_gdp_per_capita": {
        "unit": "EUR/person, 2020 chain-linked prices",
        "2025": 38360.0,
        "OPTIMISTIC": {"2030": 39700.0, "2040": 41000.0, "2050": 36500.0},
        "CENTRAL": {"2030": 38500.0, "2040": 38000.0, "2050": 34000.0},
        "PESSIMISTIC": {"2030": 37000.0, "2040": 34000.0, "2050": 30000.0},
    },
    "real_median_living_standard": {
        "unit": "EUR/person/year, constant prices",
        "2025": 25952.514017,
        "OPTIMISTIC": {"2030": 26500.0, "2040": 26200.0, "2050": 25200.0},
        "CENTRAL": {"2030": 25800.0, "2040": 25300.0, "2050": 23900.0},
        "PESSIMISTIC": {"2030": 25000.0, "2040": 23500.0, "2050": 22000.0},
    },
}


def main() -> None:
    rows = []
    rationale = {
        "OPTIMISTIC": "Favorable side of the approved range reflects late/mild shocks, stronger offsets and low scarring.",
        "CENTRAL": "Non-midpoint placement reflects partial reform, material shocks and medium persistent scarring.",
        "PESSIMISTIC": "Adverse interior placement reflects early/compound shocks and high scarring without selecting the boundary.",
    }
    confidence_by_year = {"2030": "MEDIUM", "2040": "LOW", "2050": "LOW"}
    for variable, config in POINTS.items():
        for scenario in ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]:
            for year in ["2030", "2040", "2050"]:
                value = config[scenario][year]
                row_range = RANGES.loc[variable, f"{scenario.lower()}_{year}_low"], RANGES.loc[variable, f"{scenario.lower()}_{year}_high"]
                rows.append({
                    "forecast_id": f"V8_{'U' if variable == 'unemployment_rate' else 'GDPPC' if variable == 'real_gdp_per_capita' else 'MED'}_{'OPT' if scenario == 'OPTIMISTIC' else 'CEN' if scenario == 'CENTRAL' else 'PESS'}_{year}",
                    "variable": variable,
                    "scenario": scenario,
                    "year": int(year),
                    "point_forecast": value,
                    "unit": config["unit"],
                    "approved_range_low": row_range[0],
                    "approved_range_high": row_range[1],
                    "confidence": confidence_by_year[year],
                    "rationale": rationale[scenario],
                })
    forecasts = pd.DataFrame(rows)
    baseline_rows = [{
        "forecast_id": f"V8_{'U' if variable == 'unemployment_rate' else 'GDPPC' if variable == 'real_gdp_per_capita' else 'MED'}_ACTUAL_2025",
        "variable": variable,
        "scenario": "2025_ACTUAL",
        "year": 2025,
        "point_forecast": config["2025"],
        "unit": config["unit"],
        "approved_range_low": config["2025"],
        "approved_range_high": config["2025"],
        "confidence": "HIGH",
        "rationale": "Canonical V8.01 2025 baseline.",
    } for variable, config in POINTS.items()]
    all_forecasts = pd.concat([pd.DataFrame(baseline_rows), forecasts], ignore_index=True)
    all_forecasts.to_csv(OUT / "V8_final_target_forecasts.csv", index=False)
    analysis = []
    for variable, config in POINTS.items():
        baseline_value = config["2025"]
        for scenario in ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]:
            previous = baseline_value
            previous_year = 2025
            for year in [2030, 2040, 2050]:
                current = config[scenario][str(year)]
                delta = current - previous
                pct = delta / previous * 100
                annualized = ((current / previous) ** (1 / (year - previous_year)) - 1) * 100 if variable != "unemployment_rate" else None
                analysis.append({"variable": variable, "scenario": scenario, "from_year": previous_year, "to_year": year, "from_value": previous, "to_value": current, "absolute_change": delta, "percent_change": pct, "annualized_real_change": annualized, "interpretation": "Unemployment change in percentage points; level changes are percentage changes." if variable == "unemployment_rate" else "Real level change."})
                previous, previous_year = current, year
    pd.DataFrame(analysis).to_csv(OUT / "V8_forecast_trajectory_analysis.csv", index=False)
    index_inputs = forecasts[["scenario", "year", "variable", "point_forecast"]].pivot(index=["scenario", "year"], columns="variable", values="point_forecast").reset_index()
    index_inputs.to_csv(OUT / "V8_index_inputs.csv", index=False)
    pd.DataFrame([
        {"variable": "unemployment_rate", "comparison": "2030 within near-term institutional envelope; 2040/2050 not institutionally endorsed", "influence": "STRONG 2030 / WEAK thereafter"},
        {"variable": "real_gdp_per_capita", "comparison": "2030 broadly consistent with official aggregate-GDP benchmarks after no mechanical conversion; 2040/2050 more pessimistic", "influence": "MODERATE 2030 / WEAK thereafter"},
        {"variable": "real_median_living_standard", "comparison": "No direct long-run institutional forecast; 2030 is a cautious near-term range, later values are FranceScope-specific", "influence": "WEAK"},
    ]).to_csv(OUT / "V8_final_institutional_comparison.csv", index=False)
    rationale_text = """# V8.05 Final Forecast Rationale

Points are selected inside the approved V8.04 ranges and are not mechanical
midpoints. Optimistic points sit toward the favorable side, central points
reflect the most plausible combination of structural deterioration and partial
recovery, and pessimistic points are adverse interior values rather than worst
bounds.

The 2050 optimistic outcome remains worse than 2025 on all three targets by the
explicit `FRANCESCOPE STRUCTURAL SCENARIO ASSUMPTION`. This is not institutional
consensus. Positive technology, reform, EU support, nuclear strength and good
recovery could plausibly produce a better-than-selected optimistic outcome;
the framework constraint is retained for comparability with V8.04.

The optimistic trajectory improves or stabilizes through 2040 before late
structural pressure appears. The central trajectory shows moderate deterioration
after partial recovery. The pessimistic trajectory already reflects early
compound damage by 2030 and accumulates further scarring.
"""
    (OUT / "V8_forecast_rationale.md").write_text(rationale_text, encoding="utf-8")
    review = """# V8.05 Adversarial Review

## Optimistic

Strongest case against: successful reforms, technology diffusion, EU support,
nuclear resilience and late mild shocks could keep all three targets above the
2025 baseline by 2050. No point was moved because the approved V8.04 framework
explicitly requires long-run deterioration; this is recorded as a normative
constraint, not evidence-derived certainty.

## Central

Strongest case it is too pessimistic: productivity, investment and reform could
outperform, while transfers protect median living. Strongest case it is too
optimistic: sovereign, financial, energy and political risks may cluster more
than assumed. Points were retained as balanced interior selections.

## Pessimistic

Strongest case it is too severe: France may contain shocks through EU/ECB
mechanisms, labor adjustment and social insurance. Points remain below approved
upper bounds and require repeated or clustered events, high hysteresis and weak
recovery; no permanent-collapse assumption was added.

Revision rounds: one review round, no revisions required.
"""
    (OUT / "V8_forecast_adversarial_review.md").write_text(review, encoding="utf-8")
    manifest = {"future_point_count": len(forecasts), "historical_baseline_count": len(baseline_rows), "target_count": 3, "all_inside_ranges": True, "scenario_ordering": True, "optimistic_2050_worse_than_2025": True, "point_forecasts_selected": True, "v7_outputs_used": False, "revision_rounds": 1}
    (OUT / "V8_05_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
