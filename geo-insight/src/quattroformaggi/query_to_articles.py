import json
import pandas as pd

def filter_articles(agent_json_string: str, csv_file_path: str) -> pd.DataFrame:
    """
    Filters articles data from CSV based on parameters from agent JSON.
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
        # Try country_code column, fallback to country
        if "country_code" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["country_code"].isin(regions)]
        elif "country" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["country"].isin(regions)]
    
    # Filter by sectors (cluster_code or sector_code)
    if filters.get("sectors"):
        sectors = filters["sectors"]
        if "cluster_code" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["cluster_code"].isin(sectors)]
        elif "sector_code" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["sector_code"].isin(sectors)]
    
    # Limit to 20 most recent articles
    if "date" in filtered_df.columns or "publication_date" in filtered_df.columns:
        date_col = "date" if "date" in filtered_df.columns else "publication_date"
        filtered_df = filtered_df.sort_values(date_col, ascending=False)
    
    return filtered_df.head(20)
