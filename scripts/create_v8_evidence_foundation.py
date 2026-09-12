from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"
MASTER = ROOT / "data" / "processed" / "master_canonical.parquet"
COMPONENTS = ROOT / "data" / "modeling" / "economic_index" / "francescope_components_2010_2026.csv"


def historical_targets() -> pd.DataFrame:
    master = pd.read_parquet(MASTER)
    france = master[master.geo == "FR"].copy()
    years = [2000, 2005, 2010, 2015, 2019, 2022, 2025]
    components = pd.read_csv(COMPONENTS)
    comp = components[components.year == 2025].set_index("variable_id").value
    rows: list[dict[str, object]] = []
    for year in years:
        for target, variable, unit, source in [
            ("unemployment_rate", "unemployment_rate", "%", "Eurostat une_rt_q"),
            (
                "real_gdp_per_capita",
                "real_gdp_per_capita",
                "EUR/person, 2020 chain-linked prices",
                "Eurostat nama_10_pc",
            ),
            (
                "real_median_living_standard",
                "median_living_standard_real",
                "EUR/person/year, constant prices",
                "INSEE ERFS_DNV01",
            ),
        ]:
            values = france[
                (france.variable_id == variable)
                & france.period_start.astype(str).str.startswith(str(year))
            ]
            if target == "unemployment_rate" and not values.empty:
                value = float(values.value.mean())
                status = "OBSERVED"
            elif not values.empty:
                value = float(values.value.mean())
                status = "OBSERVED"
            elif year == 2025 and target == "unemployment_rate":
                value, status = float(comp["unemployment_rate"]), "OBSERVED"
                unit = "%"
                source = "francescope_components_2010_2026.csv"
            elif year == 2025 and target == "real_median_living_standard":
                value, status = float(comp["median_living_standard_real"]), "OBSERVED"
                source = "francescope_components_2010_2026.csv"
            else:
                value, status = "N/A", "UNAVAILABLE"
            rows.append(
                {
                    "target_variable": target,
                    "year": year,
                    "value": value,
                    "unit": unit,
                    "source": source if status != "UNAVAILABLE" else "N/A",
                    "source_date_vintage": "project canonical snapshot; vintage not encoded in series"
                    if status != "UNAVAILABLE"
                    else "N/A",
                    "status": status,
                    "aggregation": "annual mean of quarterly observations"
                    if target == "unemployment_rate" and status != "UNAVAILABLE"
                    else "annual observation",
                }
            )
    return pd.DataFrame(rows)


def institutional_forecasts() -> pd.DataFrame:
    rows = [
        [
            "European Commission",
            "Autumn 2025 Economic Forecast",
            "2025-11",
            "unemployment_rate",
            "2025-2027",
            "2025 7.7%; 2026 8.3%; 2027 8.7%",
            "FORECAST",
            "DIRECT",
            "Short term",
            "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en",
            "Official country forecast; unemployment rate.",
        ],
        [
            "European Commission",
            "Autumn 2025 Economic Forecast",
            "2025-11",
            "real_gdp",
            "2025-2027",
            "GDP growth 2025 0.8%; 2026 0.8%; 2027 1.1%",
            "FORECAST",
            "PROXY",
            "Short term",
            "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en",
            "GDP growth is not converted to GDP per capita without matching population assumptions.",
        ],
        [
            "Banque de France",
            "Macroeconomic projections for France, June 2026",
            "2026-06",
            "unemployment_rate",
            "2026-2028",
            "2026 about 8.1%; 2027 7.6%; 2028 7.4%",
            "FORECAST",
            "DIRECT",
            "Short term",
            "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf",
            "Published unemployment path.",
        ],
        [
            "Banque de France",
            "Macroeconomic projections for France, June 2026",
            "2026-06",
            "real_gdp",
            "2026",
            "GDP growth 0.5%",
            "FORECAST",
            "PROXY",
            "Short term",
            "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf",
            "Proxy only; no per-capita conversion.",
        ],
        [
            "OECD",
            "Economic Outlook, Volume 2025 Issue 2: France",
            "2025-12",
            "real_gdp",
            "2025-2027",
            "GDP growth 2025 0.6%; 2026 0.9%; 2027 1.0%",
            "FORECAST",
            "PROXY",
            "Short term",
            "https://www.oecd.org/en/publications/oecd-economic-outlook-volume-2025-issue-2_9f653ca1-en/full-report/france_9f629187.html",
            "Proxy only; GDP per capita not reported here.",
        ],
        [
            "IMF",
            "France: 2025 Article IV Consultation",
            "2025-07-11",
            "real_gdp",
            "2025-2026",
            "GDP growth 2025 0.6%; 2026 1.0%",
            "FORECAST",
            "PROXY",
            "Short term",
            "https://www.imf.org/en/publications/cr/issues/2025/07/11/france-2025-article-iv-consultation-press-release-staff-report-and-statement-by-the-568520",
            "Proxy only; unemployment detail and per-capita series require annex extraction.",
        ],
        [
            "European Commission",
            "2024 Ageing Report: France country fiche",
            "2024-05",
            "real_gdp",
            "2022-2070",
            "Long-run GDP, employment and productivity projections; exact target values retained in source tables",
            "LONG_RUN_SCENARIO",
            "PROXY",
            "Long term",
            "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf",
            "Conditional ageing assumptions; not a FranceScope target forecast.",
        ],
        [
            "INSEE",
            "Standards of living and poverty / income series",
            "2025-2026",
            "real_median_living_standard",
            "Historical only",
            "No direct long-run institutional forecast found",
            "PROXY",
            "DIRECT",
            "No long-run forecast",
            "https://www.insee.fr/en/statistiques/8608103",
            "Historical benchmark, not a projection.",
        ],
    ]
    columns = [
        "institution",
        "document",
        "publication_date",
        "target_variable",
        "forecast_horizon",
        "forecast_value_or_growth",
        "classification",
        "direct_or_proxy",
        "term",
        "source_url",
        "methodology_note",
    ]
    return pd.DataFrame(rows, columns=columns)


