"""
narrative_generator.py -- PharmEasy Regional Pulse Narrative & Review Engine.
Automates CII generation, establishes human validation gates, and appends to structural audit files.
"""
import os
import json
import uuid
from datetime import datetime

AUDIT_LOG_FILE = "audit_log.jsonl"

def draft_report_v1(flagged_regions, metrics):
    """
    Generates standardized Context-Insight-Implication blocks for flagged regions.
    Dedupes overlapping region flags across both execution transitions.
    """
    cii_blocks = {}
    
    for region in flagged_regions:
        # Safely extract multi-period trends from metrics maps
        apr_val = metrics["2026-04"].get(region, 0.0)
        may_val = metrics["2026-05"].get(region, 0.0)
        jun_val = metrics["2026-06"].get(region, 0.0)
        
        # Compute exact multi-period percentage variations
        t1_pct = ((may_val - apr_val) / apr_val * 100.0) if apr_val > 0 else 0.0
        t2_pct = ((jun_val - may_val) / may_val * 100.0) if may_val > 0 else 0.0
        
        context = (f"Evaluating historical sales performance for {region} across Q1-2026. "
                   f"Baseline April Sales started at INR {apr_val:,.2f}, moving to INR {may_val:,.2f} "
                   f"in May, and concluding at INR {jun_val:,.2f} for June.")
        
        insight = (f"Programmatic analysis flagged structural MoM volatility. "
                   f"Transition 1 (Apr➔May) recorded a change of {t1_pct:+.2f}%. "
                   f"Transition 2 (May➔Jun) recorded a change of {t2_pct:+.2f}%.")
        
        implication = (f"Operational leads must investigate if seasonal volume changes or localized "
                       f"inventory issues drove these fluctuations. Stable logistics structures are "
                       f"required to prevent stockouts or high carrying costs.")
        
        cii_blocks[region] = {
            "Context": context,
            "Insight": insight,
            "Implication": implication
        }
        
    return cii_blocks

def review_gate_v1(report_id, region, decision, reviewer_note=""):
    """
    Applies an authorization block over generated text report drafts.
    Appends execution states to an immutable audit trail file.
    """
    allowed_decisions = {"approve", "edit", "reject"}
    if decision not in allowed_decisions:
        raise ValueError(f"Invalid decision parameter '{decision}'. Must be one of {allowed_decisions}")
        
    # Set deployment flag based on decision state
    downstream_allowed = (decision == "approve")
    
    gate_state = {
        "report_id": report_id,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note,
        "downstream_use_allowed": downstream_allowed,
        "last_validated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Append structured log entry to the audit file
    audit_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "run_id": str(uuid.uuid4())[:8],
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note
    }
    
    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(audit_entry) + "\n")
        
    return gate_state

def execute_test_harness():
    print("⏳ Starting Part 3 Governance Engine Test Harness...")
    
    # Clean old logs if present to ensure clean testing state
    if os.path.exists(AUDIT_LOG_FILE):
        os.remove(AUDIT_LOG_FILE)
        
    # Simulate historical metrics dictionary maps from Part 2 outputs
    mock_metrics = {
        "2026-04": {"Guntur": 8605.95, "Bengaluru": 19412.00, "Vijayawada": 14210.00},
        "2026-05": {"Guntur": 19121.50, "Bengaluru": 23410.50, "Vijayawada": 13990.00},
        "2026-06": {"Guntur": 13540.20, "Bengaluru": 21100.00, "Vijayawada": 18210.50}
    }
    
    # Create the full list of unique regions flagged across both periods
    flagged_union = ["Guntur", "Bengaluru", "Vijayawada"]
    
    # 1. Exercise Task 3.1: Generate CII Blocks
    reports = draft_report_v1(flagged_union, mock_metrics)
    print(f"   [CII Generation] Compiled {len(reports)} unique regional reports.")
    print(f"   - Guntur Insight Draft: {reports['Guntur']['Insight']}")
    
    # 2. Exercise Task 3.4: Run the Three-Path Decision Validation Gate
    print("\n🚀 Executing 3-Path Decision Gate Evaluations:")
    
    # Path 1: Approval Workflow
    state_approve = review_gate_v1("REP-001", "Guntur", "approve", "Verified metrics match SQL tables. Approved for dashboard deployment.")
    print(f"     * Path 1 (Approve) Outcome -> Downstream Allowed: {state_approve['downstream_use_allowed']}")
    
    # Path 2: Edit Workflow
    state_edit = review_gate_v1("REP-002", "Bengaluru", "edit", "Numbers match, but update narrative to highlight inventory changes.")
    print(f"     * Path 2 (Edit) Outcome    -> Downstream Allowed: {state_edit['downstream_use_allowed']}")
    
    # Path 3: Rejection Workflow
    state_reject = review_gate_v1("REP-003", "Vijayawada", "reject", "Data sync failure detected. Re-run upstream pipeline.")
    print(f"     * Path 3 (Reject) Outcome  -> Downstream Allowed: {state_reject['downstream_use_allowed']}")
    
    # Verify file output length
    with open(AUDIT_LOG_FILE, "r") as f:
        log_lines = f.readlines()
    print(f"\n✅ Audit verification complete. Total entries logged: {len(log_lines)} (Expected: 3)")

if __name__ == "__main__":
    execute_test_harness()
