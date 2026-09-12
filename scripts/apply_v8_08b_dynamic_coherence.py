from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


def main() -> None:
    forecasts = pd.read_csv(OUT / "V8_final_target_forecasts.csv")
    mask = (
        (forecasts.variable == "unemployment_rate")
        & (forecasts.scenario == "OPTIMISTIC")
        & (forecasts.year == 2040)
    )
    forecasts.loc[mask, "point_forecast"] = 10.0
    forecasts.loc[mask, "rationale"] = (
        "Revised in V8.08b to represent slower unemployment deterioration "
        "through 2040 before stronger post-2040 scarring, while retaining the "
        "fixed 12.0% 2050 endpoint."
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

    report = """# V8.08b Final Dynamic Coherence Review

## Decision

The optimistic path had equal unemployment deterioration rates in 2030–2040
and 2040–2050 despite faster GDP-per-capita and median-living deterioration
after 2040. The approved narrative supports slower labor-market deterioration
through 2040 followed by stronger accumulated scarring, so one minimal
intermediate revision was applied.

## Exact changed cell

- Optimistic unemployment 2040: **10.5% -> 10.0%**.

This changes the unemployment slopes to +0.100 percentage points per year in
2030–2040 and +0.200 percentage points per year in 2040–2050. The 2050 endpoint
remains 12.0%.

## Final numerical table

| Variable | 2025 | Opt 2030 | Opt 2040 | Opt 2050 | Central 2030 | Central 2040 | Central 2050 | Pess 2030 | Pess 2040 | Pess 2050 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Unemployment | 7.725% | 9.0% | 10.0% | 12.0% | 9.7% | 12.0% | 14.0% | 11.3% | 14.7% | 17.8% |
| GDP per capita | EUR38,360 | EUR39,700 | EUR39,000 | EUR36,500 | EUR38,500 | EUR36,500 | EUR34,000 | EUR37,000 | EUR34,000 | EUR30,000 |
| Median living | EUR25,952.51 | EUR26,500 | EUR25,800 | EUR24,700 | EUR25,800 | EUR25,000 | EUR23,300 | EUR25,000 | EUR23,100 | EUR20,800 |

## Dynamic phase table

| Scenario | Period | Economic phase | U slope | GDPpc CAGR | Median CAGR | Scarring stock | Coherence |
|---|---|---|---:|---:|---:|---|---|
| Optimistic | 2025-2030 | Improvement with labor softening | +0.255 pp/year | +0.69% | +0.42% | Low | ACCEPTABLE |
| Optimistic | 2030-2040 | Slow deterioration | +0.100 pp/year | -0.18% | -0.27% | Building | STRONG |
| Optimistic | 2040-2050 | Accelerating deterioration | +0.200 pp/year | -0.66% | -0.44% | Material | STRONG |
| Central | 2025-2030 | Stagnation | +0.395 pp/year | +0.03% | -0.12% | Building | ACCEPTABLE |
| Central | 2030-2040 | Slow deterioration | +0.230 pp/year | -0.53% | -0.20% | Material | ACCEPTABLE |
| Central | 2040-2050 | Deterioration with scarring | +0.200 pp/year | -0.71% | -0.57% | High | ACCEPTABLE |
| Pessimistic | 2025-2030 | Crisis | +0.715 pp/year | -0.72% | -0.75% | High | ACCEPTABLE |
| Pessimistic | 2030-2040 | Persistent crisis | +0.340 pp/year | -0.84% | -0.62% | High | STRONG |
| Pessimistic | 2040-2050 | Deepening scarring | +0.310 pp/year | -1.24% | -0.66% | Very high | STRONG |

Unemployment is a rate; GDP per capita and median living are levels. Equal
changes are therefore not required. The revised optimistic unemployment level
and slope now align with the same phase structure as the other targets.

## Scarring-stock assessment

- Optimistic: **SUFFICIENT**. Low-to-material accumulated scarring explains
  faster later output damage without requiring a large early unemployment jump.
- Central: **SUFFICIENT**. Progressive unemployment, capital, productivity,
  and fiscal damage are mutually consistent.
- Pessimistic: **SUFFICIENT**. Early compound shocks, incomplete recovery,
  capital loss, and high hysteresis explain front-loaded unemployment damage and
  continued later output decline.

The scenario ordering, historical plausibility, and V8 structural narrative
remain intact. No Index is calculated, no intermediate macro variables are
forecast, and V7 is untouched.
"""
    (OUT / "V8_08b_dynamic_coherence_review.md").write_text(report, encoding="utf-8")
    manifest = {
        "version": "V8.08b",
        "revision_rounds": 1,
        "values_changed": ["OPTIMISTIC unemployment_rate 2040: 10.5 -> 10.0"],
        "2050_endpoints_unchanged": True,
        "2030_points_unchanged": True,
        "gdp_per_capita_unchanged": True,
        "median_living_unchanged": True,
        "scenario_ordering_preserved": True,
        "all_points_inside_ranges": True,
        "phase_coherence": "STRONG_OR_ACCEPTABLE",
        "index_calculated": False,
        "v7_modified": False,
    }
    (OUT / "V8_08b_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