def risks() -> pd.DataFrame:
    structural = [
        (
            "ageing/demography",
            "ageing",
            "Shrinking working-age population raises dependency burden and reduces labor input.",
            "employment and GDP per capita; median living through transfers and household composition",
            "yes",
        ),
        (
            "fiscal deficits",
            "fiscal",
            "Persistent deficits increase financing needs and constrain future policy space.",
            "GDP per capita and median living through taxes, spending and demand",
            "yes",
        ),
        (
            "debt/interest feedback",
            "fiscal",
            "Higher debt and rates raise interest burden and refinancing sensitivity.",
            "all three through fiscal adjustment and demand",
            "yes",
        ),
        (
            "taxation/spending constraints",
            "institutional",
            "Political limits on tax rises or spending cuts delay consolidation.",
            "median living and employment through public services and labor costs",
            "yes",
        ),
        (
            "under-investment",
            "structural",
            "Weak investment lowers future productive capacity.",
            "GDP per capita and median living",
            "yes",
        ),
        (
            "capital weakness",
            "structural",
            "Low capital deepening reduces output per worker.",
            "GDP per capita and employment",
            "yes",
        ),
        (
            "productivity",
            "structural",
            "Slower multifactor or labor productivity limits real income growth.",
            "GDP per capita and median living",
            "yes",
        ),
        (
            "competitiveness",
            "external",
            "Cost and productivity disadvantages reduce export and investment demand.",
            "GDP per capita and employment",
            "yes",
        ),
        (
            "deindustrialisation",
            "structural",
            "Loss of tradable capacity weakens high-productivity employment.",
            "employment and GDP per capita",
            "yes",
        ),
        (
            "education/human capital",
            "structural",
            "Skill mismatch limits productivity and labor reallocation.",
            "employment and GDP per capita",
            "yes",
        ),
        (
            "infrastructure",
            "structural",
            "Infrastructure bottlenecks reduce productivity and resilience.",
            "GDP per capita",
            "yes",
        ),
        (
            "welfare/health burden",
            "structural",
            "Rising health and welfare needs compete with productive spending.",
            "median living and employment",
            "yes",
        ),
        (
            "migration",
            "demography",
            "Migration changes labor supply, population and fiscal balances.",
            "employment and GDP per capita",
            "yes",
        ),
        (
            "political/institutional constraints",
            "institutional",
            "Policy uncertainty delays investment and adjustment.",
            "all three",
            "yes",
        ),
        (
            "structural inflation/energy",
            "structural",
            "Persistent input-cost pressure erodes real household income.",
            "median living and employment",
            "yes",
        ),
        (
            "chronic climate damage",
            "climate",
            "Repeated heat, drought and flood damage reduce output and raise costs.",
            "GDP per capita and median living",
            "yes",
        ),
        (
            "AI/automation",
            "technology",
            "Automation changes task demand, productivity and displacement risk.",
            "employment and GDP per capita",
            "yes",
        ),
        (
            "technology outside AI",
            "technology",
            "Diffusion of general technology affects productivity and competitiveness.",
            "GDP per capita and median living",
            "yes",
        ),
    ]
    events = [
        ("French sovereign/debt crisis"),
        ("refinancing/spread crisis"),
        ("banking/financial crisis"),
        ("euro-area sovereign crisis"),
        ("global recession"),
        ("asset-price crash"),
        ("credit crisis"),
        ("energy shock"),
        ("oil/gas shock"),
        ("major geopolitical conflict"),
        ("trade fragmentation shock"),
        ("major climate/food-price shock"),
        ("domestic political crisis"),
        ("housing/real-estate shock"),
        ("combinations of the above"),
    ]
    rows = [
        {
            "risk_name": n,
            "risk_class": c,
            "mechanism": m,
            "primary_transmission_to_targets": t,
            "persistent_scarring": s,
            "evidence_needed_for_v802": "Historical base rates, official stress scenarios, severity/duration distributions, recovery evidence, and interaction research.",
        }
        for n, c, m, t, s in structural
    ]
    for name in events:
        rows.append(
            {
                "risk_name": name,
                "risk_class": "event/crisis",
                "mechanism": "Discrete adverse shock affecting financing, demand, supply, confidence or external conditions.",
                "primary_transmission_to_targets": "Unemployment through labor demand; GDP per capita through output; median living through real income and prices.",
                "persistent_scarring": "to be researched",
                "evidence_needed_for_v802": "Probability over 2/5/10/25 years; timing, severity, duration, recovery, scarring and interactions.",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    historical = historical_targets()
    historical.to_csv(OUT / "V8_historical_targets.csv", index=False)
    baseline = historical[historical.year == 2025].copy()
    baseline.to_csv(OUT / "V8_2025_baseline.csv", index=False)
    definitions = [
        {
            "target_variable": "unemployment_rate",
            "definition": "ILO/harmonised unemployment rate: unemployed people as a share of the labor force; France age coverage follows the Eurostat series.",
            "annual_aggregation": "mean of quarterly rates",
            "unit": "%",
            "preferred_source": "Eurostat une_rt_q",
            "status": "CANONICAL",
        },
        {
            "target_variable": "real_gdp_per_capita",
            "definition": "Real GDP per person using Eurostat chain-linked volume GDP per capita at 2020 prices.",
            "annual_aggregation": "annual observation",
            "unit": "EUR/person, 2020 chain-linked prices",
            "preferred_source": "Eurostat nama_10_pc",
            "status": "CANONICAL",
        },
        {
            "target_variable": "real_median_living_standard",
            "definition": "FranceScope median living standard, corresponding to INSEE median niveau de vie: equivalised disposable household income per consumption unit, expressed in constant euros.",
            "annual_aggregation": "annual observation",
            "unit": "EUR/person/year, constant prices",
            "preferred_source": "INSEE ERFS_DNV01 / FranceScope canonical series",
            "status": "CANONICAL_WITH_PROJECT_TRANSFORMATION",
        },
    ]
    (OUT / "V8_target_definitions.json").write_text(
        json.dumps(definitions, indent=2), encoding="utf-8"
    )
    pd.DataFrame(definitions).to_csv(OUT / "V8_target_definitions.csv", index=False)
    institutional = institutional_forecasts()
    institutional.to_csv(OUT / "V8_institutional_forecasts.csv", index=False)
    institutional[institutional.forecast_horizon.str.contains("2070|long", case=False)].to_csv(
        OUT / "V8_long_run_evidence.csv", index=False
    )
    sources = [
        [
            "Eurostat",
            "une_rt_q",
            "A",
            "Harmonised unemployment statistics",
            "https://ec.europa.eu/eurostat/databrowser/view/une_rt_q/default/table",
        ],
        [
            "Eurostat",
            "nama_10_pc",
            "A",
            "GDP per capita in chain-linked volumes",
            "https://ec.europa.eu/eurostat/databrowser/view/nama_10_pc/default/table",
        ],
        [
            "INSEE",
            "ERFS_DNV01",
            "A",
            "Median standard of living / income",
            "https://www.insee.fr/en/statistiques/8608103",
        ],
        [
            "European Commission",
            "Autumn 2025 Economic Forecast",
            "A",
            "France short-term forecast",
            "https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en",
        ],
        [
            "Banque de France",
            "Macroeconomic projections June 2026",
            "A",
            "France short-term forecast",
            "https://www.banque-france.fr/system/files/2026-06/Macroeconomic_projections_June_2026.pdf",
        ],
        [
            "OECD",
            "Economic Outlook 2025 Issue 2",
            "A",
            "France short-term GDP growth",
            "https://www.oecd.org/en/publications/oecd-economic-outlook-volume-2025-issue-2_9f653ca1-en/full-report/france_9f629187.html",
        ],
        [
            "IMF",
            "France 2025 Article IV",
            "A",
            "France short-term GDP growth",
            "https://www.imf.org/en/publications/cr/issues/2025/07/11/france-2025-article-iv-consultation-press-release-staff-report-and-statement-by-the-568520",
        ],
        [
            "European Commission",
            "2024 Ageing Report France country fiche",
            "A",
            "Conditional long-run demographic/economic scenario",
            "https://economy-finance.ec.europa.eu/document/download/e412927a-ea31-406d-bb6c-c925914123e9_en?filename=2024-ageing-report-country-fiche-France.pdf",
        ],
    ]
    pd.DataFrame(
        sources, columns=["source", "document_or_series", "quality_grade", "use", "url"]
    ).to_csv(OUT / "V8_source_registry.csv", index=False)
    risk_df = risks()
    risk_df.to_csv(OUT / "V8_risk_taxonomy.csv", index=False)
    queue = [
        {
            "risk_name": r,
            "horizon": h,
            "dimensions_to_research": "probability; timing; severity; duration; recovery; scarring; interaction",
        }
        for r in risk_df[risk_df.risk_class == "event/crisis"].risk_name
        for h in ["2 years", "5 years", "10 years", "25 years"]
    ]
    pd.DataFrame(queue).to_csv(OUT / "V8_crisis_research_queue.csv", index=False)
    methodology = """# FranceScope V8.01 Evidence Foundation

## Status and forecasting philosophy

V7 is preserved exploratory causal/modeling work. V8 is the final forecasting
framework under development. V8 has exactly three numerical forecast targets:
unemployment rate, real GDP per capita, and real median living standard.
Debt, investment, demographics, productivity, climate, energy, geopolitics and
financial conditions are causal evidence and scenario drivers, not independent
numerical endpoints.

Structural trends are persistent forces such as ageing, productivity and fiscal
constraints. Crisis/event risks are discrete shocks. Future scenarios will
differ by timing, severity, persistence, interaction, recovery and scarring.
They are not “optimistic = no crises, central = one crisis, pessimistic = many
crises”; all scenarios share structural deterioration pressures.

## Time status and definitions

2025 values are historical canonical observations where marked OBSERVED.
2026 is not used as a historical substitute. V7 bridge values are excluded.
The target definitions and historical coverage are in the accompanying CSV and
JSON files. Annual unemployment is the mean of quarterly harmonised rates.
GDP per capita uses Eurostat chain-linked 2020-price volume GDP per person.
Real median living standard is the FranceScope implementation of INSEE median
*niveau de vie*: equivalised disposable household income per consumption unit
in constant euros. The exact project transformation should be re-confirmed
before V8.02.

## Institutional evidence

Short-run official forecasts exist for GDP growth and unemployment from the
European Commission, Banque de France, OECD and IMF. They are retained with
their published horizons and are not extended. The 2024 European Commission
Ageing Report supplies a conditional long-run scenario through 2070, mainly for
demography, employment and GDP; it is a proxy, not a direct V8 target forecast.
No direct long-run institutional forecast for French median living standard was
found: `NO_DIRECT_LONG_RUN_INSTITUTIONAL_FORECAST_FOUND`.

## V7 preservation

V7 may inform causal intuition, historical data, mechanism maps, definitions
and stress-test ideas. V7 P10/P50/P90 values do not automatically become V8
forecasts, and no V8 scenario numbers are selected in V8.01.

## Evidence hierarchy

A = primary official statistical source or official projection; B = peer-reviewed
or institutional research; C = market-implied/private research; D = expert
judgment or historical analogy; E = speculative. Every source used here is
graded A.
"""
    (OUT / "V8_methodology.md").write_text(methodology, encoding="utf-8")


if __name__ == "__main__":
    main()
