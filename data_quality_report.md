# Data Quality & Governance Diagnostic Report

This report maps the programmatic data mutations executed during the cleansing pipeline (`clean_data.py`) back to their formal foundational industry data-quality dimensions.

## 📊 Summary Mapping Table

| Pipeline Mitigation Task | Anomaly Remediated | Data Quality Dimension Address | Technical Verification / Outcome |
| :--- | :--- | :--- | :--- |
| **Task 1.2.1** | Multi-source exact duplicate lines dropped. | **Uniqueness** | **59 duplicate rows** deleted; exactly **2100 rows** retained. |
| **Task 1.2.2** | Stripped whitespaces and unified casing variants. | **Consistency** | Collapsed **16 messy strings** onto **9 clean canonical targets**. |
| **Task 1.2.3** | Replaced blank structural records using deterministic product keys. | **Completeness** & **Validity** | **48 empty entries** backfilled via lookup dictionary. |
| **Task 1.2.4** | Generated un-synchronized margins via subgroup historic averages. | **Completeness** & **Accuracy** | **94 missing profit fields** populated via mean multipliers. |
| **Task 1.3** | Automated structure verification function check. | **Validity** | Catches column structural failures via `blocked_schema` error triggers. |

---

## 🏛️ Dimensional Definitions & Applied Contexts

### 1. Uniqueness
- **Context**: Exact data overlap can double metrics like revenue and order counts, artificially inflating overall performance numbers.
- **Application**: Dropping exact duplicate rows prevents multi-source copy-paste errors from distorting the downstream SQLite queries.

### 2. Consistency
- **Context**: Discrepancies in text entries (like `" hyderabad"` vs `"Hyderabad"`) prevent databases from grouping records correctly during `SUM` or `COUNT` aggregation routines.
- **Application**: Normalizing strings to canonical names ensures text formatting matches the values inside `regions_master.csv`.

### 3. Completeness
- **Context**: Empty properties disrupt reporting logic and prevent downstream financial formulas from executing properly.
- **Application**: The system achieves 100% complete metrics by filling missing category and profit data using deterministic product-to-category associations and historical category performance margins.

### 4. Validity
- **Context**: Transactions must strictly adhere to the business rules, structural columns, and reference definitions set by corporate templates.
- **Application**: Checked explicitly via `validate_schema()`. Missing structural tables trigger an immediate infrastructure alert (`blocked_schema`), stopping corrupt raw streams from entering production views.

### 5. Timeliness, Accuracy, and Relevance
- **Timeliness**: The source data matches the designated financial quarter (**April, May, June 2026**). It is updated regularly through a predictable month-end batch schedule.
- **Accuracy**: Using category-specific mean margins for missing records gives a closer approximation of real performance than applying a generic, flat multiplier across the entire data stream.
- **Relevance**: Filters out unneeded database noise, leaving only fields directly tied to performance monitoring (like volumes, turnaround metrics, and gross margins).
