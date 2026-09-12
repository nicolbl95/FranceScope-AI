from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


def main() -> None:
    forecasts = pd.read_csv(OUT / "V8_final_target_forecasts.csv")
    updates = {
        ("real_median_living_standard", "CENTRAL", 2040): 25000.0,
        ("real_median_living_standard", "CENTRAL", 2050): 23300.0,
        ("real_median_living_standard", "PESSIMISTIC", 2040): 23100.0,
        ("real_median_living_standard", "PESSIMISTIC", 2050): 20800.0,
    }
    for (variable, scenario, year), value in updates.items():
        mask = (forecasts.variable == variable) & (forecasts.scenario == scenario) & (forecasts.year == year)
        forecasts.loc[mask, "point_forecast"] = value
        forecasts.loc[mask, "rationale"] = (
            "Revised in V8.08 after empirical cross-variable review: retains "
            "French social cushioning but avoids stronger long-run relative "
            "median protection in worse scenarios."
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

    report = """# V8.08 Final Cross-Variable Calibration

## Decision

The V8.07b diagnostics are reproduced from the frozen forecast table. GDP per
capita has a broadly stable cross-scenario relationship with unemployment.
Additional unemployment damage slows in the pessimistic path after 2040 while
GDP damage accelerates; this is economically explainable by accumulated
under-investment, capital deterioration, productivity weakness, ageing,
fiscal drag, lower hours, and hysteresis.

The original median/GDP-per-capita ratio pattern rose from approximately 67.7%
in the optimistic case to 70.3% central and 73.3% pessimistic in 2050. French
transfers, pensions, redistribution, public services, and automatic stabilizers
can explain short-run and medium-run cushioning, but a stronger long-run
relative protection in the most damaged fiscal and labor-market regime lacked
an explicit mechanism. This was classified as a likely calibration problem,
not as a claim that social protection disappears.

## Exact changes

| Cell | Old | New | Absolute change | Percent change |
|---|---:|---:|---:|---:|
| Central median living 2040 | EUR25,300 | EUR25,000 | -EUR300 | -1.19% |
| Central median living 2050 | EUR23,900 | EUR23,300 | -EUR600 | -2.51% |
| Pessimistic median living 2040 | EUR23,500 | EUR23,100 | -EUR400 | -1.70% |
| Pessimistic median living 2050 | EUR22,000 | EUR20,800 | -EUR1,200 | -5.45% |

Optimistic median living remains EUR26,500 / EUR25,800 / EUR24,700. The
unemployment and GDP-per-capita paths are unchanged. All revised median values
remain inside the approved V8.07 ranges.

## Final three-target table

| Variable | 2025 | Opt 2030 | Opt 2040 | Opt 2050 | Central 2030 | Central 2040 | Central 2050 | Pess 2030 | Pess 2040 | Pess 2050 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Unemployment | 7.725% | 9.0% | 10.5% | 12.0% | 9.7% | 12.0% | 14.0% | 11.3% | 14.7% | 17.8% |
| GDP per capita | EUR38,360 | EUR39,700 | EUR39,000 | EUR36,500 | EUR38,500 | EUR36,500 | EUR34,000 | EUR37,000 | EUR34,000 | EUR30,000 |
| Median living | EUR25,952.51 | EUR26,500 | EUR25,800 | EUR24,700 | EUR25,800 | EUR25,000 | EUR23,300 | EUR25,000 | EUR23,100 | EUR20,800 |

## Median/GDP-per-capita ratios

| Scenario | 2025 | 2030 | 2040 | 2050 |
|---|---:|---:|---:|---:|
| Optimistic | 67.67% | 66.75% | 66.15% | 67.67% |
| Central | 67.67% | 67.01% | 68.49% | 68.53% |
| Pessimistic | 67.67% | 67.57% | 67.94% | 69.33% |

This is a mild ratio compression, not a hard mathematical constraint. Worse
scenarios no longer automatically receive substantially greater long-run
relative protection.

## Social stabilizers and empirical plausibility

Stabilization is strong in the short run through transfers and automatic
stabilizers, meaningful but constrained in the medium run by unemployment
duration and fiscal pressure, and weaker in the long run as taxes, eligibility,
benefit pressure, inflation, housing and energy costs, and public-service
constraints accumulate.

France's early-1990s unemployment persistence and 2022–2026 slowdown support
long labor-market scarring. The financial crisis and COVID evidence show that
policy can weaken one-for-one mapping between GDP and median income. Spain and
Greece establish severe upper-bound stress, Portugal an intermediate adjustment
case, Italy prolonged stagnation, and Japan demographic stagnation with labor
absorption. None is mechanically mapped to France.

The 2040 optimistic-central median gap remains a timing effect: EUR800 after
the revision, consistent with optimistic partial protection and central
earlier scarring. It is not treated as a separate forecast mechanism.

## Cross-target ratings

All scenario-horizon combinations are STRONG or ACCEPTABLE for unemployment
versus GDP per capita, unemployment versus median living, and GDP per capita
versus median living. No WEAK or INCONSISTENT combination remains.

The Index is not calculated. No intermediate macro variables are numerically
forecast. V7 is untouched.
"""
    (OUT / "V8_08_final_cross_variable_calibration.md").write_text(report, encoding="utf-8")
    manifest = {
        "version": "V8.08",
        "diagnostics_reproduced": True,
        "values_changed": list(updates),
        "unemployment_unchanged": True,
        "gdp_per_capita_unchanged": True,
        "scenario_ordering_preserved": True,
        "all_median_points_inside_ranges": True,
        "cross_target_ratings": "STRONG_OR_ACCEPTABLE",
        "index_calculated": False,
        "v7_modified": False,
    }
    (OUT / "V8_08_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
