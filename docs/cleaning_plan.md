
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
- Integration test: Pending


### 2. Orders

To be defined.

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
