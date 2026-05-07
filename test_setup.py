#!/usr/bin/env python3
"""
Test script for UNOCHA Geo-Insight
Validates CSV, API keys, and basic functionality
"""

import os
import sys
import pandas as pd
from pathlib import Path
import json

def test_csv_file():
    """Test if CSV file exists and has required columns"""
    print("\n=== Testing CSV File ===")
    
    workspace_root = Path(__file__).resolve().parent
    csv_path = workspace_root / "data" / "unocha_dataset.csv"
    
    if not csv_path.exists():
        print(f"❌ CSV file not found at: {csv_path}")
        return False
    
    print(f"✓ CSV file found at: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path)
        print(f"✓ CSV loaded successfully")
        print(f"  Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        
        required_columns = [
            'country_code', 'cluster_code', 'sector', 'population',
            'in_need', 'targeted', 'year', 'total_required_funds',
            'total_granted_funds', 'total_granted_percentage', 'severity_index'
        ]
        
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            print(f"❌ Missing columns: {missing}")
            print(f"   Found columns: {list(df.columns)}")
            return False
        
        print(f"✓ All required columns present")
        print(f"  Sample data:")
        print(df.head(1).to_string())
        
        return True
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False

def test_environment_variables():
    """Test if required environment variables are set"""
    print("\n=== Testing Environment Variables ===")
    
    # Check .env file
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        print(f"✓ .env file found at: {env_path}")
    else:
        print(f"⚠ .env file not found at: {env_path}")
        print(f"  (This is required for local testing)")
        env_path = Path(__file__).resolve().parent / "geo-insight" / ".env.example"
        if env_path.exists():
            print(f"  Consider running: cp {env_path} .env")
    
    # Check OPENROUTER_API_KEY
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        masked_key = api_key[:10] + "..." + api_key[-5:] if len(api_key) > 15 else "***"
        print(f"✓ OPENROUTER_API_KEY is set: {masked_key}")
        return True
    else:
        print(f"❌ OPENROUTER_API_KEY is not set")
        print(f"   Add it to .env file or set it as environment variable")
        return False

def test_imports():
    """Test if all required packages are available"""
    print("\n=== Testing Package Imports ===")
    
    packages = [
        'gradio',
        'pandas',
        'pydantic',
        'requests',
    ]
    
    failed = []
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} not installed")
            failed.append(package)
    
    if failed:
        print(f"\nMissing packages: {', '.join(failed)}")
        print(f"Install with: pip install -r geo-insight/src/requirements.txt")
        return False
    
    return True

def test_query_spec():
    """Test if QuerySpec model can be imported and validated"""
    print("\n=== Testing QuerySpec Model ===")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).resolve().parent / "geo-insight" / "src"))
        from models.QuerySpec import QuerySpec
        
        # Test valid instance
        spec = QuerySpec(
            regions=["AFG"],
            sectors=["HEA"],
            crisis_types=None,
            min_scale_of_need=None,
            max_coverage_ratio=None,
            year_range=(2023, 2024),
            hrp_status=None,
            chronic_neglect_only=False,
            interpretation_confidence="high",
            interpretation_notes="Test"
        )
        
        print(f"✓ QuerySpec model works")
        print(f"  Sample: {spec.model_dump()}")
        return True
    except Exception as e:
        print(f"❌ Error with QuerySpec: {e}")
        return False

def test_data_filtering():
    """Test if data filtering functions work"""
    print("\n=== Testing Data Filtering ===")
    
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent / "geo-insight" / "src"))
        from quattroformaggi.query_to_sql import filter_humanitarian_data
        
        workspace_root = Path(__file__).resolve().parent
        csv_path = workspace_root / "data" / "unocha_dataset.csv"
        
        # Create test query
        test_query = json.dumps({
            "regions": ["AFG"],
            "sectors": None,
            "crisis_types": None,
            "min_scale_of_need": None,
            "max_coverage_ratio": None,
            "year_range": None,
            "hrp_status": None,
            "chronic_neglect_only": False
        })
        
        # Test filtering
        result = filter_humanitarian_data(test_query, str(csv_path))
        
        print(f"✓ Data filtering works")
        print(f"  Query: regions=['AFG']")
        print(f"  Result: {result.shape[0]} rows returned")
        
        if result.shape[0] > 0:
            print(f"  Sample:")
            print(result.head(1).to_string())
        
        return True
    except Exception as e:
        print(f"❌ Error with data filtering: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("UNOCHA Geo-Insight - Test Suite")
    print("=" * 50)
    
    results = {
        "CSV File": test_csv_file(),
        "Environment Variables": test_environment_variables(),
        "Package Imports": test_imports(),
        "QuerySpec Model": test_query_spec(),
        "Data Filtering": test_data_filtering(),
    }
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed! You're ready to run the app.")
        print("\nRun with: python geo-insight/src/app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    print("=" * 50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
