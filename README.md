# 💊 PharmEasy Regional Pulse

An automated, data-validated, Human-in-the-Loop operations monitoring platform tailored for PharmEasy's regional delivery channels in **Telangana, Andhra Pradesh, and the Bengaluru Hub**.

---

## 🚀 1. Setup & Installation (Run the Pipeline End-to-End)

Follow these **three simple commands** sequentially to clean, index, validate, and launch the interactive analytics dashboard stack from your shell environment.

### Command 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Command 2: Execute Ingestion, Pipeline Extraction & Analysis
This generates messy mock data, executes cleansing, applies winsorization guardrails, builds SQLite models, and aggregates regional metrics.
```bash
python generate_data.py && python pipeline.py
```

### Command 3: Launch Local Interactive Enterprise Dashboard Cockpit
```bash
streamlit run app.py
```

---

## 📂 2. Four-Artifact Strategic Cover Note

### Artifact A: The Data Cleaning Diagnostic Report
- **Input Integrity Auditing**: The pipeline processes messy text streams and removes whitespace and structural anomalies.
- **Financial Risk Mitigation Guardrails**: Negative transaction volumes are pruned. Outliers are handled using mathematical percentile winsorization at the `99th percentile` to eliminate data anomalies while preserving trend structures.
- **Data Loss Disclosures**: 
  - ~2% drop rate due to missing geo-location regional metadata identifiers.
  - ~1.5% record filtration rate applied to drop negative values.

### Artifact B: The SQLite Analytics Blueprint
- **Relational Ingestion Schema**: The system ingests processed data frames directly into a localized relational SQLite workspace (`pharmeasy_pulse.db`).
- **Mathematical Multi-Period Delta Inferences**: Programmatic change inferences are calculated via structured SQL window partition functions (`LAG() OVER (PARTITION BY region ORDER BY month_year)`), computing Month-over-Month volume modifications and operational speed performance metrics without pandas processing constraints.

### Artifact C: The Actionable Management Memo
- **Regional Strategy Directive**: When regional indicators decline past historical deviations (e.g., GMV drop > 5% or operational TAT bottlenecks > 48 hours), the text processing heuristics flag localized risks.
- **Tactical Implementation**: Alerts transition from passive monitoring state directives to urgent operational remediation deployment instructions.

### Artifact D: The Governance Audit Log
- **Human-In-The-Loop Workflow Design**: Every automated alert draft is blocked at an active review gate. Regional managers can evaluate, refine insights, and add oversight notes.
- **Immutable Log Schema**: Approved decisions are committed to an audit log (`audit_gate_log.csv`) capturing accurate timestamps and comments to verify corporate governance parameters.
