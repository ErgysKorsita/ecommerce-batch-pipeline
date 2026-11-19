
# Exploratory Data Analysis — Findings

> **Scope:** Preliminary EDA of the nine Olist e-commerce source datasets. The notebook contains the underlying checks; this document summarizes decisions and follow-up work. Findings flagged for investigation are **not** confirmed data errors.

## Executive Summary

The datasets are generally usable for the planned batch pipeline.

The main Silver-layer work includes:
- Parsing timestamps.
- Preserving five-character ZIP code prefixes.
- Correcting misspelled product column names.
- Validating relationships and payment sequences.
- Handling incomplete product and category information.
- Investigating unusual dates, coordinates, payments, and shipping charges.

**Important:** Repeated business identifiers and statistical outliers are not inherently data errors.

---

## Dataset Findings

### 1. Customers

**Baseline:**
- No missing values or fully duplicated rows.
- `customer_id` identifies individual customer records.
- `customer_unique_id` can repeat when customers place multiple orders (over 3,000 repeated occurrences).

**Follow-up:**
- 23,995 ZIP code prefixes appear with four rather than five digits.
- Verify ZIP formatting against the raw CSV.
- Preserve ZIP prefixes as five-character strings.
- Use `customer_id` for joins with Orders and `customer_unique_id` for customer-level analytics.

### 2. Orders

**Baseline:**
- `customer_id` is unique in this table.
- No fully duplicated rows or column-name spelling issues.
- `order_status` contains no missing values.
- Date columns were imported as strings.

**Follow-up:**
- Convert date columns to timestamps in Silver.
- Investigate missing approval, carrier-handoff, and customer-delivery timestamps by `order_status`.
- Investigate **680** carrier-handoff timestamps occurring before approval and **20** customer deliveries occurring before carrier handoff.
- **6,535** orders were delivered after their estimated delivery date. This is a business metric, not a cleaning issue.
- Repeated carrier-handoff timestamps (16,640 repeated non-null occurrences; 1,782 repeated missing occurrences) and customer-delivery timestamps (812 repeated non-null occurrences; 2,965 missing values) do not automatically indicate duplicated orders.

**Date semantics:**
- `order_delivered_carrier_date`: Carrier handoff.
- `order_delivered_customer_date`: Customer delivery.
- `order_estimated_delivery_date`: Expected delivery date.

### 3. Products

**Baseline:**
- `product_id` is unique.
- No fully duplicated rows.
- Repeated product categories are expected.
- No negative values in checked numeric columns.

**Follow-up:**
- Rename `product_name_lenght` and `product_description_lenght` to use `length` in Silver.
- **610** missing values in each of category, name length, description length, and photo quantity.
- **2** missing values in each of weight, length, height, and width.
- Investigate whether missing attributes occur in the same product records.

### 4. Sellers

**Baseline:**
- Unique `seller_id`.
- No missing values or fully duplicated rows.
- No column-name spelling issues.
- No unexpected state codes.

**Follow-up:**
- Seller ZIP prefixes may have lost leading zeros.
- Verify the raw values and preserve ZIP prefixes as five-character strings.

### 5. Order Items

**Baseline:**
- No missing values or fully duplicated rows.
- Repeated `order_id`, `product_id`, `seller_id`, and `order_item_id` values are expected.
- The composite key (`order_id`, `order_item_id`) was verified unique.
- Identifiers support relationships with Orders, Products, and Sellers.

**Follow-up:**
- Convert `shipping_limit_date` to timestamp in Silver. All checked values parsed successfully.
- Prices contain no missing, zero, or negative values.
  - Minimum: R$0.85
  - Maximum: R$6,735.00
  - Mean: R$120.65
  - Median: R$74.99
- Freight contains no missing or negative values.
  - Zero freight: 383 records
  - Maximum: R$409.68
  - Mean: R$19.99
  - Median: R$16.26
- IQR analysis identified **8,427** price outliers.
- Freight outlier count requires verification against the notebook (originally recorded as `12,1234`).
- Some freight charges exceed product prices. Investigate relationships with product dimensions, weight, and shipping distance.
- Preserve statistical outliers unless business-rule validation identifies actual errors.

### 6. Order Payments

