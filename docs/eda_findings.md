# EDA FINDINGS

## 1. Customers
### Finding 001 - Repeated Customer Identifiers 

- **Observation** - Over 3000 repeated occurrances of customer_unique_id.
- **Cause** - Customers can place multiple orders.
- **Impact** - customer_id and customer_unique_id serve different purposes.
- **Action** - Use customer_unqiue_id for customer-level analytics.
- **Status** - Expected behaviour - no cleaning required.

### Finding 002 - Customer Identifiers & Duplicates

- **Observation** - No fully duplicated rows were found. customer_unique_id contains repeated values.
- **Cause** - The same customer can place multiple orders, each associated with a different customer_id. 
- **Impact** - Using customer_id for customer_level analytics could overestimate the number of unique customers. 
- **Action** - Use customer_unique_id for customer-level analytics and customer_id for joining with orders table.
- **Status** - Expected behaviour - no cleaning required.

### Finding 003 - Zip Code Leading Zeros

- **Observation** - 23,995 ZIP code prefixes apper as 4-digit values instead of 5-digit values. 
- **Cause** - Likely caused by pandas interpreting ZIP codes as integers.
- **Impact** - Ptential mismatches when joining with geolocation data.
- **Action** - Read ZIP code prefixes as strings and valiudate their length.
- **Status** - Pending validation against source CSV.