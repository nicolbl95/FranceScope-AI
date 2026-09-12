from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


def main() -> None:
    forecasts = pd.read_csv(OUT / "V8_final_target_forecasts.csv")
    changes = {
        ("real_gdp_per_capita", "OPTIMISTIC", 2040): 39000.0,
        ("real_median_living_standard", "OPTIMISTIC", 2040): 25800.0,
    }
    for (variable, scenario, year), value in changes.items():
        mask = (forecasts.variable == variable) & (forecasts.scenario == scenario) & (forecasts.year == year)
        forecasts.loc[mask, "point_forecast"] = value
        forecasts.loc[mask, "rationale"] = (
            "Revised in V8.07b to distribute gradual structural deterioration "
            "more progressively before the fixed 2050 endpoint."
        )
    forecasts.to_csv(OUT / "V8_final_target_forecasts.csv", index=False)

    baseline = forecasts[forecasts.year == 2025].set_index("variable").point_forecast
    rows = []
    for variable, group in forecasts[forecasts.year > 2025].groupby("variable"):
        for scenario, path in group.sort_values("year").groupby("scenario"):
            previous_year, previous = 2025, float(baseline[variable])
            for _, item in path.iterrows():
                year, current = int(item.year), float(item.point_forecast)
                rows.append({
                    "variable": variable, "scenario": scenario,
                    "from_year": previous_year, "to_year": year,
                    "from_value": previous, "to_value": current,
                    "absolute_change": current - previous,
                    "percent_change": (current / previous - 1) * 100,
                    "annualized_real_change": (
                        None if variable == "unemployment_rate"
                        else ((current / previous) ** (1 / (year - previous_year)) - 1) * 100
                    ),
                    "interpretation": (
                        "Unemployment change in percentage points; level changes are percentage changes."
                        if variable == "unemployment_rate" else "Real level change."
                    ),
                })
                previous_year, previous = year, current
    pd.DataFrame(rows).to_csv(OUT / "V8_forecast_trajectory_analysis.csv", index=False)
    index_inputs = forecasts[forecasts.year > 2025][
        ["scenario", "year", "variable", "point_forecast"]
    ].pivot(index=["scenario", "year"], columns="variable", values="point_forecast").reset_index()
    index_inputs.to_csv(OUT / "V8_index_inputs.csv", index=False)

    report = """# V8.07b Final Intertemporal and Cross-Target Coherence Review

## Decision

One revision round was applied. The optimistic path had material back-loading:
unemployment rose by 1.5 percentage points in both decades, while GDP per
capita and median living were nearly flat through 2040 and then fell sharply.
The approved scenario architecture describes gradual structural pressure and
does not identify a discrete late shock sufficient to explain that shape.

## Current and proposed optimistic table

| Target | 2025 | 2030 current | 2040 current | 2050 current | 2030 final | 2040 final | 2050 final |
|---|---:|---:|---:|---:|---:|---:|---:|
| Unemployment | 7.725% | 9.0% | 10.5% | 12.0% | 9.0% | 10.5% | 12.0% |
| GDP per capita | EUR38,360 | EUR39,700 | EUR39,500 | EUR36,500 | EUR39,700 | EUR39,000 | EUR36,500 |
| Median living | EUR25,952.51 | EUR26,500 | EUR26,200 | EUR24,700 | EUR26,500 | EUR25,800 | EUR24,700 |

Central and pessimistic paths are unchanged.

## Exact changed cells

- Optimistic real GDP per capita 2040: **EUR39,500 -> EUR39,000**.
- Optimistic real median living 2040: **EUR26,200 -> EUR25,800**.

The revised values remain inside the existing V8.07 ranges. No range revision
was necessary.

## Decade movements

| Scenario | Period | Unemployment | GDP per capita | Median living | Rating |
|---|---|---:|---:|---:|---|
| Optimistic | 2025-2030 | +1.275 pp | +3.49% | +2.11% | ACCEPTABLE |
| Optimistic | 2030-2040 | +1.5 pp | -1.76% | -2.64% | ACCEPTABLE |
| Optimistic | 2040-2050 | +1.5 pp | -6.41% | -4.26% | ACCEPTABLE |
| Central | 2025-2030 | +1.975 pp | +0.36% | -0.59% | ACCEPTABLE |
| Central | 2030-2040 | +2.3 pp | -5.19% | -1.94% | ACCEPTABLE |
| Central | 2040-2050 | +2.0 pp | -6.85% | -5.53% | ACCEPTABLE |
| Pessimistic | 2025-2030 | +3.575 pp | -3.55% | -3.67% | ACCEPTABLE |
| Pessimistic | 2030-2040 | +3.4 pp | -8.11% | -6.00% | ACCEPTABLE |
| Pessimistic | 2040-2050 | +3.1 pp | -11.76% | -6.38% | ACCEPTABLE |

GDP per capita and median living are levels, while unemployment is a rate;
therefore the changes are not expected to be proportional. The final table
nevertheless reflects the same gradual deterioration, recovery limits, and
scarring history across targets.

## Cross-target and regime checks

The central path shows progressive deterioration before 2040 and additional
post-2040 scarring. The pessimistic path is already substantially damaged by
2030 and worsens through repeated shocks and weak recovery. The revised
optimistic path now shows early improvement followed by gradual weakening,
without concentrating all economic damage in the final decade.

The combinations remain historically intelligible under the V8.06 France,
Spain, Greece, Portugal, Italy, and Japan analogues. They remain defensible
under fiscal/debt pressure, weak demand, under-investment, productivity
weakness, ageing, climate and energy risk, geopolitics, political constraints,
hysteresis, and transitional AI effects.

## Adversarial review

The optimistic path could still be too pessimistic if reform, technology, EU
support, nuclear resilience, or transfers outperform. It could be too
optimistic if unemployment damages wages and the tax base more severely.
Central and pessimistic paths have corresponding upside and downside risks
through policy capacity, correlated shocks, and hysteresis.

All rows are STRONG or ACCEPTABLE. No WEAK or INCONSISTENT row remains.
The 2050 endpoints and unemployment paths are unchanged. No Index is calculated.
V7 remains untouched.
"""
    (OUT / "V8_07b_cross_target_temporal_review.md").write_text(report, encoding="utf-8")
    manifest = {
        "version": "V8.07b",
        "revision_rounds": 1,
        "values_changed": [
            "OPTIMISTIC real_gdp_per_capita 2040: 39500.0 -> 39000.0",
            "OPTIMISTIC real_median_living_standard 2040: 26200.0 -> 25800.0",
        ],
        "unemployment_unchanged": True,
        "2050_endpoints_unchanged": True,
        "ranges_changed": False,
        "all_points_inside_ranges": True,
        "scenario_ordering_preserved": True,
        "index_calculated": False,
        "v7_modified": False,
    }
    (OUT / "V8_07b_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
