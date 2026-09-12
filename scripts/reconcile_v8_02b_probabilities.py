from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parents[1]
OUT = ROOT / "data" / "research" / "v8"
SOURCE = OUT / "V8_crisis_probability_estimates.csv"
FINAL = OUT / "V8_crisis_probability_estimates_final.csv"


def main() -> None:
    raw = pd.read_csv(SOURCE)
    raw["risk"] = raw["risk"].replace({"material sovereign stress": "French sovereign/debt crisis"})
    original_low = raw["probability_low"].copy()
    original_high = raw["probability_high"].copy()
    raw["probability_low"] = pd.concat([original_low, original_high], axis=1).min(axis=1)
    raw["probability_high"] = pd.concat([original_low, original_high], axis=1).max(axis=1)
    raw["probability_central"] = raw["central_estimate"]
    raw["source_basis"] = raw["main_sources"] + "; " + raw["estimate_basis"]
    raw["judgment_flag"] = "JUDGMENT_SYNTHESIS"
    final = raw[
        [
            "risk", "definition", "horizon", "probability_low",
            "probability_central", "probability_high", "confidence",
            "evidence_grade", "source_basis", "judgment_flag",
        ]
    ].copy()
    final.to_csv(FINAL, index=False)

    horizon_order = {"2y": 0, "5y": 1, "10y": 2, "25y": 3}
    violations = []
    range_violations = []
    duplicate_rows = int(final.duplicated(["risk", "horizon"]).sum())
    for risk, group in final.groupby("risk"):
        ordered = group.assign(_order=group.horizon.map(horizon_order)).sort_values("_order")
        for field in ["probability_low", "probability_central", "probability_high"]:
            values = ordered[field].tolist()
            if any(values[i] > values[i + 1] for i in range(len(values) - 1)):
                violations.append({"risk": risk, "field": field, "values": values})
        for _, row in ordered.iterrows():
            if not row.probability_low <= row.probability_central <= row.probability_high:
                range_violations.append({"risk": risk, "horizon": row.horizon})
    ranking = (
        final[final.horizon == "25y"]
        .sort_values("probability_central", ascending=False)
        .reset_index(drop=True)
    )
    ranking.insert(0, "rank", ranking.index + 1)
    ranking = ranking[
        ["rank", "risk", "probability_low", "probability_central",
         "probability_high", "confidence", "evidence_grade"]
    ]
    ranking.to_csv(OUT / "V8_02b_top_25y_ranking.csv", index=False)
    report = """# V8.02b Probability Consistency Reconciliation

## Contradictions found

The underlying `V8_crisis_probability_estimates.csv` had the two range tuples
reversed during generation: the first tuple was written as `probability_low`
and the second as `probability_high`, although the first was numerically larger
for each risk. This caused lower bounds to exceed upper bounds. The central
estimate was the midpoint and was therefore retained.

The previous prose summary also transcribed some ranges inconsistently
(notably global recession and banking/financial crisis). Those were summary
errors. The range inversion was an underlying-data error.

## Corrections

`V8_crisis_probability_estimates_final.csv` swaps the affected lower and upper
semantics, retains every central estimate, standardizes the exact probability
field names, and labels all values `JUDGMENT_SYNTHESIS`. Probabilities are
cumulative probabilities of at least one qualifying event within the horizon.
The original research artifact remains unchanged.

The sovereign concepts remain separate: material French sovereign/debt stress,
severe funding/refinancing crisis, and formal default/restructuring. These are
not collapsed into a single default probability.

Global recession means at least one qualifying global recession, not a French
recession, ordinary slowdown, or equity bear market. Banking crisis, asset-price
crash and credit crisis remain separate but correlated risks and must not be
treated as independent in V8.03.

## Final ranking

The authoritative ranking is in `V8_02b_top_25y_ranking.csv` and is calculated
directly from 25-year central estimates in the final table.

## Sovereign-default language

“France will default within 25 years” remains **NOT_SUPPORTED / TOO_STRONG**.
The defensible wording is that France faces material long-run sovereign funding
stress risk, while formal default or restructuring remains a low-probability
tail event.
"""
    (OUT / "V8_02b_consistency_report.md").write_text(report, encoding="utf-8")
    manifest = {
        "source_rows": len(raw),
        "final_rows": len(final),
        "risk_count": int(final.risk.nunique()),
        "duplicate_risk_horizon_rows": duplicate_rows,
        "horizon_monotonicity_violations": len(violations),
        "range_violations": len(range_violations),
        "judgment_flags_complete": bool((final.judgment_flag == "JUDGMENT_SYNTHESIS").all()),
        "v8_target_forecasts_selected": False,
        "formal_default_certain": False,
    }
    (OUT / "V8_02b_consistency_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if violations or range_violations or duplicate_rows:
        raise RuntimeError(f"Consistency validation failed: {manifest}")


if __name__ == "__main__":
    main()