**Baseline:**
- No missing values, fully duplicated rows, or column-name spelling issues.
- Repeated `order_id` values are expected.
- `payment_sequential` identifies separate payment entries, not installments.
- Payment sequences range from 1 to 29 (mean 1.09, median 1).
- One investigated order contained 29 voucher entries and another payment entry.

**Follow-up:**
- Investigate `payment_type = not_defined`.
- Investigate **9** zero-value payments.
- Payment values:
  - Reported maximum: R$13,663.08
  - Mean: R$154.10
  - Median: R$100.00
- Investigate **2** records with zero installments.
- Installments range up to 24 (mean 2.85, median 1).
- **80 orders** have payment sequences starting at 2:
  - 78 contain only sequence 2.
  - 2 contain sequences 2 and 3.
- IQR identified:
  - 7,981 payment-value outliers.
  - 4,526 payment-sequence outliers.
  - 6,331 installment outliers.
- Aggregate payments and order items separately by order before comparing totals to avoid inflated results from many-to-many joins.

**Verification:** The original findings contain two different maximum payment values (R$13,663.08 and R$13,664.08). Confirm the correct value in the notebook.

### 7. Order Reviews

**Baseline:**
- Missing review titles and messages are expected because comments are optional.
- No missing values in other columns.
- No fully duplicated rows or column-name spelling issues.
- Review scores fall within the expected range of 1–5 and are predominantly positive.
- No chronological inconsistencies between review creation and answer timestamps.

**Follow-up:**
- `review_id` and `order_id` contain repeated values.
- Investigate identifier repetition and join cardinality before aggregating reviews.
- Convert `review_creation_date` and `review_answer_timestamp` to timestamps in Silver.

### 8. Geolocation

**Baseline:**
- No missing values or column-name spelling issues.
- 27 distinct state codes, consistent with Brazil's 26 states and Federal District.
- All coordinates fall within globally valid latitude and longitude ranges.

**Follow-up:**
- **245,733** ZIP prefixes contain four digits.
- **754,430** ZIP prefixes contain five digits.
- Preserve five-character ZIP prefixes, restoring leading zeros where appropriate.
- **42** coordinates fall outside Brazil's approximate geographical boundaries. Investigate before correcting or excluding them.
- Approximately **19,000** unique ZIP prefixes exist across approximately **1 million** records.
- Multiple coordinates can share the same ZIP prefix.
- Create a one-row-per-prefix geolocation lookup with a documented representative-coordinate rule to avoid row multiplication during joins.

### 9. Product Category Translations

**Baseline:**
- No missing values.
- No duplicated category identifiers or fully duplicated rows.
- No column-name spelling issues.
- Suitable as a category translation lookup table.

**Follow-up:**
- Two categories have no English translations:
  - `portateis_cozinha_e_preparadores_de_alimentos`
  - `pc_gamer`
- Add translations or implement a fallback strategy.
- Avoid inner joins that silently exclude products with missing translations.

---

## Silver-Layer Action Checklist

- [ ] **Data types:** Convert Orders, Order Items, and Reviews date columns to timestamps.
- [ ] **ZIP prefixes:** Verify source formatting and preserve five-character strings in Customers, Sellers, and Geolocation.
- [ ] **Schema:** Correct the two misspelled `*_lenght` product column names.
- [ ] **Keys and relationships:** Validate foreign keys, composite keys, and repeated review identifiers.
- [ ] **Geolocation:** Create a unique ZIP-prefix lookup and investigate 42 out-of-bounds coordinates.
- [ ] **Missing data:** Investigate missing order timestamps and product attributes.
- [ ] **Payments:** Investigate undefined payment types, zero values, unusual payment sequences, and order-level totals.
- [ ] **Categories:** Handle the two missing category translations.
- [ ] **Business anomalies:** Investigate chronological inconsistencies, unusual freight charges, and relevant monetary outliers.
- [ ] **Verification:** Confirm the freight-outlier count and maximum payment value against the EDA notebook.

---

## Deferred Analytics

The following topics are reserved for downstream analysis rather than automatic data cleaning:

- Late deliveries and fulfillment performance.
- Customer review scores and satisfaction.
- Freight-to-price ratios.
- Relationships between shipping costs, product dimensions, and geography.
- Payment patterns and order-level financial analysis.

The EDA notebook remains the reproducible source for detailed checks, distributions, and exploratory calculations.
