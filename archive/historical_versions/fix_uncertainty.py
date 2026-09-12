"""Fix uncertainty propagation and investigate issues."""
from __future__ import annotations

from pathlib import Path

import polars as pl

MODELING_DIR = Path("data/modeling/economic_index")
AUDIT_DIR = Path("data/audits/institutional_forecast_readiness")

CORE_VARIABLES = [
    "average_net_pension_real",
    "effective_retirement_age",
    "real_gdp",
    "unemployment_rate",
    "median_living_standard_real",
    "poverty_rate",
    "housing_cost_burden",
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

CLIP_LOWER = 50.0
CLIP_UPPER = 150.0


def compute_score(var_id: str, value: float) -> float:
    p = NORMALIZATION[var_id]
    z = (value - p["median"]) / p["sd"]
    score = 100.0 + 10.0 * p["direction"] * z
    return max(CLIP_LOWER, min(CLIP_UPPER, score))


def compute_index_with_proper_bounds(panel: pl.DataFrame) -> pl.DataFrame:
    """Compute index with CORRECT uncertainty bounds.
    
    For direction=1 (higher is better):
      - lower bound value -> lower score
      - upper bound value -> higher score
    
    For direction=-1 (lower is better):
      - lower bound value -> HIGHER score (because lower numeric value is better)
      - upper bound value -> LOWER score (because higher numeric value is worse)
    
    Therefore:
      - index_lower_bound = min possible index = worst case = 
        sum of (lower_score for direction=1, upper_score for direction=-1) / n
      - index_upper_bound = max possible index = best case =
        sum of (upper_score for direction=1, lower_score for direction=-1) / n
    """
    rows = []
    for year in range(2010, 2027):
        year_data = panel.filter(pl.col("year") == year)
        scores, lower_scores, upper_scores = [], [], []
        bridged, observed = 0, 0
        
        for var_id in CORE_VARIABLES:
            vd = year_data.filter(pl.col("variable_id") == var_id)
            if vd.is_empty():
                continue
            v, s, lo, hi = vd["value"][0], vd["value_status"][0], vd["lower_bound"][0], vd["upper_bound"][0]
            direction = NORMALIZATION[var_id]["direction"]
            
            scores.append(compute_score(var_id, v))
            
            if direction > 0:
                # Higher is better: lower value = lower score, upper value = higher score
                lower_scores.append(compute_score(var_id, lo))
                upper_scores.append(compute_score(var_id, hi))
            else:
                # Lower is better: lower value = HIGHER score, upper value = LOWER score
                lower_scores.append(compute_score(var_id, hi))  # SWAPPED!
                upper_scores.append(compute_score(var_id, lo))  # SWAPPED!
            
            if s == "bridge_estimate":
                bridged += 1
            else:
                observed += 1
        
        status = "observed_complete" if bridged == 0 else ("bridge_heavy" if observed == 0 else "mixed_observed_bridge")
        
        rows.append({
            "year": year,
            "francescope_index": sum(scores) / len(scores),
            "index_lower_bound": sum(lower_scores) / len(lower_scores),
            "index_upper_bound": sum(upper_scores) / len(upper_scores),
            "status": status,
            "components_used": len(scores),
            "observed_components": observed,
            "bridged_components": bridged,
        })
    
    return pl.DataFrame(rows)


def main():
    print("=== FIXING UNCERTAINTY BOUNDS ===\n")
    
    # Load panel
    panel = pl.read_csv(MODELING_DIR / "francescope_core_annual_2010_2026.csv")
    
    # Compute index with correct bounds
    index = compute_index_with_proper_bounds(panel)
    
    # Check invariant
    print("Checking invariant: lower_bound <= index <= upper_bound")
    all_valid = True
    for row in index.iter_rows(named=True):
        valid = row["index_lower_bound"] <= row["francescope_index"] <= row["index_upper_bound"]
        status = "OK" if valid else "FAIL"
        if not valid:
            all_valid = False
        print(f"  {row['year']}: {row['francescope_index']:.4f} [{row['index_lower_bound']:.4f}, {row['index_upper_bound']:.4f}] {status}")
    
    print(f"\nAll invariants valid: {all_valid}")
    
    # Save corrected index
    index.write_csv(MODELING_DIR / "francescope_economic_index_2010_2026_final.csv")
    
    # Show 2023-2026
    print("\n=== CORRECTED INDEX 2023-2026 ===")
    print(index.filter(pl.col("year") >= 2023).write_csv())
    
    # Investigate effective_retirement_age provenance
    print("\n=== INVESTIGATING effective_retirement_age PROVENANCE ===")
    
    # Check canonical for this variable
    canonical = pl.read_parquet("data/processed/master_canonical.parquet")
    era = canonical.filter(pl.col("variable_id") == "effective_retirement_age")
    
    if not era.is_empty():
        print(f"Found {era.height} rows in canonical")
        # Get years 2024 and 2025
        for year in ["2024", "2025"]:
            yr_data = era.filter(pl.col("period") == year)
            if not yr_data.is_empty():
                print(f"\n{year}:")
                print(f"  value: {yr_data['value'][0]}")
                print(f"  source: {yr_data['source'][0]}")
                print(f"  dataset: {yr_data['source_dataset'][0]}")
    
    # Compare with bridge values
    print("\n=== BRIDGE VALUES FOR RETIREMENT AGE ===")
    bridge = pl.read_csv(MODELING_DIR / "economic_index_bridge_values_2024_2026.csv")
    era_bridge = bridge.filter(pl.col("variable_id") == "effective_retirement_age")
    print(era_bridge[["year", "bridge_value", "data_status", "method"]].write_csv())
    
    # Check the existing historical components file
    print("\n=== COMPONENTS FILE RETIREMENT AGE ===")
    comp = pl.read_csv(MODELING_DIR / "francescope_components_2010_2026.csv")
    era_comp = comp.filter(pl.col("variable_id") == "effective_retirement_age")
    print(era_comp.filter(pl.col("year").is_in([2023, 2024, 2025])).write_csv())
    
    # Check existing validated series
    print("\n=== COMPARING WITH ORIGINAL HISTORICAL INDEX ===")
    orig = pl.read_csv(MODELING_DIR / "francescope_index_2010_2026.csv")
    print(orig.filter(pl.col("year").is_in([2020, 2021, 2022, 2023])).write_csv())
    
    # Compare with our new calculation
    print("\n=== OUR NEW CALCULATION (2020-2023) ===")
    print(index.filter(pl.col("year").is_in([2020, 2021, 2022, 2023])).write_csv())
    
    print("\n=== ANALYSIS ===")
    print("The historical index differences are due to:")
    print("1. Different component data sources for certain variables")
    print("2. Our panel uses the component_2010_2026.csv data which may differ from original")
    print("3. The original index may have used different raw source data")
    print("\nFor the index to be consistent, we need to use the SAME canonical source data.")


if __name__ == "__main__":
    main()
