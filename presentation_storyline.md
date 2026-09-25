# Strategic Presentation Storyline Index

This document structures the reframing models for the Guntur **+122.19% Month-over-Month revenue spike** flag discovered during the April–May transition.

---

## 🏛️ Storyline Framework A: The Executive Briefing
**Structure Profile**: Situation ➔ Complication ➔ Resolution (SCR)

### 1. Situation (Current Operational State)
Our regional data operations desk successfully deployed the **PharmEasy Regional Pulse Engine** to process, clean, and standardize quarterly order records across the Telugu-speaking states. This framework establishes an auditable baseline for tracking performance and flagging revenue volatility across all active distribution channels.

### 2. Complication (The Core Performance Outlier)
During the April-May 2026 monthly transition, the pipeline flagged an anomalous revenue surge in the Guntur region. Total sales jumped from **INR 8,605.95** to **INR 19,121.50**, representing a **+122.19% spike** that far exceeded our standard 8% variation threshold. The change immediately reversed the following month, confirming this was a highly volatile, transient spike rather than stable market growth.

### 3. Resolution (Strategic Management Directive)
To prevent inventory imbalances, we recommend sending a field supervisor to the Guntur fulfillment hub immediately to perform a manual facility audit. The team will cross-reference physical inventory counts with digital order logs and present their findings at our upcoming operations review on October 15, 2026.

---

## 🏃 Storyline Framework B: The Regional Operations Review
**Structure Profile**: Overview ➔ Category ➔ Detail (OCD)

### 1. Overview (The Headline Performance Metric)
Attention Team: The pipeline flagged Guntur as the single largest performance outlier across the regional desk, driven by a rapid **+122.19% revenue surge** during the April-May 2026 monitoring cycle.

### 2. Category (The Primary Volume Driver)
Granular pipeline filtering shows this revenue surge was concentrated entirely within the **OTC Medicines** and **Prescription Medicines** segments. These two product categories accounted for over 55% of the total transaction volume in the region, while newer segments like Lab Tests remained completely flat.

### 3. Detail (Supporting Verification Logic)
These metrics are calculated directly from our verified SQLite tables (`orders_clean`). We confirmed the trend by cross-referencing it with control markets like Nellore, which remained completely stable during the same period. This validation rules out systemic data anomalies and confirms the variance was isolated to Guntur.

---

## 🛑 3. Anticipated Stakeholder Pushback Q&A
This section uses the **Direct Acknowledgement Pattern** to address common operational concerns.

### Question 1: "Why should I believe this number? The sales jump looks like a copy-paste error from our regional store spreadsheet."
- **Direct Acknowledgement**: We understand the concern that a sudden +122.19% revenue surge could look like an infrastructure data entry error rather than a real market change.
- **Verification Boundaries**: We verified that our upstream data cleaning script (`clean_data.py`) successfully deduplicated the raw data, removing exactly **59 duplicate entries** before ingestion. However, we have not yet verified the physical delivery receipts at the Guntur facility.
- **Resolution Plan**: The regional data engineering lead will run a transaction log trace on the database by October 2, 2026, to confirm that all recorded orders correspond to distinct transaction IDs.

### Question 2: "What if an alternative explanation is driving this? Our team ran a local marketing campaign in Guntur that might explain the entire spike."
- **Direct Acknowledgement**: We acknowledge that localized marketing activities can drive significant short-term demand variations.
- **Verification Boundaries**: We have verified the exact timing of the revenue jump using database timestamps, but we cannot track external marketing spend or local campaign schedules within the order data itself.
- **Resolution Plan**: The Guntur territory manager will provide the local marketing and promotional calendar by October 5, 2026. We will cross-reference these campaign dates with daily sales trends to see if the marketing push caused the volume spike.
