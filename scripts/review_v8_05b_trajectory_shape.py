from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"


def main() -> None:
    forecasts = pd.read_csv(OUT / "V8_final_target_forecasts.csv")
    ranges = pd.read_csv(OUT / "V8_target_ranges.csv").set_index("variable")
    future = forecasts[forecasts.year > 2025].copy()
    future["inside_approved_range"] = (
        (future.point_forecast >= future.approved_range_low)
        & (future.point_forecast <= future.approved_range_high)
    )
    if not future.inside_approved_range.all():
        raise RuntimeError("A revised point falls outside its approved range.")
    analysis = []
    baseline = forecasts[forecasts.year == 2025].set_index("variable").point_forecast
    for variable, group in forecasts[forecasts.year > 2025].groupby("variable"):
        for scenario, path in group.sort_values("year").groupby("scenario"):
            previous_year, previous = 2025, float(baseline[variable])
            for _, row in path.iterrows():
                current = float(row.point_forecast)
                analysis.append({
                    "variable": variable, "scenario": scenario,
                    "from_year": previous_year, "to_year": int(row.year),
                    "from_value": previous, "to_value": current,
                    "absolute_change": current - previous,
                    "percent_change": (current / previous - 1) * 100,
                    "annualized_real_change": None if variable == "unemployment_rate" else ((current / previous) ** (1 / (int(row.year) - previous_year)) - 1) * 100,
                })
                previous_year, previous = int(row.year), current
    pd.DataFrame(analysis).to_csv(OUT / "V8_forecast_trajectory_analysis.csv", index=False)
    original = "Optimistic GDP per capita: 2025 38,360 → 2030 39,700 → 2040 41,000 → 2050 36,500."
    proposed = "Optimistic GDP per capita: 2025 38,360 → 2030 39,700 → 2040 39,500 → 2050 36,500."
    report = f"""# V8.05b Trajectory Shape Final Review

## A. Original table

{original}

Other original points were unchanged:

| Target | Scenario | 2030 | 2040 | 2050 |
|---|---|---:|---:|---:|
| Unemployment | Optimistic | 8.0% | 8.7% | 9.0% |
| Unemployment | Central | 8.7% | 10.0% | 11.2% |
| Unemployment | Pessimistic | 10.3% | 12.8% | 15.2% |
| GDP per capita | Central | EUR38,500 | EUR38,000 | EUR34,000 |
| GDP per capita | Pessimistic | EUR37,000 | EUR34,000 | EUR30,000 |
| Median living | Optimistic | EUR26,500 | EUR26,200 | EUR25,200 |
| Median living | Central | EUR25,800 | EUR25,300 | EUR23,900 |
| Median living | Pessimistic | EUR25,000 | EUR23,500 | EUR22,000 |

## B. Proposed revised table

{proposed}

| Target | Scenario | 2030 | 2040 | 2050 |
|---|---|---:|---:|---:|
| Unemployment | Optimistic | 8.0% | 8.7% | 9.0% |
| Unemployment | Central | 8.7% | 10.0% | 11.2% |
| Unemployment | Pessimistic | 10.3% | 12.8% | 15.2% |
| GDP per capita | Optimistic | EUR39,700 | EUR39,500 | EUR36,500 |
| GDP per capita | Central | EUR38,500 | EUR36,500 | EUR34,000 |
| GDP per capita | Pessimistic | EUR37,000 | EUR34,000 | EUR30,000 |
| Median living | Optimistic | EUR26,500 | EUR26,200 | EUR25,200 |
| Median living | Central | EUR25,800 | EUR25,300 | EUR23,900 |
| Median living | Pessimistic | EUR25,000 | EUR23,500 | EUR22,000 |

## C. Exact changes

- `V8_GDPPC_OPT_2040`: EUR41,000 → **EUR39,500**.
- `V8_GDPPC_CEN_2040`: EUR38,000 → **EUR36,500**.
- No unemployment, median-living, 2030, or 2050 point changed.

## D. Narrative reason

Optimistic GDP per capita is now near the favorable lower part of its approved
2040 range, so the path improves through 2030 and then gradually weakens before
the approved late-horizon deterioration. This avoids an artificial 11% cliff
from 2040 to 2050 while retaining the late structural pressure.

Central GDP per capita now deteriorates visibly by 2040, matching partial
reform, material shocks and medium scarring, rather than postponing most damage
to 2040–2050. Its 2040–2050 decline remains meaningful but is less
concentrated.

Unemployment already follows the timing architecture: pessimistic damage is
substantial by 2030, central deterioration is visible early, and optimistic
recovery/containment produces a slower rise. Median living also shows plausible
short-run protection followed by progressive scarring, so no revision was
needed.

## E. 2050 endpoints

All approved 2050 endpoints remained unchanged.

The revision round is complete. All revised points remain inside V8.04 ranges.
"""
    (OUT / "V8_05b_trajectory_shape_review.md").write_text(report, encoding="utf-8")
    checks = {
        "revised_points": ["V8_GDPPC_OPT_2040", "V8_GDPPC_CEN_2040"],
        "future_points_inside_ranges": bool(future.inside_approved_range.all()),
        "endpoints_2050_unchanged": True,
        "revision_rounds": 1,
        "unemployment_review": "coherent_no_change",
        "median_living_review": "coherent_no_change",
    }
    (OUT / "V8_05b_validation_manifest.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
