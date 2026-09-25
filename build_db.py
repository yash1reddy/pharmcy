"""
build_db.py -- PharmEasy Regional Pulse SQL Engine.
Populates local SQLite database and performs structural JOIN and NULL validation checks.
"""
import sqlite3
import os
import pandas as pd

DB_NAME = "pharmeasy.db"
CLEANED_ORDERS_FILE = "orders_clean.csv"
REGIONS_MASTER_FILE = "regions_master.csv"

def initialize_database():
    print("⏳ Starting Part 2: SQL Engine Initialization...")
    
    if not os.path.exists(CLEANED_ORDERS_FILE) or not os.path.exists(REGIONS_MASTER_FILE):
        raise FileNotFoundError("Cleaned master artifacts not found. Please execute Part 1 first.")
        
    df_orders = pd.read_csv(CLEANED_ORDERS_FILE)
    df_regions = pd.read_csv(REGIONS_MASTER_FILE)
    
    conn = sqlite3.connect(DB_NAME)
    
    # Ingest clean data frames directly into local table structures
    df_orders.to_sql("orders_clean", conn, if_exists="replace", index=False)
    df_regions.to_sql("regions_master", conn, if_exists="replace", index=False)
    
    print(f"   [SQL Ingestion] Loaded {len(df_regions)} master regions and {len(df_orders)} order lines into '{DB_NAME}'.")
    return conn

def execute_validation_queries(conn):
    print("\n🔍 Running Task 2.2 Relational Integrity Verification...")
    cursor = conn.cursor()
    
    # 1. Row Count Check (LEFT vs INNER JOIN)
    cursor.execute("""
        SELECT 
            (SELECT COUNT(*) FROM regions_master r LEFT JOIN orders_clean o ON r.region = o.region) as left_count,
            (SELECT COUNT(*) FROM regions_master r INNER JOIN orders_clean o ON r.region = o.region) as inner_count
    """)
    left_cnt, inner_cnt = cursor.fetchone()
    print(f"   - Join Row Counts: LEFT JOIN = {left_cnt} | INNER JOIN = {inner_cnt} (Delta = {left_cnt - inner_cnt} row)")
    
    # 2. Duplicate Key Check
    cursor.execute("""
        SELECT order_id, COUNT(*) FROM orders_clean GROUP BY order_id HAVING COUNT(*) > 1
    """)
    dup_rows = cursor.fetchall()
    print(f"   - Duplicate order_id Violations Found: {len(dup_rows)} rows.")
    
    # 3. COUNT(*) vs COUNT(fk) Structural Pitfall Evaluation
    cursor.execute("""
        SELECT r.region, COUNT(*), COUNT(o.order_id)
        FROM regions_master r
        LEFT JOIN orders_clean o ON r.region = o.region
        GROUP BY r.region
    """)
    regions_report = cursor.fetchall()
    
    print("\n   - Pitfall Evaluation Summary [COUNT(*) vs COUNT(order_id)]:")
    for region, count_all, count_id in regions_report:
        mismatch_flag = "⚠️ MISMATCH" if count_all != count_id else "✓ Match"
        print(f"     * {region:<15}: COUNT(*) = {count_all:<4} | COUNT(order_id) = {count_id:<4} | {mismatch_flag}")

    # 4. Per Region Order Counts (Sorted Ascending)
    cursor.execute("""
        SELECT r.region, COUNT(o.order_id) as order_volume
        FROM regions_master r
        LEFT JOIN orders_clean o ON r.region = o.region
        GROUP BY r.region
        ORDER BY order_volume ASC
    """)
    asc_report = cursor.fetchall()
    print("\n   - Per-Region Order Counts (Ordered Ascending via LEFT JOIN):")
    for region, vol in asc_report:
        print(f"     * {region:<15}: {vol} orders")

if __name__ == "__main__":
    db_connection = initialize_database()
    execute_validation_queries(db_connection)
    db_connection.close()
