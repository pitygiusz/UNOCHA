import json
import pandas as pd
from pathlib import Path

def filter_humanitarian_data(agent_json_string: str, csv_file_path: str) -> pd.DataFrame:
    """
    Filters humanitarian data from CSV based on parameters from agent JSON.
    Returns a filtered Pandas DataFrame.
    """
    # 1. Load CSV file
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
        return pd.DataFrame()
    
    # 2. Parse JSON to Python dictionary
    try:
        filters = json.loads(agent_json_string)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return pd.DataFrame(columns=df.columns)

    # 3. Apply filters dynamically
    filtered_df = df.copy()
    
    # Filter by regions (country_code)
    if filters.get("regions"):
        regions = filters["regions"]
        filtered_df = filtered_df[filtered_df["country_code"].isin(regions)]
    
    # Filter by sectors (cluster_code or sector)
    if filters.get("sectors"):
        sectors = filters["sectors"]
        # Check if 'cluster_code' column exists, otherwise try 'sector'
        if "cluster_code" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["cluster_code"].isin(sectors)]
        elif "sector" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["sector"].isin(sectors)]
    
    # Filter by year range
    if filters.get("year_range") and len(filters["year_range"]) == 2:
        min_year, max_year = filters["year_range"]
        filtered_df = filtered_df[
            (filtered_df["year"] >= min_year) & (filtered_df["year"] <= max_year)
        ]
    
    # Filter by minimum scale of need (in_need column)
    if filters.get("min_scale_of_need"):
        min_need = filters["min_scale_of_need"]
        filtered_df = filtered_df[filtered_df["in_need"] >= min_need]
    
    # Filter by maximum coverage ratio (total_granted_percentage)
    if filters.get("max_coverage_ratio"):
        max_coverage = filters["max_coverage_ratio"]
        if "total_granted_percentage" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["total_granted_percentage"] <= max_coverage]
    
    return filtered_df
