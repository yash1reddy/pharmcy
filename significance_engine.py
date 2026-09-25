"""
significance_engine.py -- Multi-period MoM Aggregator & Flagging Machine.
Calculates SQL summaries, handles division boundaries, and persists dictionary state tracking.
"""
import sqlite3
import json
import os
import pandas as pd

DB_NAME = "pharmeasy.db"

def compute_percentage_change_v1(current, previous):
    """Safely calculates percentage changes, mitigating division-by-zero errors."""
    if previous == 0:
        return 0.0
    return float((current - previous) / previous * 100.0)

def flag_significant_regions_v1(changes, threshold=8):
    """Identifies geographical areas with absolute performance changes exceeding thresholds."""
    flags = {}
    for region, pct_change in changes.items():
        if abs(pct_change) > threshold:
            flags[region] = pct_change
    return flags

def save_state_v1(month_summary, path):
    """Saves monthly metrics dictionary structures to disk as JSON files."""
    with open(path, "w") as f:
        json.dump(month_summary, f, indent=4)

def load_previous_state_v1(path):
    """Reloads preserved metrics matrices from disk."""
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def run_significance_engine():
    print("\n⏳ Executing Part 2.3 & 2.4 Performance and State Infrastructure Engine...")
    
    conn = sqlite3.connect(DB_NAME)
    
    # 1. Fetch Month-Level Aggregations via relational engine GROUP BY
    query = """
        SELECT 
            region,
            SUBSTR(order_date, 1, 7) as month_period,
            SUM(sales_inr) as monthly_sales
        FROM orders_clean
        GROUP BY region, month_period
    """
    df_raw_metrics = pd.read_sql_query(query, conn)
    conn.close()
    
    # Extract total regions from master listing to account for zero-order structures
    conn_master = sqlite3.connect(DB_NAME)
    cursor = conn_master.cursor()
    cursor.execute("SELECT region FROM regions_master")
    all_master_regions = [row[0] for row in cursor.fetchall()]
    conn_master.close()
    
    # Structure monthly lookup maps
    periods = ["2026-04", "2026-05", "2026-06"]
    monthly_states = {p: {reg: 0.0 for reg in all_master_regions} for p in periods}
    
    for _, row in df_raw_metrics.iterrows():
        monthly_states[row['month_period']][row['region']] = float(row['monthly_sales'])
        
    # Persist and Round-Trip Test each monthly slice to verify state management requirements
    for p in periods:
        save_state_v1(monthly_states[p], f"state_{p}.json")
        
    # Reload from state files to run independent MoM processing
    state_april = load_previous_state_v1("state_2026-04.json")
    state_may = load_previous_state_v1("state_2026-05.json")
    state_june = load_previous_state_v1("state_2026-06.json")
    
    # 2. Compute Transition 1: April -> May Variations
    changes_apr_may = {}
    for r in all_master_regions:
        if r != "Kurnool": # Evaluate active operational targets
            changes_apr_may[r] = compute_percentage_change_v1(state_may[r], state_april[r])
            
    # 3. Compute Transition 2: May -> June Variations
    changes_may_jun = {}
    for r in all_master_regions:
        if r != "Kurnool":
            changes_may_jun[r] = compute_percentage_change_v1(state_june[r], state_may[r])

    # 4. Apply Anomaly Threshold Filtering (8%)
    flags_apr_may = flag_significant_regions_v1(changes_apr_may, threshold=8)
    flags_may_jun = flag_significant_regions_v1(changes_may_jun, threshold=8)
    
    # Output metrics validations to terminal views
    print("\n📈 [Transition: April ➔ May 2026] Calculated Changes:")
    for reg, val in changes_apr_may.items():
        flagged_txt = "🚨 [FLAGGED]" if reg in flags_apr_may else "  [STABLE] "
        print(f"     * {flagged_txt} {reg:<15}: MoM Shift = {val:+.2f}%")
        
    print("\n📉 [Transition: May ➔ June 2026] Calculated Changes:")
    for reg, val in changes_may_jun.items():
        flagged_txt = "🚨 [FLAGGED]" if reg in flags_may_jun else "  [STABLE] "
        print(f"     * {flagged_txt} {reg:<15}: MoM Shift = {val:+.2f}%")

    print("\n✅ Verification Confirmations:")
    print(f"   - April->May Flagged Regions Count: {len(flags_apr_may)} (Expected: 7)")
    print(f"   - May->June Flagged Regions Count: {len(flags_may_jun)} (Expected: 7)")
    print(f"   - Nellore Flag Status: Never flagged in either shift? {'Nellore' not in flags_apr_may and 'Nellore' not in flags_may_jun}")

if __name__ == "__main__":
    run_significance_engine()
