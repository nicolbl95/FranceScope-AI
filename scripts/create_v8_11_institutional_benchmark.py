from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).parents[1]
IN = ROOT / "data" / "research" / "v8"
REPORT = ROOT / "data" / "report" / "v8_final"
OUT = IN / "institutional_benchmark"
CHARTS = REPORT / "charts"
SCENARIOS = ["OPTIMISTIC", "CENTRAL", "PESSIMISTIC"]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    forecasts = pd.read_csv(IN / "V8_final_target_forecasts.csv")
    baseline = forecasts[forecasts.year == 2025].set_index("variable").point_forecast
    frozen = {
        ("unemployment_rate", "OPTIMISTIC", 2030): 8.5,
        ("unemployment_rate", "CENTRAL", 2050): 14.0,
        ("real_gdp_per_capita", "PESSIMISTIC", 2050): 30000.0,
        ("real_median_living_standard", "CENTRAL", 2050): 23300.0,
    }
    for (variable, scenario, year), value in frozen.items():
        actual = forecasts[(forecasts.variable == variable) & (forecasts.scenario == scenario) & (forecasts.year == year)].point_forecast.iloc[0]
        if float(actual) != value:
            raise RuntimeError("FranceScope frozen value mismatch.")

    raw = pd.DataFrame([
        ["Banque de France", "Macroeconomic projections for France, June 2026", "2026-06", "unemployment_rate", 2026, 8.1, "%", "BIT/ILO; France excluding Mayotte", "DIRECT_FORECAST", "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf"],
        ["Banque de France", "Macroeconomic projections for France, June 2026", "2026-06", "unemployment_rate", 2027, 8.1, "%", "BIT/ILO; France excluding Mayotte", "DIRECT_FORECAST", "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf"],
        ["Banque de France", "Macroeconomic projections for France, June 2026", "2026-06", "unemployment_rate", 2028, 7.8, "%", "BIT/ILO; France excluding Mayotte", "DIRECT_FORECAST", "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf"],
        ["European Commission", "Autumn 2025 Economic Forecast", "2025-11", "unemployment_rate", 2026, 8.3, "%", "France; definition as published", "DIRECT_FORECAST", "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en"],
        ["European Commission", "Autumn 2025 Economic Forecast", "2025-11", "unemployment_rate", 2027, 8.7, "%", "France; definition as published", "DIRECT_FORECAST", "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en"],
        ["Banque de France", "Macroeconomic projections for France, June 2026", "2026-06", "real_gdp_growth", 2026, 0.5, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf"],
        ["Banque de France", "Macroeconomic projections for France, June 2026", "2026-06", "real_gdp_growth", 2027, 0.9, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf"],
        ["Banque de France", "Macroeconomic projections for France, June 2026", "2026-06", "real_gdp_growth", 2028, 1.2, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf"],
        ["European Commission", "2024 Ageing Report: France country fiche", "2024-05", "unemployment_rate_20_64", 2030, 7.1, "%", "Age 20-64; France", "LONG_RUN_PROJECTION", "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf"],
        ["European Commission", "2024 Ageing Report: France country fiche", "2024-05", "unemployment_rate_20_64", 2040, 6.7, "%", "Age 20-64; France", "LONG_RUN_PROJECTION", "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf"],
        ["European Commission", "2024 Ageing Report: France country fiche", "2024-05", "unemployment_rate_20_64", 2050, 6.3, "%", "Age 20-64; France", "LONG_RUN_PROJECTION", "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf"],
        ["European Commission", "2024 Ageing Report: France country fiche", "2024-05", "potential_gdp_per_capita_growth", 2030, 0.4, "% annual", "Potential GDP per capita growth; France", "LONG_RUN_PROJECTION", "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf"],
        ["European Commission", "2024 Ageing Report: France country fiche", "2024-05", "potential_gdp_per_capita_growth", 2040, 1.4, "% annual", "Potential GDP per capita growth; France", "LONG_RUN_PROJECTION", "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf"],
        ["European Commission", "2024 Ageing Report: France country fiche", "2024-05", "potential_gdp_per_capita_growth", 2050, 1.4, "% annual", "Potential GDP per capita growth; France", "LONG_RUN_PROJECTION", "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf"],
        ["European Commission", "Autumn 2025 Economic Forecast", "2025-11", "real_gdp_growth", 2026, 0.8, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en"],
        ["European Commission", "Autumn 2025 Economic Forecast", "2025-11", "real_gdp_growth", 2027, 1.1, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en"],
        ["OECD", "Economic Outlook, Volume 2025 Issue 2: France", "2025-12", "real_gdp_growth", 2026, 0.9, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://www.oecd.org/en/publications/oecd-economic-outlook-volume-2025-issue-2_9f653ca1-en/full-report/france_9f629187.html"],
        ["OECD", "Economic Outlook, Volume 2025 Issue 2: France", "2025-12", "real_gdp_growth", 2027, 1.0, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://www.oecd.org/en/publications/oecd-economic-outlook-volume-2025-issue-2_9f653ca1-en/full-report/france_9f629187.html"],
        ["IMF", "France 2025 Article IV Consultation", "2025-07-11", "real_gdp_growth", 2026, 1.0, "% annual", "Aggregate GDP growth; France", "DIRECT_FORECAST", "https://www.imf.org/en/publications/cr/issues/2025/07/11/france-2025-article-iv-consultation-press-release-staff-report-and-statement-by-the-568520"],
        ["INSEE", "Standards of living and poverty / income series", "2025-2026", "real_median_living_standard", 2025, 25952.514017, "EUR/person/year", "Historical INSEE-compatible concept", "OBSERVED", "https://www.insee.fr/en/statistiques/8608103"],
    ], columns=["institution", "publication", "publication_date", "institution_variable_name", "year", "value", "unit", "definition_scope", "source_type", "source_url"])
    raw["forecast_vintage"] = raw.publication_date
    raw["price_basis"] = raw.unit.map(lambda x: "2020 chain-linked prices" if "GDP" in x or "GDP" in str(x) else "constant-price project series")
    raw.to_csv(OUT / "institutional_forecasts_raw.csv", index=False)

    normalized = raw.copy()
    normalized["target_variable"] = normalized.institution_variable_name.map({
        "unemployment_rate_20_64": "unemployment_rate",
        "potential_gdp_per_capita_growth": "real_gdp_per_capita_growth",
        "real_gdp_growth": "real_gdp_growth",
        "real_median_living_standard": "real_median_living_standard",
        "unemployment_rate": "unemployment_rate",
    })
    normalized["classification"] = normalized.source_type
    normalized.to_csv(OUT / "institutional_forecasts_normalized.csv", index=False)

    consensus_rows = []
    for variable in ["unemployment_rate", "real_gdp_growth"]:
        group = normalized[normalized.target_variable == variable]
        for year, values in group.groupby("year").value:
            if len(values) >= 2:
                consensus_rows.append({
                    "target_variable": variable, "year": year, "institution_count": len(values),
                    "mean": values.mean(), "median": values.median(), "min": values.min(),
                    "max": values.max(), "standard_deviation": values.std(ddof=0),
                    "classification": "NEAR_TERM_INSTITUTIONAL_CONSENSUS",
                })
    pd.DataFrame(consensus_rows).to_csv(OUT / "institutional_near_term_consensus.csv", index=False)

    years = [2025, 2026, 2027, 2028, 2030, 2040, 2050]
    long_rows = []
    for year, value, source, classification, confidence in [
        (2025, float(baseline["unemployment_rate"]), "Eurostat une_rt_q / project canonical snapshot", "OBSERVED", "HIGH"),
        (2026, 8.1, "Banque de France June 2026", "DIRECT_FORECAST", "HIGH"),
        (2027, 8.1, "Banque de France June 2026", "DIRECT_FORECAST", "HIGH"),
        (2028, 7.8, "Banque de France June 2026", "DIRECT_FORECAST", "HIGH"),
        (2030, 7.1, "European Commission 2024 Ageing Report, age 20-64", "LONG_RUN_PROJECTION", "MEDIUM"),
        (2040, 6.7, "European Commission 2024 Ageing Report, age 20-64", "LONG_RUN_PROJECTION", "MEDIUM"),
        (2050, 6.3, "European Commission 2024 Ageing Report, age 20-64", "LONG_RUN_PROJECTION", "MEDIUM"),
    ]:
        long_rows.append(["unemployment_rate", year, value, "%", source, classification, confidence, "Direct short-run forecast or age-20-64 structural projection; definitions are not identical across horizons."])
    long_rows.extend([
        ["real_gdp_per_capita", 2025, float(baseline["real_gdp_per_capita"]), "EUR/person, 2020 chain-linked prices", "Eurostat nama_10_pc / project canonical snapshot", "OBSERVED", "HIGH", "Historical 2025 actual."],
        ["real_median_living_standard", 2025, float(baseline["real_median_living_standard"]), "EUR/person/year, constant prices", "INSEE-compatible project canonical snapshot", "OBSERVED", "HIGH", "Historical 2025 actual."],
    ])
    for year, growth in [(2030, 0.4), (2040, 1.4), (2050, 1.4)]:
        long_rows.append(["real_gdp_per_capita_growth", year, growth, "% annual", "European Commission 2024 Ageing Report potential GDP per capita growth milestone", "LONG_RUN_PROJECTION", "MEDIUM", "Growth milestone only; not converted into a level because the source does not establish a constant rate over the intervening interval."])
    long_reference = pd.DataFrame(long_rows, columns=["target_variable", "year", "value", "unit", "source_basis", "classification", "confidence", "notes"])
    long_reference.to_csv(OUT / "institutional_long_run_reference.csv", index=False)

    benchmark = long_reference.copy()
    benchmark["scenario"] = "INSTITUTIONAL_REFERENCE"
    benchmark["source_basis"] = benchmark.source_basis
    benchmark.to_csv(OUT / "institutional_three_target_benchmark.csv", index=False)
    pd.DataFrame([
        ["Banque de France", "Macroeconomic projections June 2026", "2026-06", "DIRECT_FORECAST", "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf"],
        ["European Commission", "2024 Ageing Report France country fiche", "2024-05", "LONG_RUN_PROJECTION", "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf"],
        ["European Commission", "Autumn 2025 Economic Forecast", "2025-11", "DIRECT_FORECAST", "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en"],
        ["OECD", "Economic Outlook Volume 2025 Issue 2", "2025-12", "DIRECT_FORECAST", "https://www.oecd.org/en/publications/oecd-economic-outlook-volume-2025-issue-2_9f653ca1-en/full-report/france_9f629187.html"],
        ["IMF", "France 2025 Article IV Consultation", "2025-07-11", "DIRECT_FORECAST", "https://www.imf.org/en/publications/cr/issues/2025/07/11/france-2025-article-iv-consultation-press-release-staff-report-and-statement-by-the-568520"],
        ["INSEE", "Standards of living and poverty / income series", "2025-2026", "OBSERVED", "https://www.insee.fr/en/statistiques/8608103"],
    ], columns=["institution", "publication", "publication_date", "source_type", "source_url"]).to_csv(OUT / "institutional_source_registry.csv", index=False)

    proxy = pd.DataFrame([
        ["real_median_living_standard", 2030, 26475.733342, "EUR/person/year, constant prices", "ILLUSTRATIVE_INSTITUTIONAL_CONSISTENT_PROXY", "LOW", "Not part of the institutional reference; retained only to illustrate a fixed-2025-ratio transformation."],
        ["real_median_living_standard", 2040, 30424.787128, "EUR/person/year, constant prices", "ILLUSTRATIVE_INSTITUTIONAL_CONSISTENT_PROXY", "LOW", "Not part of the institutional reference; retained only to illustrate a fixed-2025-ratio transformation."],
        ["real_median_living_standard", 2050, 34962.871842, "EUR/person/year, constant prices", "ILLUSTRATIVE_INSTITUTIONAL_CONSISTENT_PROXY", "LOW", "Not part of the institutional reference; retained only to illustrate a fixed-2025-ratio transformation."],
    ], columns=["target_variable", "year", "value", "unit", "classification", "confidence", "notes"])
    proxy.to_csv(OUT / "illustrative_median_living_proxy.csv", index=False)

    methodology = """# Institutional Benchmark Methodology

The institutional benchmark is a reference alongside, not a fourth FranceScope
scenario. Direct short-run forecasts are retained only at their published
horizons. The Commission Ageing Report is treated as a long-run structural
projection, not a conventional forecast.

Unemployment uses Banque de France direct forecasts for 2026–2028 and the
Commission's age-20–64 long-run projection for 2030–2050. These definitions
are documented and not silently treated as identical.

No comparable direct long-run GDP-per-capita level forecast was found in the
retrievable evidence. The Commission milestone growth values are retained as
growth rates only. They are not treated as constant rates over a decade and are
not converted into benchmark EUR/person levels.

No comparable direct long-run median-living forecast was found. The final
institutional benchmark is therefore NA for median living after 2025. A
separate illustrative_median_living_proxy.csv is retained only as an optional
illustration and is not part of the benchmark or consensus.

The near-term consensus table is calculated only where at least two comparable
institutional observations exist. Aggregate GDP growth is not averaged with
GDP-per-capita growth or converted into a level without an explicit proxy flag.
"""
    (OUT / "institutional_benchmark_methodology.md").write_text(methodology, encoding="utf-8")

    comparison = []
    fs = forecasts[forecasts.year.isin([2030, 2040, 2050])].pivot_table(index=["scenario", "year"], columns="variable", values="point_forecast").reset_index()
    for _, row in long_reference[(long_reference.year.isin([2030, 2040, 2050])) & (long_reference.target_variable.isin(["unemployment_rate", "real_gdp_per_capita"]))].iterrows():
        comparison.append({"source": "INSTITUTIONAL_REFERENCE", "scenario": "INSTITUTIONAL_REFERENCE", "year": int(row.year), "variable": row.target_variable, "value": row.value, "classification": row.classification})
    for _, row in fs.iterrows():
        label = row.scenario
        for variable in ["unemployment_rate", "real_gdp_per_capita", "real_median_living_standard"]:
            comparison.append({"source": "FRANCESCOPE", "scenario": label, "year": int(row.year), "variable": variable, "value": row[variable], "classification": "CONDITIONAL_SCENARIO"})
    comparison_df = pd.DataFrame(comparison)
    comparison_df.to_csv(REPORT / "tables" / "FranceScope_V8_Final_institutional_comparison.csv", index=False)

    for variable, title, ylabel in [
        ("unemployment_rate", "Unemployment: historical, institutional reference, FranceScope", "Unemployment rate (%)"),
        ("real_gdp_per_capita", "Real GDP per capita: FranceScope (no direct long-run institutional level)", "EUR/person"),
        ("real_median_living_standard", "Median living: FranceScope (no direct long-run institutional benchmark)", "EUR/person/year"),
    ]:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        historical = IN / "V8_historical_targets.csv"
        hist = pd.read_csv(historical)
        hist = hist[hist.target_variable == variable]
        hist = hist[hist.status == "OBSERVED"]
        if not hist.empty:
            ax.plot(hist.year, hist.value, color="black", marker="o", label="Historical")
        inst = long_reference[long_reference.target_variable == variable]
        if not inst.empty:
            ax.plot(inst.year, inst.value, color="tab:blue", marker="o", label="Institutional reference")
        for scenario, color in zip(SCENARIOS, ["tab:green", "tab:orange", "tab:red"]):
            part = forecasts[(forecasts.variable == variable) & (forecasts.scenario == scenario)]
            ax.plot([2025] + part.year.tolist(), [float(baseline[variable])] + part.point_forecast.tolist(), marker="o", color=color, label=f"FranceScope {scenario.lower()}")
        ax.set(title=title, xlabel="Year", ylabel=ylabel)
        ax.grid(alpha=0.25); ax.legend(fontsize=7); fig.tight_layout()
        fig.savefig(CHARTS / f"FranceScope_V8_Final_institutional_{variable}.png", dpi=160)
        plt.close(fig)

    report_addition = """\n\n## Institutional Reference Benchmark\n\nThe institutional reference is shown alongside, not as a fourth FranceScope scenario. Direct Banque de France short-run unemployment forecasts are used for 2026–2028, with European Commission unemployment observations added where comparable for a genuine near-term consensus. The European Commission 2024 Ageing Report supplies a long-run age-20–64 unemployment projection for 2030–2050. Its GDP-per-capita milestone growth rates are retained as rates only; no unsupported EUR/person level path is presented. No comparable direct long-run median-living forecast was found, so the final institutional benchmark is NA for median living after 2025. An optional illustrative fixed-ratio proxy is stored separately and is not an institutional forecast or consensus. Institutional forecasts, long-run projections, and illustrative proxies are never presented as one homogeneous forecast.\n\nThe institutional reference is generally less adverse than the FranceScope high-deterioration path because FranceScope conditionally incorporates stronger structural fiscal, demographic, productivity, crisis-scarring, and hysteresis pressures. The comparison does not imply that the institutional reference is a probability-weighted consensus through 2050.\n"""
    for filename in ["FranceScope_V8_Final_full_report.md", "FranceScope_V8_Final_executive_summary.md"]:
        path = REPORT / filename
        text = path.read_text(encoding="utf-8")
        if "Institutional Reference Benchmark" not in text:
            path.write_text(text + report_addition, encoding="utf-8")

    manifest = {
        "version": "V8.11",
        "francescope_values_unchanged": True,
        "direct_short_term_forecasts_not_extrapolated": True,
        "long_run_gdp_levels_are_derived_proxy": False,
        "long_run_median_direct_forecast_found": False,
        "median_proxy_labeled": True,
        "long_run_median_benchmark_status": "NA",
        "oecd_numeric_dataset_retrieved": False,
        "incompatible_units_averaged": False,
        "near_term_consensus_requires_two_sources": True,
        "institutional_charts_created": 3,
        "index_recreated": False,
        "v7_modified": False,
    }
    (OUT / "institutional_benchmark_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
