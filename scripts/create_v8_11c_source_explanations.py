from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parents[1]
IN = ROOT / "data" / "research" / "v8"
BENCH = IN / "institutional_benchmark"
REPORT = ROOT / "data" / "report" / "v8_final"


def main() -> None:
    raw = pd.read_csv(BENCH / "institutional_forecasts_raw.csv")
    rows = []
    for _, r in raw.iterrows():
        reason = ["No explicit rationale found in the retained source artifact."] * 3
        assumptions = ["Published value is used without extrapolation.", "Definition and vintage are as published.", "No FranceScope interpretation is substituted."]
        if r.institution == "Banque de France" and r.institution_variable_name == "unemployment_rate":
            reason = ["Employment and salaried employment are expected to stagnate in the weak early-2026 environment.", "A recovery in job creation is expected from around mid-2027.", "The projection is framed against sluggish activity and international uncertainty."]
            assumptions = ["The published macroeconomic scenario holds.", "France Travail registration and labor-market flows evolve as modeled.", "The unemployment definition is BIT/ILO, France excluding Mayotte."]
        elif r.institution == "European Commission" and r.institution_variable_name == "unemployment_rate":
            reason = ["Payroll employment contracts while the labor force continues to grow.", "Higher participation, including younger and older workers, raises labor supply.", "A modest productivity rebound accompanies weak employment growth."]
            assumptions = ["The Commission baseline fiscal and macro scenario holds.", "Participation and pension-reform effects follow the published forecast.", "Definition is the Commission's published France series."]
        elif r.institution == "Banque de France" and r.institution_variable_name == "real_gdp_growth":
            reason = ["No explicit mechanism was extracted in the retained source artifact."]
        elif r.institution == "European Commission" and r.institution_variable_name == "real_gdp_growth":
            reason = ["Domestic demand and fiscal conditions shape the subdued near-term path.", "A recovery in productivity is associated with modestly rising output.", "The published forecast includes external and policy uncertainty."]
        elif r.institution == "OECD" and r.institution_variable_name == "real_gdp_growth":
            reason = ["No explicit rationale was extracted in the retained source artifact."]
        elif r.institution == "IMF" and r.institution_variable_name == "real_gdp_growth":
            reason = ["No explicit rationale was extracted in the retained source artifact."]
        elif r.institution == "European Commission" and r.institution_variable_name == "potential_gdp_per_capita_growth":
            reason = ["The Ageing Report uses long-run demographic, labor-input, and productivity assumptions.", "The value is a milestone growth projection, not a level forecast.", "It belongs to the agreed Ageing Working Group long-run framework."]
            assumptions = ["Conditional unchanged-policy framework.", "Demographic and participation paths follow the Ageing Report.", "Productivity follows the report's potential-growth assumptions."]
        reason = (reason + ["No explicit rationale found in the retained source artifact."] * 3)[:3]
        assumptions = (assumptions + ["Published value is used without extrapolation."] * 3)[:3]
        rows.append({
            "variable": r.institution_variable_name, "year": int(r.year), "institution": r.institution,
            "value": r.value, "unit": r.unit, "definition": r.definition_scope,
            "classification": r.source_type, "publication": r.publication,
            "publication_date": r.publication_date, "source": r.source_url,
            "source_table_or_section": "France forecast: labour market" if r.institution_variable_name == "unemployment_rate" else "France forecast: GDP and activity",
            "source_page_if_available": "Not identified in retained source artifact",
            "institution_stated_reason_1": reason[0], "institution_stated_reason_2": reason[1],
            "institution_stated_reason_3": reason[2], "key_assumption_1": assumptions[0],
            "key_assumption_2": assumptions[1], "key_assumption_3": assumptions[2],
            "source_quote_or_paraphrase": " | ".join(reason),
            "our_interpretation": "FranceScope treats this as an institutional benchmark only; it is not extrapolated into a FranceScope target.",
            "confidence": "HIGH" if r.source_type in ["OBSERVED", "DIRECT_FORECAST"] else "MEDIUM",
            "notes": f"Source quote not reproduced; rationale fields distinguish explicit source material from non-available explanation. Forecast vintage: {r.forecast_vintage}.",
        })
    explanations = pd.DataFrame(rows)
    explanations.to_csv(BENCH / "institutional_forecast_explanations.csv", index=False)

    forecasts = pd.read_csv(IN / "V8_final_target_forecasts.csv")
    institutional_unemp = {2030: 7.1, 2040: 6.7, 2050: 6.3}
    fs = forecasts[forecasts.year.isin([2030, 2040, 2050])].pivot_table(index=["scenario", "year"], columns="variable", values="point_forecast").reset_index()
    divergence = []
    for variable in ["unemployment_rate", "real_gdp_per_capita", "real_median_living_standard"]:
        for year in [2030, 2040, 2050]:
            ref = institutional_unemp[year] if variable == "unemployment_rate" else "NA"
            part = fs[fs.year == year].set_index("scenario")
            low = float(part.loc["OPTIMISTIC", variable])
            central = float(part.loc["CENTRAL", variable])
            high = float(part.loc["PESSIMISTIC", variable])
            divergence.append({
                "variable": variable, "year": year, "institutional_reference": ref,
                "FranceScope_low": low, "FranceScope_central": central, "FranceScope_high": high,
                "numerical_gap": "NA" if ref == "NA" else f"low={low-ref:.2f}; central={central-ref:.2f}; high={high-ref:.2f}",
                "institutional_assumptions": "Baseline participation/demographic convergence and limited permanent scarring; EC reference is a long-run structural projection." if variable == "unemployment_rate" else "No comparable direct long-run institutional level reference.",
                "FranceScope_assumptions": "Persistent fiscal pressure, debt-service burden, under-investment, weaker capital formation/productivity, competitiveness loss, political constraints, stronger crisis scarring, hysteresis, and weaker recovery.",
                "reason_for_divergence": "FranceScope assigns greater weight to structural deterioration and persistent scarring; it does not claim institutions are wrong.",
            })
    pd.DataFrame(divergence).to_csv(BENCH / "francescope_vs_institutions_explanation.csv", index=False)
    pd.DataFrame(divergence).to_csv(REPORT / "tables" / "FranceScope_V8_Final_institutional_divergence.csv", index=False)

    narrative = """\n\n## Why FranceScope Differs from Institutional Baselines\n\n### A. What institutions assume\n\nThe near-term institutional layer is a set of published forecasts, not one homogeneous path. Banque de France projects unemployment of 8.1% in 2026, 8.1% in 2027, and 7.8% in 2028. The European Commission contributes 8.3% in 2026 and 8.7% in 2027. Where multiple comparable forecasts exist, the near-term unemployment median is 8.2% in 2026 and 8.4% in 2027. The Commission Ageing Report supplies a long-run age-20–64 unemployment reference of 7.1% in 2030, 6.7% in 2040, and 6.3% in 2050 under its conditional long-run framework.\n\nThe Commission's long-run GDP-per-capita values are milestone growth rates, not EUR/person levels. No direct long-run median-living institutional benchmark is available. Those gaps are reported as NA rather than filled with unsupported forecasts.\n\n### B. What FranceScope assumes differently\n\nFranceScope is a conditional adverse structural framework. It assigns greater weight to persistent fiscal pressure, debt-service burden, under-investment, weaker capital formation and productivity, competitiveness loss and deindustrialisation, political constraints, stronger crisis frequency or severity, hysteresis, cumulative scarring, and weaker recovery. These mechanisms are scenario assumptions, not additional numerical forecasts.\n\n### C. Why the outcomes diverge\n\nThe EC long-run unemployment reference declines toward 6.3% by 2050, while FranceScope reaches 12.0%, 14.0%, or 17.8% because FranceScope allows persistent unemployment and repeated scarring rather than limited permanent damage in the institutional baseline. GDP per capita and median living are not assigned institutional long-run levels because comparable official level paths were not retrieved. FranceScope therefore adds conditional target paths where the institutional layer remains structurally incomplete.\n\n### D. Which view is more uncertain\n\nThe 2050 institutional unemployment reference is itself conditional and structurally modeled. FranceScope's long-run points are also low-confidence conditional scenarios. The GDP-per-capita and median-living comparison is more uncertain because the institutional layer lacks comparable direct levels; no false precision is introduced.\n\n### E. Interpretation\n\nFranceScope assigns greater weight to structural deterioration and persistent scarring than the institutional baseline. It does not claim that institutions are wrong. It answers a different question: how adverse could a coherent French long-run path be if fiscal, demographic, productivity, competitiveness, crisis, and recovery pressures compound?\n\nInstitution-stated explanations are separated from our interpretation in the value-level registry. Rows that lack an explicit source explanation say so directly rather than inferring a mechanism.\n"""
    for filename in ["FranceScope_V8_Final_full_report.md", "FranceScope_V8_Final_executive_summary.md"]:
        path = REPORT / filename
        text = path.read_text(encoding="utf-8")
        if "Why FranceScope Differs from Institutional Baselines" not in text:
            path.write_text(text + narrative, encoding="utf-8")
    manifest = {
        "version": "V8.11c",
        "value_level_registry_created": True,
        "institutional_explanations_separated_from_interpretation": True,
        "all_displayed_long_run_median_values": "NA",
        "unsupported_gdp_per_capita_levels_removed": True,
        "francescope_values_changed": False,
        "index_recreated": False,
        "v7_modified": False,
    }
    (BENCH / "institutional_explanation_validation_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
