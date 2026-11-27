
# Silver Layer - Data Cleaning Plan

## Objective

Transform raw Bronze datasets into clean, consistent, and validated Silver datasets stored in Parquet format.

## Cleaning Strategy

- Preserve original Bronze data without modifications.
- Apply transformations only when necessary.
- Investigate anomalies before modifying or removing records.
- Validate data quality before writing to Silver.
- Document all cleaning decisions.

## Dataset Cleaning Plans

### 1. Customers

| Issue | Planned Action | Status |
|---|---|---|
| ZIP code prefixes | Preserve as five-character strings with leading zeros | Implemented |
| Customer identifiers | Validate uniqueness of customer_id | Implemented |
| Repeated customer_unique_id | Preserve as expected behavior | Implemented |
| Missing values | Validate absence of unexpected nulls | Implemented |

**Implementation progress**
- Transformation: Implemented
- Validation: Implemented
- Unit tests: Passing
- Silver Parquet output: Generated
- Integration test: Passed


### 2. Orders

| Issue | Planned Action | Status |
|---|---|---|
| Date columns stored as strings | Convert five date columns to datetime | Implemented |
| Order identifiers | Validate uniqueness and absence of nulls in `order_id` | Implemented |
| Customer identifiers | Validate absence of nulls in `customer_id`; preserve for joins | Implemented |
| Missing timestamps | Preserve expected nulls; flag inconsistencies based on order status | Implemented |
| Invalid dates | Detect parsing failures without silently losing original information | Implemented |
| Date chronology | Check seven chronological conditions and flag suspicious records | Implemented |
| Order statuses | Preserve original statuses and validate relevant timestamp requirements | Implemented |
| Quality flags | Add `chronology_issue` and `status_timestamp_issue` | Implemented |

**Implementation Progress**
- Transformation: Implemented
- Validation: Implemented
- Chronology checks: Implemented
- Status-dependent timestamp checks: Implemented
- Unit tests: Passing
- Silver Parquet output: Generated
- Pipeline execution: Successful
- Automated end-to-end integration test: Pending

**Data Quality Findings**

A total of 99,441 orders were processed.

**Chronology Issues**
- 1,382 orders (1.39%) violate at least one chronological validation rule.
- 1,359 orders have carrier handoff timestamps before payment approval.
- 166 orders have carrier handoff timestamps before purchase.
- 61 orders have customer delivery timestamps before payment approval.
- 23 orders have customer delivery timestamps before carrier handoff.
- Individual rule counts overlap because orders may violate multiple conditions.

**Carrier Handoff Before Payment Approval**
- Median discrepancy: 17.17 hours.
- Mean discrepancy: 24.75 hours.
- 178 orders have discrepancies greater than 48 hours.
- Maximum discrepancy: approximately 171.2 days.

**Status-Dependent Timestamp Issues**
- Eight delivered orders have missing customer delivery timestamps.
- One of these orders also has a missing carrier handoff timestamp.
- No shipped orders were found with missing carrier handoff timestamps.

**Cleaning Decisions**
- Preserve all records with nonfatal chronology or status-timestamp issues.
- Flag affected records instead of automatically removing them.
- Do not modify inconsistent timestamps without supporting evidence.
- Use quality flags when filtering data for Gold-layer analytics.
- Keep the original order statuses unchanged.

**Documentation**
- Detailed findings: `docs/silver_data_quality.md`

---

### 3. Order Items

| Issue | Planned Action | Status |
|---|---|---|
| Shipping deadline stored as string | Convert `shipping_limit_date` to datetime | Implemented |
| Composite key | Validate uniqueness of (`order_id`, `order_item_id`) | Implemented |
| Missing values | Validate absence of nulls in required columns | Implemented |
| Order item identifiers | Validate positive integer values | Implemented |
| Product prices | Reject zero and negative prices | Implemented |
| Freight values | Reject negative freight values; allow zero | Implemented |
| Order references | Validate referential integrity against Silver Orders | Implemented |
| Product and seller references | Validate against Silver Products and Sellers | Pending |
| Shipping deadline chronology | Check deadlines against purchase and approval timestamps | Implemented |
| Quality flags | Add `shipping_deadline_issue` | Implemented |
| Statistical outliers | Preserve unless confirmed as data errors | Implemented |
| Late carrier handoff | Investigate as a fulfillment performance metric in Gold | Deferred |

**Implementation Progress**
- Transformation: Implemented
- Single-table validation: Implemented
- Reusable referential integrity validation: Implemented
- Cross-table chronology checks: Implemented
- Unit tests: Passing
- Silver Parquet output: Generated
- Pipeline execution: Successful
- Manual Silver output verification: Passed
- Automated end-to-end integration test: Pending

**Data Quality Findings**

A total of 112,650 order item records were processed.

**Referential Integrity**
- All order item records reference existing orders.
- No unmatched order identifiers were detected.
- The composite key remains unique after processing.
- Many-to-one merge validation prevents accidental row multiplication.

**Shipping Deadline Chronology**
- 127 order items (0.11%) have detected shipping deadline chronology issues.
- These records belong to 116 distinct orders.
- No shipping deadlines occur before the purchase timestamp.
- 127 shipping deadlines occur before the approval timestamp.
- 15 order items have missing approval timestamps.
- Missing approval timestamps alone do not trigger a chronology flag.

**Approval After Shipping Deadline**
- Median discrepancy: 19.58 hours.
- Mean discrepancy: 45.62 hours.
- 41 records have discrepancies greater than 48 hours.
- Maximum discrepancy: approximately 445.03 hours (18.54 days).

**Fulfillment Performance**
- 10,423 order items have carrier handoff timestamps after their shipping deadlines.
- 1,194 order items have missing carrier handoff timestamps.
- Approximately 9.35% of records with available carrier handoff timestamps exceed their shipping deadlines.
- These findings are reserved for Gold-layer analytics rather than treated as data errors.
- Carrier handoff timestamps are recorded at order level and therefore serve as a proxy for item-level fulfillment.

**Cleaning Decisions**
- Preserve all records with nonfatal shipping deadline chronology issues.
- Flag affected records using `shipping_deadline_issue`.
- Do not modify inconsistent timestamps without supporting evidence.
- Preserve missing approval timestamps without imputation.
- Preserve valid zero-freight records.
- Preserve statistical price and freight outliers unless confirmed as errors.
- Remove temporary Orders timestamps after cross-table validation.
- Defer fulfillment delay calculations to the Gold layer.

**Pipeline Dependencies**
- Bronze: `olist_order_items_dataset.csv`
- Silver: `orders.parquet`
- The Orders pipeline must execute before the Order Items pipeline.

**Silver Output**
- File: `data/silver/order_items.parquet`
- Records: 112,650
- Columns: 8
- Records with detected chronology issues: 127
- Records without detected chronology issues: 112,523
- Duplicate composite keys: 0
- Quality flag data type: Boolean

---

### 4. Products

To be defined.

### 5. Sellers

To be defined.

### 6. Payments

To be defined.

### 7. Reviews

To be defined.

### 8. Geolocation

To be defined.

### 9. Category Translations

To be defined.
