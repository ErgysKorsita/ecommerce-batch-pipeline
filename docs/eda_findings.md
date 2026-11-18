# EDA FINDINGS

## 1. Customers
### Finding 001 - Repeated Customer Identifiers 

- **Observation** - Over 3000 repeated occurrences of customer_unique_id.
- **Cause** - Customers can place multiple orders.
- **Impact** - customer_id and customer_unique_id serve different purposes.
- **Action** - Use customer_unique_id for customer-level analytics.
- **Status** - Expected behavior - no cleaning required.

### Finding 002 - Customer Identifiers & Duplicates

- **Observation** - No fully duplicated rows were found. customer_unique_id contains repeated values.
- **Cause** - The same customer can place multiple orders, each associated with a different customer_id. 
- **Impact** - Using customer_id for customer_level analytics could overestimate the number of unique customers. 
- **Action** - Use customer_unique_id for customer-level analytics and customer_id for joining with orders table.
- **Status** - Expected behavior - no cleaning required.

### Finding 003 - Zip Code Leading Zeros

- **Observation** - 23,995 ZIP code prefixes appear as 4-digit values instead of 5-digit values. 
- **Cause** - Likely caused by pandas interpreting ZIP codes as integers.
- **Impact** - Potential mismatches when joining with geo-location data.
- **Action** - Read ZIP code prefixes as strings and validate their length.
- **Status** - Pending validation against source CSV.

## 2. Orders

### Finding 001 - Customer Identifiers & Relationships

- **Observation** - customer_id is unique in the orders table and can be used to link orders to customer_unique_id through customers table.
- **Cause** - A new customer_id is assigned for each order, consistent with the customers table
- **Impact** - Enables relationships between orders and customers.
- **Action** - Use customer_id for joins and customer_unique_id for customer_level analysis
- **Status** - Expected behavior - no cleaning required

### Finding 002 - Incorrect Date Data Types

- **Observation** - Date columns are stored as strings rather than than timestamps.
- **Cause** - CSV files do not preserve native datetime data types. 
- **Impact** - Date comparisons and time-based calculations require conversation.
- **Action** - Convert date columns to timestamps in the Silver layer.
- **Status** - Transformation required.

### Finding 003 - Missing Order Timestamps

- **Observation** - Missing values exist in order_approved_at, order_delivered_carrier_date and order_delivered_customer_date. No missing values were found in order_status. 
- **Cause** - Potentially related to canceled, unavailable or incomplete orders.
- **Impact** - Missing timestamps can affect delivery and order processing analysis
- **Action** - Investigate missing values in relation to order_status before defining cleaning rules.
- **Status** - Further investigation required. 

### Finding 004 - Data Uniqueness and Schema Consistency

- **Observation** - No fully duplicated rows or misspelled column names were identified.
- **Cause** - No apparent duplication or column-name issues.
- **Impact** - No immediate schema corrections or row-level deduplication are necessary.
- **Action** - Preserve the existing column names and validate uniqueness during pipeline processing. 
- **Status** - No cleaning required.

### Finding 005 - Chronological Inconsistencies

- **Observation** - No invalid approval dates were found. However, 680 carrier handoff timestamps occur before approval timestamps and 20 customer delivery timestamps occur before carrier handoff timestamps.
- **Cause** - Potential timestamp recording errors, delayed system updates or operation differences.
- **Impact** - May affect order-processing duration and shipping performance calculations. 
- **Action** - Investigate affected records and define chronological validation rules in the Silver layer.
- **Status** - Potential data quality issue - investigation required.

### Finding 006 - Late Deliveries

- **Observation** - 6,535 orders were delivered after their estimated delivery date.
- **Cause** - Potential logistics or fulfillment delays, specific causes have not been investigated. 
- **Impact** - Relevant for evaluating delivery performance and customer satisfaction.
- **Action** - Use actual and estimated delivery dates to calculate delivery delays in downstream analytics.
- **Status** - Business insight - no cleaning required.

### Finding 007 - Repeated Carrier Handoff Timestamps

- **Observation** - 18,422 duplicate occurrences were identified in order_delivered_carrier_date, including 1,782 repeated missing timestamps. The remaining 16,640 are repeated non-null timestamps.
- **Cause** - Possible batch processing, scheduled carrier pickups, or simultaneous system updates. Missing values might come to order not being in curriers possession yet.
- **Impact** - Repeated timestamps do not necessarily indicate duplicated orders or invalid records.
- **Action** - Preserve repeated timestamps and investigate their frequency if necessary.
- **Status** - Potentially expected behavior - no immediate cleaning required.

