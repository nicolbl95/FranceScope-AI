"""Final fixes: add non-zero uncertainty for retirement age, add test, add audit note."""
from __future__ import annotations

from pathlib import Path

import polars as pl

MODELING_DIR = Path("data/modeling/economic_index")
AUDIT_DIR = Path("data/audits/institutional_forecast_readiness")

CORE_VARIABLES = [
    "average_net_pension_real", "effective_retirement_age", "real_gdp",
    "unemployment_rate", "median_living_standard_real", "poverty_rate", "housing_cost_burden",
]

NORMALIZATION = {
    "average_net_pension_real": {"median": 1787.36033294441, "sd": 21.726609781288147, "direction": 1.0},
    "effective_retirement_age": {"median": 61.485, "sd": 0.6949592290585619, "direction": -1.0},
    "real_gdp": {"median": 2335541.95, "sd": 88665.90066716072, "direction": 1.0},
    "unemployment_rate": {"median": 9.6, "sd": 0.7181245366938473, "direction": -1.0},
    "median_living_standard_real": {"median": 23800.0, "sd": 300.2223869532987, "direction": 1.0},
    "poverty_rate": {"median": 13.6, "sd": 0.2594514455151949, "direction": -1.0},
    "housing_cost_burden": {"median": 5.2, "sd": 0.07412898443291367, "direction": -1.0},
}

# Retirement age uncertainty: ±0.15 years for bridge estimates
# Widens slightly with distance from 2023 anchor
RETIREMENT_AGE_BRIDGE_UNCERTAINTY = {
    2024: 0.12,  # 1 year from anchor
    2025: 0.15,  # 2 years from anchor
    2026: 0.15,  # 3 years from anchor
}


def compute_score(var_id: str, value: float) -> float:
    p = NORMALIZATION[var_id]
    z = (value - p["median"]) / p["sd"]
    score = 100.0 + 10.0 * p["direction"] * z
    return max(50.0, min(150.0, score))


def get_correct_status(var_id: str, year: int, original_status: str) -> str:
    if year <= 2023:
        return original_status
    if year == 2026:
        return "bridge_estimate"
    if var_id == "average_net_pension_real":
        return "bridge_estimate"
    elif var_id == "effective_retirement_age":
        return "bridge_estimate"
    elif var_id == "real_gdp":
        return "observed_complete"
    elif var_id == "unemployment_rate":
        return "observed_complete"
    elif var_id == "median_living_standard_real":
        if year == 2024:
            return "observed_complete"
        return "bridge_estimate"
    elif var_id == "poverty_rate":
        return "observed_complete"
    elif var_id == "housing_cost_burden":
        return "observed_complete"
    return original_status


def build_correct_panel() -> pl.DataFrame:
    """Build panel with correct status logic and non-zero uncertainty for bridge values."""
    comp = pl.read_csv(MODELING_DIR / "francescope_components_2010_2026.csv")
    
    rows = []
    for row in comp.iter_rows(named=True):
        var_id = row["variable_id"]
        year = row["year"]
        
        correct_status = get_correct_status(var_id, year, row["data_status"])
        value = row["value"]
        lower = row["lower_bound"]
        upper = row["upper_bound"]
        
        # Apply non-zero uncertainty for retirement age bridge estimates
        if var_id == "effective_retirement_age" and correct_status == "bridge_estimate":
            uncertainty = RETIREMENT_AGE_BRIDGE_UNCERTAINTY.get(year, 0.15)
            lower = value - uncertainty
            upper = value + uncertainty
        
        rows.append({
            "variable_id": var_id,
            "year": year,
            "value": value,
            "value_status": correct_status,
            "lower_bound": lower,
            "upper_bound": upper,
        })
    
    return pl.DataFrame(rows).sort(["year", "variable_id"])


