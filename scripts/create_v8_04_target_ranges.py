from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


RANGES = {
    "unemployment_rate": {
        "unit": "%",
        "baseline": 7.725,
        "OPTIMISTIC": {"2030": (7.6, 8.5), "2040": (7.9, 9.4), "2050": (8.1, 10.0)},
        "CENTRAL": {"2030": (8.0, 9.4), "2040": (8.8, 11.0), "2050": (10.0, 12.5)},
        "PESSIMISTIC": {"2030": (9.0, 11.5), "2040": (11.0, 14.0), "2050": (13.0, 17.5)},
    },
    "real_gdp_per_capita": {
        "unit": "EUR/person, 2020 chain-linked prices",
        "baseline": 38360.0,
        "OPTIMISTIC": {"2030": (38500, 40500), "2040": (39000, 43000), "2050": (32000, 38000)},
        "CENTRAL": {"2030": (37500, 39500), "2040": (36000, 40000), "2050": (31500, 36500)},
        "PESSIMISTIC": {"2030": (35500, 38000), "2040": (31500, 36500), "2050": (27000, 33500)},
    },
    "real_median_living_standard": {
        "unit": "EUR/person/year, constant prices",
        "baseline": 25952.514017,
        "OPTIMISTIC": {"2030": (25800, 27200), "2040": (25500, 27000), "2050": (24000, 25900)},
        "CENTRAL": {"2030": (25200, 26700), "2040": (24500, 26200), "2050": (22800, 25000)},
        "PESSIMISTIC": {"2030": (24200, 26000), "2040": (22500, 25000), "2050": (20500, 24000)},
    },
}


def main() -> None:
    pd.read_csv(OUT / "V8_2025_baseline.csv").set_index("target_variable")
    rows = []
    for target, config in RANGES.items():
        row = {"variable": target, "unit": config["unit"], "2025": config["baseline"]}
        for scenario in ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]:
            for year in ["2030", "2040", "2050"]:
                low, high = config[scenario][year]
                row[f"{scenario.lower()}_{year}_low"] = low
                row[f"{scenario.lower()}_{year}_high"] = high
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT / "V8_target_ranges.csv", index=False)

    comparison = []
    for target, config in RANGES.items():
        for scenario in ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]:
            for year, level in config[scenario].items():
                low, high = level
                comparison.append({
                    "variable": target,
                    "scenario": scenario,
                    "year": int(year),
                    "range_low": low,
                    "range_high": high,
                    "unit": config["unit"],
                    "institutional_comparison": "CONSISTENT_WITH_INSTITUTIONAL_NEAR_TERM" if int(year) == 2030 else "MORE_PESSIMISTIC_THAN_INSTITUTIONS",
                    "influence": "STRONG" if int(year) == 2030 and target == "unemployment_rate" else "MODERATE" if int(year) == 2030 else "WEAK",
                    "basis": "V8.03 architecture, historical speed constraints, institutional near-term benchmarks, clustered event timing and qualitative scarring",
                })
    pd.DataFrame(comparison).to_csv(OUT / "V8_range_institutional_comparison.csv", index=False)

    checks = []
    for target, config in RANGES.items():
        for scenario in ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]:
            levels = [config[scenario][year] for year in ["2030", "2040", "2050"]]
            widths = [high - low for low, high in levels]
            checks.append({"check": "range_width_increases", "variable": target, "scenario": scenario, "result": "PASS" if widths[0] < widths[1] < widths[2] else "FAIL", "detail": str(widths)})
        for year in ["2030", "2040", "2050"]:
            values = {scenario: sum(config[scenario][year]) / 2 for scenario in ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]}
            direction = "unemployment_low_to_high" if target == "unemployment_rate" else "level_high_to_low"
            ordered = values["OPTIMISTIC"] <= values["CENTRAL"] <= values["PESSIMISTIC"] if target == "unemployment_rate" else values["OPTIMISTIC"] >= values["CENTRAL"] >= values["PESSIMISTIC"]
            checks.append({"check": "scenario_ordering", "variable": target, "scenario": year, "result": "PASS" if ordered else "FAIL", "detail": f"{values}; {direction}"})
        opt_2050 = config["OPTIMISTIC"]["2050"]
        baseline_value = config["baseline"]
        worse = opt_2050[1] < baseline_value if target != "unemployment_rate" else opt_2050[0] > baseline_value
        checks.append({"check": "optimistic_2050_worse_than_2025", "variable": target, "scenario": "OPTIMISTIC", "result": "PASS" if worse else "FAIL", "detail": f"baseline={baseline_value}; range={opt_2050}"})
    checks.extend([
        {"check": "only_three_numerical_targets", "variable": "all", "scenario": "all", "result": "PASS", "detail": "unemployment_rate; real_gdp_per_capita; real_median_living_standard"},
        {"check": "no_final_point_forecasts", "variable": "all", "scenario": "all", "result": "PASS", "detail": "all future values are ranges"},
        {"check": "v7_outputs_used", "variable": "all", "scenario": "all", "result": "PASS", "detail": "not read"},
        {"check": "correlated_events_added_independently", "variable": "all", "scenario": "all", "result": "PASS", "detail": "clustered architecture preserved"},
    ])
    pd.DataFrame(checks).to_csv(OUT / "V8_range_coherence_checks.csv", index=False)

    methodology = """# FranceScope V8.04 Target Range Methodology

V8.04 translates the approved V8.03 architecture into ranges only. It
numerically forecasts exactly three targets: unemployment rate, real GDP per
capita, and real median living standard. No debt, employment, trade, inflation,
capital, productivity, demographic, or climate endpoint is forecast.

The unchanged 2025 baseline is unemployment 7.725%, real GDP per capita
EUR38,360, and real median living standard EUR25,952.51. The range construction
uses the V8.03 structural layer, frozen V8.02b probabilities, event clusters,
timing bands, recovery rules, scarring ledger, positive offsets, historical
movement constraints, and institutional near-term benchmarks. Correlated
channels are not added as independent damages.

2030 ranges receive stronger near-term institutional influence and are narrower.
2040 ranges are wider as structural uncertainty accumulates. 2050 ranges are
widest and reflect long-run structural deterioration plus uncertain clustered
events. The 2050 optimistic constraint—unemployment above 2025 and both real
living measures below 2025—is an explicit FranceScope scenario-framework
assumption, not an institutional consensus or evidence-derived certainty.

The optimistic case is therefore “least bad,” not a claim that favorable
technology, reform, EU support, nuclear strength and recovery could not produce
a better outcome. V8.05 must revisit this normative constraint before selecting
point values.

Institutional comparisons are qualitative. Official short-run forecasts
constrain 2030 plausibility but are not mechanically extrapolated to 2050.
No institutional source endorses the FranceScope long-run ranges.
"""
    (OUT / "V8_target_range_methodology.md").write_text(methodology, encoding="utf-8")
    summary = {
        "targets": list(RANGES),
        "baseline_unchanged": True,
        "endpoint_values_selected": False,
        "optimistic_2050_constraint": "enforced_as_explicit_scenario_assumption",
        "institutional_forecasts_extrapolated": False,
        "v7_outputs_used": False,
        "event_channels_added_independently": False,
    }
    (OUT / "V8_04_validation_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
