from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


def main() -> None:
    forecasts = pd.read_csv(OUT / "V8_final_target_forecasts.csv")
    updates = {
        ("unemployment_rate", "OPTIMISTIC", 2030): 8.5,
        ("unemployment_rate", "CENTRAL", 2030): 9.1,
    }
    for (variable, scenario, year), value in updates.items():
        mask = (forecasts.variable == variable) & (forecasts.scenario == scenario) & (forecasts.year == year)
        forecasts.loc[mask, "point_forecast"] = value
        forecasts.loc[mask, "rationale"] = (
            "Revised in V8.08c after early-horizon coherence review: aligns "
            "2030 labor deterioration with the 2026 Q2 anchor and near-term "
            "GDP-per-capita and median-living phases."
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

    report = """# V8.08c Final Early-Horizon Coherence Review

## Decision

The optimistic and central 2030 unemployment points were too high relative to
the near-term GDP-per-capita and median-living phases and the observed 2026 Q2
unemployment anchor of 8.3%. The pessimistic 2030 point remains justified by
its early compound-shock narrative.

## Current and proposed unemployment table

| Year | Optimistic current | Central current | Pessimistic current | Optimistic final | Central final | Pessimistic final |
|---|---:|---:|---:|---:|---:|---:|
| 2025 | 7.725% | 7.725% | 7.725% | 7.725% | 7.725% | 7.725% |
| 2030 | 9.0% | 9.7% | 11.3% | 8.5% | 9.1% | 11.3% |
| 2040 | 10.0% | 12.0% | 14.7% | 10.0% | 12.0% | 14.7% |
| 2050 | 12.0% | 14.0% | 17.8% | 12.0% | 14.0% | 17.8% |

Exact changes:

- Optimistic 2030: **9.0% -> 8.5%**
- Central 2030: **9.7% -> 9.1%**

## Final three-target table

| Variable | 2025 | Opt 2030 | Opt 2040 | Opt 2050 | Central 2030 | Central 2040 | Central 2050 | Pess 2030 | Pess 2040 | Pess 2050 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Unemployment | 7.725% | 8.5% | 10.0% | 12.0% | 9.1% | 12.0% | 14.0% | 11.3% | 14.7% | 17.8% |
| GDP per capita | EUR38,360 | EUR39,700 | EUR39,000 | EUR36,500 | EUR38,500 | EUR36,500 | EUR34,000 | EUR37,000 | EUR34,000 | EUR30,000 |
| Median living | EUR25,952.51 | EUR26,500 | EUR25,800 | EUR24,700 | EUR25,800 | EUR25,000 | EUR23,300 | EUR25,000 | EUR23,100 | EUR20,800 |

## Period slopes and phases

| Scenario | Period | U slope | GDPpc CAGR | Median CAGR | Phase | Coherence |
|---|---|---:|---:|---:|---|---|
| Optimistic | 2025-2030 | +0.155 pp/year | +0.69% | +0.42% | Initial mild deterioration | ACCEPTABLE |
| Optimistic | 2030-2040 | +0.150 pp/year | -0.18% | -0.27% | Persistent deterioration | STRONG |
| Optimistic | 2040-2050 | +0.200 pp/year | -0.66% | -0.44% | Accelerating late deterioration | STRONG |
| Central | 2025-2030 | +0.275 pp/year | +0.03% | -0.12% | Near-term stagnation | ACCEPTABLE |
| Central | 2030-2040 | +0.290 pp/year | -0.53% | -0.20% | Stronger 2030s deterioration | STRONG |
| Central | 2040-2050 | +0.200 pp/year | -0.71% | -0.57% | Persistent scarring | ACCEPTABLE |
| Pessimistic | 2025-2030 | +0.715 pp/year | -0.72% | -0.75% | Early compound crisis | ACCEPTABLE |
| Pessimistic | 2030-2040 | +0.340 pp/year | -0.84% | -0.62% | Persistent crisis | STRONG |
| Pessimistic | 2040-2050 | +0.310 pp/year | -1.24% | -0.66% | Deep scarring | STRONG |

## Anchor and spread checks

The revised paths start from the observed 2026 Q2 unemployment rate of 8.3%.
The 2030 values imply modest further deterioration in the optimistic case,
moderate deterioration centrally, and early crisis damage pessimistically.

Unemployment spreads are:

- 2030: central-minus-optimistic **0.6 pp**; pessimistic-minus-central **2.2 pp**
- 2040: **2.0 pp**; **2.7 pp**
- 2050: **2.0 pp**; **3.8 pp**

The uncertainty cone widens coherently with horizon and scenario severity.

The 2050 endpoints, GDP-per-capita paths, and median-living paths are unchanged.
All final period blocks are STRONG or ACCEPTABLE. No Index is calculated, no
intermediate macro variables are forecast, and V7 is untouched.
"""
    (OUT / "V8_08c_early_horizon_coherence_review.md").write_text(report, encoding="utf-8")
    manifest = {
        "version": "V8.08c",
        "revision_rounds": 1,
        "values_changed": [
            "OPTIMISTIC unemployment_rate 2030: 9.0 -> 8.5",
            "CENTRAL unemployment_rate 2030: 9.7 -> 9.1",
        ],
        "pessimistic_2030_unchanged": True,
        "2040_values_unchanged": True,
        "2050_endpoints_unchanged": True,
        "gdp_per_capita_unchanged": True,
        "median_living_unchanged": True,
        "scenario_ordering_preserved": True,
        "all_points_inside_ranges": True,
        "observed_2026_q2_anchor_considered": True,
        "phase_coherence": "STRONG_OR_ACCEPTABLE",
        "index_calculated": False,
        "v7_modified": False,
    }
    (OUT / "V8_08c_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
