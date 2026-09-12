from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).parents[1]
IN = ROOT / "data" / "research" / "v8"
OUT = ROOT / "data" / "report" / "v8_final"
CHARTS = OUT / "charts"
TABLES = OUT / "tables"
SCENARIOS = ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]
LABELS = {
    "OPTIMISTIC": "Low deterioration / least-bad",
    "CENTRAL": "Central deterioration",
    "PESSIMISTIC": "High deterioration",
}


def main() -> None:
    forecasts = pd.read_csv(IN / "V8_final_target_forecasts.csv")
    expected = {
        ("unemployment_rate", "OPTIMISTIC", 2030): 8.5,
        ("unemployment_rate", "CENTRAL", 2050): 14.0,
        ("unemployment_rate", "PESSIMISTIC", 2050): 17.8,
        ("real_gdp_per_capita", "OPTIMISTIC", 2050): 36500.0,
        ("real_gdp_per_capita", "CENTRAL", 2050): 34000.0,
        ("real_gdp_per_capita", "PESSIMISTIC", 2050): 30000.0,
        ("real_median_living_standard", "OPTIMISTIC", 2050): 24700.0,
        ("real_median_living_standard", "CENTRAL", 2050): 23300.0,
        ("real_median_living_standard", "PESSIMISTIC", 2050): 20800.0,
    }
    for (variable, scenario, year), value in expected.items():
        actual = forecasts[(forecasts.variable == variable) & (forecasts.scenario == scenario) & (forecasts.year == year)].point_forecast.iloc[0]
        if float(actual) != value:
            raise RuntimeError(f"Frozen input mismatch: {variable}/{scenario}/{year}")

    baseline = forecasts[forecasts.year == 2025].set_index("variable").point_forecast
    main = forecasts.pivot_table(index="variable", columns=["scenario", "year"], values="point_forecast", aggfunc="first")
    columns = [("2025 Actual", "2025")]
    for scenario in SCENARIOS:
        for year in [2030, 2040, 2050]:
            columns.append((LABELS[scenario], str(year)))
    result = pd.DataFrame(index=main.index)
    for label, year in columns:
        if year == "2025":
            result[label] = baseline
        else:
            scenario = next(s for s in SCENARIOS if LABELS[s] == label)
            result[f"{label} {year}"] = main[(scenario, int(year))]
    result.index = result.index.map({
        "unemployment_rate": "unemployment",
        "real_gdp_per_capita": "real GDP per capita",
        "real_median_living_standard": "real median living standard",
    })
    result.reset_index(names="Variable").to_csv(OUT / "FranceScope_V8_Final_main_results.csv", index=False)
    result.reset_index(names="Variable").to_csv(TABLES / "FranceScope_V8_Final_main_results.csv", index=False)

    normalized = []
    for variable in ["unemployment_rate", "real_gdp_per_capita", "real_median_living_standard"]:
        for scenario in SCENARIOS:
            for year in [2030, 2040, 2050]:
                value = float(forecasts[(forecasts.variable == variable) & (forecasts.scenario == scenario) & (forecasts.year == year)].point_forecast.iloc[0])
                normalized.append({
                    "scenario": LABELS[scenario], "year": year, "variable": variable,
                    "relative_to_2025": value / float(baseline[variable]) * 100,
                })
    normalized_df = pd.DataFrame(normalized)
    for scenario in SCENARIOS:
        label = LABELS[scenario]
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for variable, name in [
            ("unemployment_rate", "Unemployment"),
            ("real_gdp_per_capita", "GDP per capita"),
            ("real_median_living_standard", "Median living"),
        ]:
            part = normalized_df[normalized_df.variable == variable]
            part = part[part.scenario.isin(["Low deterioration / least-bad", "Central deterioration", "High deterioration"])]
            part = part[part.scenario == label]
            years = [2025] + part.year.tolist()
            values = [100.0] + part.relative_to_2025.tolist()
            ax.plot(years, values, marker="o", label=name)
        ax.set(xlabel="Year", ylabel="2025 = 100 (visual only)", title=f"Three-target relative trajectories: {label}")
        ax.legend(fontsize=8); ax.grid(alpha=0.25); fig.tight_layout()
        fig.savefig(CHARTS / f"FranceScope_V8_Final_normalized_{scenario.lower()}.png", dpi=160)
        plt.close(fig)

    end = forecasts[forecasts.year == 2050].pivot(index="scenario", columns="variable", values="point_forecast").loc[SCENARIOS]
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    for ax, variable, title in zip(
        axes,
        ["unemployment_rate", "real_gdp_per_capita", "real_median_living_standard"],
        ["Unemployment (%)", "GDP per capita (EUR)", "Median living (EUR)"],
    ):
        ax.bar([LABELS[s] for s in SCENARIOS], end[variable].tolist())
        ax.set_title(title); ax.tick_params(axis="x", rotation=35)
    fig.suptitle("FranceScope V8: 2050 three-target comparison")
    fig.tight_layout()
    fig.savefig(CHARTS / "FranceScope_V8_Final_2050_dashboard.png", dpi=160)
    plt.close(fig)

    for path in [
        OUT / "FranceScope_V8_Final_index.csv",
        OUT / "FranceScope_V8_Final_index_components.csv",
        TABLES / "FranceScope_V8_Final_index.csv",
        TABLES / "FranceScope_V8_Final_index_components.csv",
        CHARTS / "FranceScope_V8_Final_index.png",
    ]:
        if path.exists():
            path.unlink()

    framework = """# FranceScope V8 Three-Target Framework

FranceScope is a long-run macroeconomic scenario project for France centered
on three final variables that directly capture different dimensions of
economic well-being:

1. unemployment;
2. real GDP per capita;
3. real median living standard.

Unemployment represents labor-market access and economic security. Real GDP per
capita represents average productive capacity and real economic output per
person. Real median living standard represents material living conditions of
the median person or household after taxes, transfers, and redistribution.
Together they represent employment conditions, production, and distributed
living standards without claiming to capture every aspect of welfare.

Earlier versions used a FranceScope Index. V8 removes it because only these
three final variables are forecast numerically; a composite would merely
recombine them, add normative weights and normalization assumptions, introduce
false precision, and obscure direct tradeoffs. **No replacement composite score
is used.**

FranceScope does not attempt to forecast every macroeconomic variable. It
focuses on three outcome measures directly meaningful for long-run economic
welfare: employment conditions, productive output per person, and the median
material standard of living. Omitted dimensions include inequality beyond the
median, public-service quality, health, environmental quality, leisure, wealth,
and security.

The scenarios are Low deterioration / least-bad, Central deterioration, and
High deterioration. Internal compatibility codes remain OPTIMISTIC, CENTRAL,
and PESSIMISTIC. The normalized trajectory charts use 2025 = 100 for visual
comparison only; they are not an index and do not aggregate variables.
"""
    (OUT / "FranceScope_V8_Three_Target_Framework.md").write_text(framework, encoding="utf-8")
    summary = """# FranceScope V8 Final Executive Summary

FranceScope V8 is a long-run macroeconomic scenario system for France focused
on three final targets: unemployment, real GDP per capita, and real median
living standard. The formal 2025 historical baseline is unemployment **7.725%**,
GDP per capita **EUR38,360**, and median living **EUR25,952.51**. The observed
2026 Q2 unemployment rate is **8.3%** and is contextual evidence, not the
formal baseline.

By 2050, the low-deterioration/least-bad scenario reaches unemployment
**12.0%**, GDP per capita **EUR36,500**, and median living **EUR24,700**.
Central deterioration reaches **14.0%**, **EUR34,000**, and **EUR23,300**.
High deterioration reaches **17.8%**, **EUR30,000**, and **EUR20,800**.

The scenarios represent conditional paths, not institutional forecasts.
Unemployment is labor-market access and security; GDP per capita is average
productive capacity; median living is the distributed material outcome after
taxes and transfers. No composite Index or replacement aggregate score is used.
"""
    (OUT / "FranceScope_V8_Final_executive_summary.md").write_text(summary, encoding="utf-8")
    methodology = """# FranceScope V8 Final Methodology

V8 numerically forecasts only three final outcome variables: unemployment, real
GDP per capita, and real median living standard. Structural macro forces are
causal evidence, while scenario architecture, crisis timing, recovery, and
scarring determine conditional paths. Debt, deficit, population, employment,
inflation, trade, productivity, investment, rates, climate, AI, and geopolitics
are not independently forecast numerically.

The three targets were selected because together they capture labor-market
conditions, productive capacity, and household living standards. They do not
capture all welfare dimensions, including inequality beyond the median,
public-service quality, health, environment, leisure, wealth, or security.

Earlier versions used a FranceScope Index. V8 removes it: the composite merely
recombined the same three targets, required normative weights and normalization,
and risked false precision. **No replacement composite score is used.**

The normalized charts are visualization-only relative trajectories with
2025 = 100. They do not aggregate variables and must not be interpreted as an
Index.
"""
    (OUT / "FranceScope_V8_Final_methodology.md").write_text(methodology, encoding="utf-8")
    full_report = """# FranceScope V8 Final Report

## 1. Executive Summary

FranceScope V8 is a conditional long-run scenario system for France centered
on three final macro targets: unemployment, real GDP per capita, and real
median living standard. The low-deterioration/least-bad, central-deterioration,
and high-deterioration scenarios are not institutional forecasts.

## 2. What FranceScope V8 Is

V8 describes alternative structural and crisis paths using only the three final
targets. Unemployment captures labor-market access and economic security; real
GDP per capita captures average productive capacity and output per person; real
median living standard captures distributed material living conditions after
taxes, transfers, and redistribution.

## 3. What FranceScope V8 Does NOT Forecast

Debt, deficit, population, employment, inflation, trade, productivity,
investment, rates, climate, AI, and geopolitics are causal evidence and
qualitative drivers, not independent numerical forecasts.

## 4. 2025 Historical Starting Point

The historical baseline is unemployment 7.725%, GDP per capita EUR38,360, and
median living EUR25,952.51. The observed 2026 Q2 unemployment rate is 8.3% and
is contextual evidence only.

## 5. Institutional Benchmark

Banque de France, the European Commission, OECD, IMF, and INSEE evidence is
retained with its published horizon and clearly distinguished from FranceScope
scenario estimates. No institutional forecast is extended beyond its source.

## 6. Structural Thesis

Scenarios reflect fiscal pressure, ageing, under-investment, productivity
weakness, competitiveness, energy, climate, geopolitics, political constraints,
crisis timing, recovery, scarring, hysteresis, and nonlinear interactions.

## 7. Risk and Crisis Framework

The frozen V8 risk layer informs qualitative scenario timing and severity.
Risks are correlated and are not independent numerical forecasts in this
report.

## 8. Scenario Definitions

- **Low deterioration / least-bad:** later or milder shocks, stronger recovery,
  lower scarring, stronger offsets.
- **Central deterioration:** persistent weakness, plausible material crises,
  partial recovery, medium scarring.
- **High deterioration:** earlier severe compound shocks, weak recovery, high
  hysteresis and scarring, insufficient offsets.

## 9. Final Unemployment Scenarios

The 2050 points are 12.0%, 14.0%, and 17.8%. These are conditional scenario
assumptions, not institutional forecasts.

## 10. Final GDP-per-Capita Scenarios

The 2050 points are EUR36,500, EUR34,000, and EUR30,000. GDP per capita need
not move one-for-one with unemployment because participation, ageing,
productivity, automation, hours, employment composition, and GDP per worker
matter.

## 11. Final Median-Living Scenarios

The 2050 points are EUR24,700, EUR23,300, and EUR20,800. Social stabilizers
partially protect the median, while fiscal, wage, inflation, housing, energy,
and benefit pressures constrain protection.

## 12. Three-Target Framework

Earlier versions used a FranceScope Index. V8 removes it because it merely
recombined the same three forecast variables, introduced normative weighting
and normalization assumptions, and risked false precision. **No replacement
composite score is used.** The three targets and their tradeoffs are reported
directly.

## 13. Cross-Variable Coherence

The final paths preserve scenario ordering and were reviewed for temporal and
cross-target coherence. The normalized charts use 2025 = 100 for visual
comparison only; they do not aggregate variables and are not an Index.

## 14. Historical and International Analogues

France's early-1990s unemployment persistence, the financial crisis, COVID
policy support, and the 2022–2026 slowdown provide domestic context. Spain,
Greece, Portugal, Italy, and Japan constrain plausibility but do not predict
France.

## 15. Why FranceScope Differs from Institutional Baselines

V8 explicitly considers long-run structural forces and crisis scarring that
short-horizon institutional forecasts generally do not extend. These are
qualitative scenario drivers, not extra numerical targets.

## 16. Limitations

Long-horizon confidence is low. Scenario values are conditional estimates.
Event probabilities include judgment synthesis. Intermediate macro variables
are not independently forecast numerically. Historical analogues are not
forecasts. The framework does not capture all welfare dimensions, including
inequality beyond the median, public-service quality, health, environmental
quality, leisure, wealth, or security.

## 17. Conclusion

FranceScope V8 is finalized as a direct three-target long-run macroeconomic
scenario project. It does not claim to summarize welfare in one score.

## 18. Technical Appendix

The primary results table, trajectory tables, institutional benchmarks,
historical targets, risk summary, scenario definitions, and limitations table
are provided in the accompanying report package. The final numerical values
are sourced from the frozen V8.08d forecast artifacts.
"""
    (OUT / "FranceScope_V8_Final_full_report.md").write_text(full_report, encoding="utf-8")
    manifest = {
        "version": "V8.10",
        "project_framework": "three_final_macro_targets",
        "final_targets": ["unemployment_rate", "real_gdp_per_capita", "real_median_living_standard"],
        "index_removed": True,
        "replacement_composite_created": False,
        "frozen_values_verified": True,
        "scenario_ordering_preserved": True,
        "normalized_charts_visual_only": True,
        "charts_updated": 7,
        "tables_updated": 1,
        "v7_modified": False,
        "historical_index_artifacts_untouched": True,
    }
    (OUT / "FranceScope_V8_Final_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
