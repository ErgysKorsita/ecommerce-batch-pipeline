
# Silver Layer — Data Quality Findings

## Orders Dataset

**Source:** `olist_orders_dataset.csv`  
**Silver output:** `data/silver/orders.parquet`  
**Total records:** 99,441

---

### Finding 001 — Chronological Timestamp Inconsistencies

- **Observation** — 1,382 orders (1.39%) violate at least one of the seven chronological validation rules.

- **Breakdown:**
  - Carrier handoff before payment approval: 1,359 orders.
  - Carrier handoff before purchase: 166 orders.
  - Customer delivery before payment approval: 61 orders.
  - Customer delivery before carrier handoff: 23 orders.
  - Payment approval before purchase: 0 orders.
  - Customer delivery before purchase: 0 orders.
  - Estimated delivery before purchase: 0 orders.

- **Cause** — Unknown. Potential explanations include delayed event recording or inconsistent source timestamps.

- **Impact** — Chronological inconsistencies may affect delivery-time calculations and other time-based analytics.

- **Action** — Preserve affected records and flag them using `chronology_issue`. Investigate or filter them when building relevant Gold-layer analytics.

- **Status** — Flagged in Silver; no automatic correction or removal.

**Note:** Individual rule counts overlap because an order can violate multiple conditions.

---

### Finding 002 — Carrier Handoff Before Payment Approval

- **Observation** — 1,359 orders have a carrier handoff timestamp earlier than their payment approval timestamp.

- **Investigation:**
  - Mean difference: 24.75 hours.
  - Median difference: 17.17 hours.
  - Minimum difference: approximately 21 seconds.
  - Maximum difference: approximately 171.2 days.
  - 1,181 orders have discrepancies of 48 hours or less.
  - 178 orders (13.1%) have discrepancies greater than 48 hours.
  - The second-largest discrepancy is approximately 9.4 days.

- **Cause** — Undetermined. Differences may result from delayed payment-status updates or inconsistent event recording.

- **Impact** — These inconsistencies may affect analyses that depend on the sequence or duration of order-processing events.

- **Action** — Retain the existing chronology validation rule and preserve affected records. Do not modify timestamps without supporting evidence.

- **Status** — Investigated and flagged in Silver; further investigation may be needed for extreme discrepancies.

---

### Finding 003 — Missing Delivery Timestamps

- **Observation** — Eight orders marked as `delivered` have no customer delivery timestamp.

- **Additional findings:**
  - Seven orders have a carrier handoff timestamp but no customer delivery timestamp.
  - One order has neither a carrier handoff nor a customer delivery timestamp.
  - No orders marked as `shipped` were found to have a missing carrier handoff timestamp.

- **Cause** — Unknown. The missing timestamps may reflect incomplete event recording.

- **Impact** — Affected orders cannot reliably contribute to delivery-duration calculations.

- **Action** — Preserve affected records and flag them using `status_timestamp_issue`. Exclude them from calculations requiring the missing timestamps.

- **Status** — Flagged in Silver; no automatic correction or removal.

---

## Data Quality Strategy

- **Bronze** — Preserve the original source data without modification.
- **Silver** — Convert data types, validate identifiers, and flag potential quality issues.
- **Gold** — Apply analytical rules and filter flagged records when necessary.

Records with nonfatal quality issues are retained in Silver rather than automatically deleted.

This approach preserves information, supports traceability, and allows different Gold-layer analyses to apply appropriate data quality requirements.
