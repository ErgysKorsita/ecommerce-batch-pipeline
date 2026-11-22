
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

To be defined.

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