### Finding 008 - Customer Delivery Timestamps

- **Observation** - 812 repeated non-null timestamps and 2,965 missing values were identified in order_delivered_customer_date. 
- **Cause** - Repeated timestamps may reflect coinciding delivery or recording times. Missing values may relate to orders that were not delivered. 
- **Impact** - Missing timestamps limit delivery-time analysis, while repeated timestamps do not necessarily indicate errors.  
- **Action** - Investigate missing delivery dates by order_status and preserve legitimate repeated timestamps. 
- **Status** - Missing values require investigation; repeated timestamps require no immediate cleaning. 

### Finding 009 - Delivery date Semantics

- **Observation** - order_delivered_carrier_date records the carrier handoff, order_delivered_customer_date records customer delivery and order_estimated_delivery_date represent the predicted delivery date.
- **Cause** - These columns represent different stages of the fulfillment process. 
- **Impact** - Enables shipping-duration calculations, chronological validation and delivery performance analysis. 
- **Action** - Use the appropriate timestamps for each metric and compare calendar dates when evaluating delivery deadlines. 
- **Status** - Expected behavior - no cleaning required. 

## 3. Products

### Finding 001 - Misspelled Column name 

- **Observation** - A spelling mistake was identified in product_name_lenght and product_description_lenght.
- **Cause** - Likely a naming error in the source dataset.
- **Impact** - May cause confusion or inconsistencies when referencing the column.
- **Action** - Rename the column during the cleaning/transformation stage.
- **Status** - Cleaning required. 

### Finding 002 - Unique Product Identifiers

- **Observation** - No duplicate product_id values were found.
- **Cause** - Each product record has a unique identifier, even when multiple products belong to the same category.
- **Impact** - product_id can be used as a unique key for the product table.
- **Action** - Preserve uniqueness during data processing.
- **Status** - Expected behavior - no cleaning required. 

### Finding 003 - No duplicate rows 

- **Observation** - No fully duplicated rows were found.
- **Cause** - Each row represents a distinct product record.
- **Impact** - No duplicate records need to be removed.
- **Action** - No action required. 
- **Status** - No cleaning required.

### Finding 004 - Missing product information

- **Observation** - No missing values in product_id. However, 610 missing values were found in each of product_category_name, product_name_length, product_description_length, and product_photos_qty. Additionally, 2 missing values were found in each of product_weight_g, product_length_cm, product_height_cm, and product_width_cm.
- **Cause** - Unknown; possibly incomplete product information.
- **Impact** - May affect category-based analytics and calculations involving product dimensions.
- **Action** - Investigate whether missing values occur in the same records and determine an appropriate handling strategy.
- **Status** - Further investigation required. 

### Finding 005 - Repeated Product Categories

- **Observation** - Multiple products share the same product_category_name.
- **Cause** - Different products can belong to the same category.
- **Impact** - product_category_name is not a unique identifier and should not be used as a primary key.
- **Action** - Use product_id for product identification.
- **Status** - Expected behavior - no cleaning required.


### Finding 006 - No negative numeric values

- **Observation** - No negative values were found in the numeric columns checked.
- **Cause** - Numeric values are non-negative in the inspected records.
- **Impact** - No negative-value anomalies were identified. 
- **Action** - No action required.
- **Status** - No cleaning required.

# 4. Sellers

### Finding 001 - Consistent column naming

- **Observation** - No spelling mistakes were identified in the column names.
- **Cause** - Column names appear correctly defined in the source dataset.
- **Impact** - No naming inconsistencies were identified. 
- **Action** - No action required.
- **Status** - No cleaning required.

### Finding 002 - Missing Leading Zeros in ZIP codes

- **Observation** - Some seller_zip_code_prefix value appear to be missing leading zeros, consistent with the customer table.
- **Cause** - ZIP codes may have been interpreted as numeric values instead of strings.
- **Impact** - May cause inconsistencies when joining location data or performing geographical analysis.
- **Action** - Investigate the raw values and preserve ZIP code prefixes as five-character strings, restoriong leading zeros where appropriate.
- **Status** - Cleaning required where leading zeros were lost.

### Finding 003 - No missing values

- **Observation** - No null values were found in any columns.
- **Cause** - All sellers records contain values for the available fields.
- **Impact** - No null-value handling is required based on the current checks.
- **Action** - No action required. 
- **Status** - No action required.

### Finding 004 - Unique Seller Identifiers 

- **Observation** - No duplicate seller_id values were found.
- **Cause** - Each seller is represented by a unique identifier.
- **Impact** - seller_id can be used as the primary key for the sellers table.
- **Action** - Preserve uniqueness during data processing.
- **Status** - Expected behavior - no cleaning required.

