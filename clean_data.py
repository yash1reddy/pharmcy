"""
clean_data.py -- PharmEasy Regional Pulse Cleaning & Validation Engine.
Processes raw orders, handles string normalization, computes exact lookups and mean margins,
and performs structural schema validations.
"""
import os
import pandas as pd
import numpy as np

RAW_ORDERS_FILE = "pharmeasy_orders_raw.csv"
CLEANED_ORDERS_FILE = "orders_clean.csv"

def validate_schema(df, required_columns):
    """
    Validates that the DataFrame contains all required columns.
    Returns a dictionary indicating status, current row count, and missing fields.
    """
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        return {
            "status": "blocked_schema",
            "row_count": len(df),
            "missing_columns": missing_cols
        }
    return {
        "status": "validated",
        "row_count": len(df),
        "missing_columns": []
    }

def run_cleaning_pipeline():
    print("⏳ Starting Part 1: Data Cleaning & Validation Pipeline...")
    
    if not os.path.exists(RAW_ORDERS_FILE):
        raise FileNotFoundError(f"Source file '{RAW_ORDERS_FILE}' not found. Run generate_dataset.py first.")
        
    df = pd.read_csv(RAW_ORDERS_FILE)
    print(f"Initial raw rows loaded: {len(df)}")
    
    # --- Step 1: Remove Exact Duplicate Rows ---
    before_dup = len(df)
    df = df.drop_duplicates(keep='first').copy()
    removed_dups = before_dup - len(df)
    print(f"   [Step 1: Uniqueness] Removed {removed_dups} exact duplicate rows. (Remaining: {len(df)})")
    
    # --- Step 2: Normalize Region Text ---
    raw_unique_regions = df['region'].nunique()
    df['region'] = df['region'].astype(str).str.strip().str.title()
    clean_unique_regions = df['region'].nunique()
    print(f"   [Step 2: Consistency] Normalized region variants from {raw_unique_regions} down to {clean_unique_regions} canonical names.")
    
    # --- Step 3: Impute Missing Category via Product Lookup ---
    missing_cat_before = df['category'].isna().sum() + (df['category'] == "").sum()
    # Build deterministic map from valid pairs
    valid_pairs = df[df['category'].notna() & (df['category'] != "")]
    product_to_cat = dict(zip(valid_pairs['product'], valid_pairs['category']))
    
    # Replace empty strings with NaN for reliable filling
    df['category'] = df['category'].replace("", np.nan)
    df['category'] = df['category'].fillna(df['product'].map(product_to_cat))
    missing_cat_after = df['category'].isna().sum()
    print(f"   [Step 3: Completeness] Imputed {missing_cat_before} missing categories via Product Lookup. (Remaining missing: {missing_cat_after})")
    
    # --- Step 4: Impute Missing profit_inr via Category Mean Margin ---
    df['profit_inr'] = pd.to_numeric(df['profit_inr'].replace("", np.nan), errors='coerce')
    missing_profit_before = df['profit_inr'].isna().sum()
    
    # Compute mean profit margin per category on non-missing items
    non_missing_profit = df[df['profit_inr'].notna()].copy()
    non_missing_profit['margin'] = non_missing_profit['profit_inr'] / non_missing_profit['sales_inr']
    category_mean_margins = non_missing_profit.groupby('category')['margin'].mean().to_dict()
    
    # Apply calculation to missing fields
    def impute_profit(row):
        if pd.isna(row['profit_inr']):
            mean_margin = category_mean_margins[row['category']]
            return round(row['sales_inr'] * mean_margin, 2)
        return row['profit_inr']
        
    df['profit_inr'] = df.apply(impute_profit, axis=1)
    missing_profit_after = df['profit_inr'].isna().sum()
    print(f"   [Step 4: Completeness] Imputed {missing_profit_before} missing profits via Mean Margin. (Remaining missing: {missing_profit_after})")
    
    # --- Step 5: Save Dataset ---
    df.to_csv(CLEANED_ORDERS_FILE, index=False)
    print(f"   [Step 5] Saved clean operational dataset to '{CLEANED_ORDERS_FILE}' with {len(df)} records.")
    
    # --- Task 1.3: Schema Validation Verification ---
    required_cols = ["order_id", "order_date", "region", "category", "product", "quantity", "sales_inr", "profit_inr"]
    
    print("\n🔍 Running Task 1.3 Schema Validations...")
    # Validate clean copy
    clean_val = validate_schema(df, required_cols)
    print(f"   Clean Data Schema Validation Result: {clean_val}")
    
    # Validate a broken copy (simulated error by dropping 'profit_inr')
    broken_df = df.drop(columns=['profit_inr'])
    broken_val = validate_schema(broken_df, required_cols)
    print(f"   Broken Data Schema Validation Result: {broken_val}")
    
    print("\n✅ Part 1 Pipeline Executed Successfully!")

if __name__ == "__main__":
    run_cleaning_pipeline()