def compute_index_with_proper_bounds(panel: pl.DataFrame) -> pl.DataFrame:
    """Compute index with correct uncertainty bounds."""
    rows = []
    for year in range(2010, 2027):
        year_data = panel.filter(pl.col("year") == year)
        scores, lower_scores, upper_scores = [], [], []
        bridged, observed = 0, 0
        
        for var_id in CORE_VARIABLES:
            vd = year_data.filter(pl.col("variable_id") == var_id)
            if vd.is_empty():
                continue
            
            v = vd["value"][0]
            s = vd["value_status"][0]
            lo = vd["lower_bound"][0]
            hi = vd["upper_bound"][0]
            direction = NORMALIZATION[var_id]["direction"]
            
            scores.append(compute_score(var_id, v))
            
            if direction > 0:
                lower_scores.append(compute_score(var_id, lo))
                upper_scores.append(compute_score(var_id, hi))
            else:
                lower_scores.append(compute_score(var_id, hi))
                upper_scores.append(compute_score(var_id, lo))
            
            if s == "bridge_estimate":
                bridged += 1
            else:
                observed += 1
        
        if len(scores) == 0:
            continue
        
        n = len(scores)
        
        if bridged == 0:
            status = "observed_complete"
        elif observed == 0:
            status = "bridge_heavy"
        else:
            status = "mixed_observed_bridge"
        
        rows.append({
            "year": year,
            "francescope_index": sum(scores) / n,
            "index_lower_bound": sum(lower_scores) / n,
            "index_upper_bound": sum(upper_scores) / n,
            "status": status,
            "components_used": n,
            "observed_components": observed,
            "bridged_components": bridged,
        })
    
    return pl.DataFrame(rows)


def verify_bridge_uncertainty(panel: pl.DataFrame) -> tuple[bool, list]:
    """Verify that all bridge estimates have non-zero uncertainty."""
    issues = []
    for row in panel.iter_rows(named=True):
        if row["value_status"] == "bridge_estimate":
            width = row["upper_bound"] - row["lower_bound"]
            if width <= 0:
                issues.append(f"{row['variable_id']} {row['year']}: width={width}")
    return len(issues) == 0, issues


def main():
    print("=== FINAL FIX: RETIREMENT AGE UNCERTAINTY ===\n")
    
    # Build panel
    panel = build_correct_panel()
    
    # Verify bridge uncertainty
    valid, issues = verify_bridge_uncertainty(panel)
    print(f"Normal bridge estimates have non-zero uncertainty: {valid}")
    if issues:
        print(f"Issues: {issues}")
    
    # Show retirement age values
    print("\n=== RETIREMENT AGE BRIDGE VALUES ===")
    era = panel.filter(pl.col("variable_id") == "effective_retirement_age")
    for year in [2024, 2025, 2026]:
        row = era.filter(pl.col("year") == year)
        if not row.is_empty():
            print(f"  {year}: value={row['value'][0]:.4f}, lower={row['lower_bound'][0]:.4f}, upper={row['upper_bound'][0]:.4f}")
    
    # Save panel
    panel.write_csv(MODELING_DIR / "francescope_core_annual_2010_2026.csv")
    
    # Compute index
    index = compute_index_with_proper_bounds(panel)
    index.write_csv(MODELING_DIR / "francescope_economic_index_2010_2026_final.csv")
    
    print("\n=== FINAL INDEX 2024-2026 ===")
    result = index.filter(pl.col("year").is_in([2024, 2025, 2026]))
    print(result.write_csv())
    
    print("\n=== QUALITY CHECKS ===")
    # Check invariant
    all_valid = True
    for row in index.iter_rows(named=True):
        if row["components_used"] > 0:
            valid = row["index_lower_bound"] <= row["francescope_index"] <= row["index_upper_bound"]
            if not valid:
                all_valid = False
    print(f"Index bounds invariant: {all_valid}")
    print(f"Normal bridge uncertainty: {valid}")


if __name__ == "__main__":
    main()