### Finding 005 - Valid Seller State Codes

- **Observation** - No unexpected or invalid state codes were identified in seller_state.
- **Cause** - Seller state values appear consistent with brazilian state codes.
- **Impact** - No state-code inconsistencies were identified that could affect geographical analysis.
- **Action** - No action required.
- **Status** - No action required.

### Finding 006 - No duplicated rows 

- **Observation** - No fully duplicated rows were found.
- **Cause** - Each row represents a distinct seller record.
- **Impact** - No duplicated records need to be removed.
- **Action** - No action required.
- **Status** - No action required.

# 5. Order Items 

### Finding 001 - Column Names and Data Types 

- **Observation** - No spelling mistakes detected in column names. Shipping_limit_data is stored as a string.
- **Cause** - Data values were imported from CSV without datetime conversion.
- **Impact** - Date-based calculations and comparisons may require conversion.
- **Action** - Converting shipping_limit_date to a timestamp during Silver-layer transformations.
- **Status** - Cleaning required in Silver layer.

### Finding 002 - Repeated Order Identifiers

- **Observation** - order_id contains duplicate values but no missing values.
- **Cause** - A single order can contain multiple items.
- **Impact** - order_id cannot uniquely identify individual order items.
- **Action** - Verify uniqueness of the composite key (order_id, order_item_id).
- **Status** - Expected behavior, composite key validation pending.

### Finding 003 - Data Completeness and Duplicates

- **Observation** - No missing values across all seven columns and no fully duplicated rows. Repeated values exist in order_id, order_item_id, product_id and seller_id.
- **Cause** - Orders can contain multiple items, while products and sellers can appear across different orders. Item numbering restarts for each order.
- **Impact** - Individual column duplicates are expected and do not necessarily indicate duplicate records.
- **Action** - Verify uniqueness of composite key (order_id, order_item_id).
- **Status** - No missing-value cleaning required, composite key validation pending.

### Finding 004 - Relationship between tables. 

- **Observation** - order_id, product_id and seller_id are present and can be used to relate order_items to orders_products and sellers.
- **Cause** - The dataset follows a relational structure.
- **Impact** - Enables cross-table analysis of orders, products sellers and shipping costs.
- **Action** - Validate relationships and referential integrity during Silver-layer development.
- **Status** - Expected structure - validation pending.

### Finding 005 - Price validation. 

- **Observation** - No missing, negative or zero prices. Minimum price is R$0.85, maximum R$6.735.00, mean R$120.65 and median R$74.99.
- **Cause** - Price vary across products.
- **Impact** - No obvious invalid prices detected, although extreme values may affect aggregations.
- **Action** - Preserve original values and investigate unusually high prices if necessary.
- **Status** - No immediate cleaning required.

### Finding 006 - Freight Value Validation

- **Observation** - freight_value represents the shipping charge associated with an order_item. No missing or negative values were detected. there are 383 zero-freight records. Maximum freight is R$409.68 , mean is R$19.99 and median is R$ 16.26 .
- **Cause** - Zero freight may represent free shipping; high values may reflect shipping requirements or product characteristics.
- **Impact** - Unusual freight values may affect shipping-cost analytics.
- **Action** - Preserve original values and investigate extreme freight charges.
- **Status** - Further investigation required.

### Finding 007 - Statistical Outliers

- **Observation** - IQR analysis identified 8,427 potential outliers in price and 12,1234 in freight_value.
- **Cause** - Potentially related to variation in product prices and shipping costs.
- **Impact** - Extreme values may influence statistical summaries but are not necessarily errors.
- **Action** - Preserve records and investigate relevant outliers during cross-table analysis.
- **Status** - Further investigation required.

### Finding 008 - Freight Costs Exceeding Product Prices

- **Observation** - Multiple order items have freight_value greater than price.
- **Cause** - Potentially related to product weight, dimensions, fragility or shipping distance.
- **Impact** - High freight-to-price ratios may be legitimate but warrant investigation.
- **Action** - Compare freight charges with product weight and dimensions from the products table during cross-table analysis.
- **Status** - Further investigation required.

### Finding 009 - Shipping Deadline Analysis

- **Observation** - shipping_limit_date represents the shipping deadline and may be compared with dates in the orders table.
- **Cause** - Shipping deadlines and order timestamps represent different stages of order fulfillment.
- **Impact** - Cross-table comparisons may help identify unusual fulfillment timelines.
- **Action** - Investigate shipping deadlines against relevant order timestamps after date conversion.
- **Status** - Further investigation required in Silver layer.