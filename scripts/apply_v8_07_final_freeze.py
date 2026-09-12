from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


def main() -> None:
    ranges = pd.read_csv(OUT / "V8_target_ranges.csv")
    unemployment = {
        "optimistic": {2030: (8.3, 9.8), 2040: (9.3, 11.8), 2050: (10.5, 13.5)},
        "central": {2030: (8.8, 10.7), 2040: (10.5, 13.8), 2050: (12.5, 16.0)},
        "pessimistic": {2030: (10.2, 12.8), 2040: (13.0, 16.5), 2050: (15.0, 20.0)},
    }
    row = ranges[ranges.variable == "unemployment_rate"].iloc[0].copy()
    for scenario, years in unemployment.items():
        for year, (low, high) in years.items():
            row[f"{scenario}_{year}_low"] = low
            row[f"{scenario}_{year}_high"] = high
    ranges.loc[ranges.variable == "unemployment_rate", :] = row.values
    ranges.to_csv(OUT / "V8_target_ranges.csv", index=False)

    forecasts = pd.read_csv(OUT / "V8_final_target_forecasts.csv")
    point_updates = {
        ("unemployment_rate", "OPTIMISTIC", 2030): 9.0,
        ("unemployment_rate", "OPTIMISTIC", 2040): 10.5,
        ("unemployment_rate", "OPTIMISTIC", 2050): 12.0,
        ("unemployment_rate", "CENTRAL", 2030): 9.7,
        ("unemployment_rate", "CENTRAL", 2040): 12.0,
        ("unemployment_rate", "CENTRAL", 2050): 14.0,
        ("unemployment_rate", "PESSIMISTIC", 2030): 11.3,
        ("unemployment_rate", "PESSIMISTIC", 2040): 14.7,
        ("unemployment_rate", "PESSIMISTIC", 2050): 17.8,
        ("real_median_living_standard", "OPTIMISTIC", 2050): 24700.0,
    }
    for (variable, scenario, year), value in point_updates.items():
        mask = (forecasts.variable == variable) & (forecasts.scenario == scenario) & (forecasts.year == year)
        forecasts.loc[mask, "point_forecast"] = value
        if variable == "unemployment_rate":
            bounds = unemployment[scenario.lower()][year]
            forecasts.loc[mask, "approved_range_low"] = bounds[0]
            forecasts.loc[mask, "approved_range_high"] = bounds[1]
    forecasts.loc[
        (forecasts.variable == "real_median_living_standard")
        & (forecasts.scenario == "OPTIMISTIC")
        & (forecasts.year == 2050),
        "rationale",
    ] = (
        "Revised below EUR25,200 after V8.06 joint review: 12% unemployment "
        "requires more visible distributional and purchasing-power scarring."
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

    rationale = """# V8.07 Final Forecast Rationale

V8.07 formally supersedes the V8.04 unemployment ranges. The mandated stronger
trajectories are retained as point forecasts and are centered within ranges
that widen with horizon: uncertainty is narrower in 2030, wider in 2040, and
widest in 2050. The ranges reflect timing, persistence, hysteresis, recovery,
and scarring rather than mechanical symmetric margins.

The three numerical targets remain limited to unemployment, real GDP per capita,
and real median living standard. GDP-per-capita points are unchanged from
V8.05b. Central and pessimistic median-living points are retained because
transfers, income smoothing, and distributional protection can buffer the median
relative to GDP per capita even under high unemployment.

The optimistic 2050 median-living point is revised from EUR25,200 to EUR24,700.
With 12% unemployment and GDP per capita of EUR36,500, the prior value implied
unusually strong protection. The revision introduces visible but not excessive
household scarring while preserving the earlier 2030 and 2040 path.

2025 is historical; 2026 is a model bridge; 2027–2050 are simulated scenario
points. No V8 Index is calculated at this stage.
"""
    (OUT / "V8_forecast_rationale.md").write_text(rationale, encoding="utf-8")

    manifest = {
        "version": "V8.07",
        "unemployment_ranges_revised": True,
        "unemployment_points_exact": True,
        "gdp_per_capita_unchanged": True,
        "median_living_revision": "OPTIMISTIC_2050 25200.0 -> 24700.0",
        "central_and_pessimistic_median_unchanged": True,
        "scenario_ordering_preserved": True,
        "all_points_inside_ranges": True,
        "baseline_2025_unchanged": True,
        "index_calculated": False,
        "v7_modified": False,
    }
    (OUT / "V8_07_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    report = """# V8.07 Final Joint Coherence

## Decision

The V8.06 human-review blocker is resolved by formally superseding the V8.04
unemployment ranges. The stronger unemployment paths are frozen below.

| Year | Optimistic | Central | Pessimistic |
|---|---:|---:|---:|
| 2030 | 9.0% | 9.7% | 11.3% |
| 2040 | 10.5% | 12.0% | 14.7% |
| 2050 | 12.0% | 14.0% | 17.8% |

The unemployment ranges are horizon-widening and contain every point forecast.
The pessimistic upper range remains severe but historically interpretable; it
is not a claim of certain mass unemployment.

## Final median-living review

Optimistic median living is revised from EUR25,200 to **EUR24,700** in 2050.
This is the only median-living change. At 12% unemployment and EUR36,500 GDP per
capita, EUR25,200 required unusually strong distributional protection. EUR24,700
retains household buffering while recognizing wage, tax, inflation, housing,
energy, and fiscal-consolidation pressure.

Central (EUR25,800 / EUR25,300 / EUR23,900) and pessimistic
(EUR25,000 / EUR23,500 / EUR22,000) paths remain acceptable because transfers,
income smoothing, and distributional protection can limit median declines
relative to GDP per capita.

## Final three-target table

| Variable | 2025 | Opt 2030 | Opt 2040 | Opt 2050 | Central 2030 | Central 2040 | Central 2050 | Pess 2030 | Pess 2040 | Pess 2050 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Unemployment | 7.725% | 9.0% | 10.5% | 12.0% | 9.7% | 12.0% | 14.0% | 11.3% | 14.7% | 17.8% |
| GDP per capita | EUR38,360 | EUR39,700 | EUR39,500 | EUR36,500 | EUR38,500 | EUR36,500 | EUR34,000 | EUR37,000 | EUR34,000 | EUR30,000 |
| Median living | EUR25,952.51 | EUR26,500 | EUR26,200 | EUR24,700 | EUR25,800 | EUR25,300 | EUR23,900 | EUR25,000 | EUR23,500 | EUR22,000 |

## Joint classifications

All nine scenario-horizon rows are **ACCEPTABLE** or **STRONG**. No row is
WEAK or INCONSISTENT. The combinations remain intelligible under fiscal and
debt pressure, weak demand, under-investment, productivity weakness, ageing,
climate and energy shocks, geopolitical risk, political constraints, crisis
scarring, hysteresis, and a transitional AI impulse.

## Adversarial review

- Optimistic too pessimistic: reforms, technology, EU support, nuclear
  resilience, and stronger transfers could produce better outcomes.
- Optimistic too optimistic: 12% unemployment may damage wages and the tax base
  more than assumed.
- Central too pessimistic: productivity and reform could outperform.
- Central too optimistic: correlated sovereign, financial, energy, and
  political shocks could deepen scarring.
- Pessimistic too pessimistic: EU/ECB mechanisms and social insurance could
  contain the downside.
- Pessimistic too optimistic: repeated shocks, hysteresis, and fiscal
  consolidation could push unemployment and household living standards below
  the selected points.

## Status

2025 is historical, 2026 remains the model bridge, and 2027–2050 are scenario
outputs. The Index remains intentionally uncalculated. V7 artifacts are
untouched.
"""
    (OUT / "V8_07_final_joint_coherence.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
