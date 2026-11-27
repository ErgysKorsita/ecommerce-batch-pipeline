import pandas as pd

from pathlib import Path
from src.extract import extract_customers
from src.transform import transform_customers, validate_customers
from src.load import load_to_parquet
from src.transform import (
    transform_orders, 
    validate_orders, 
    check_order_chronology, 
    check_order_status_timestamps,
    transform_order_items, 
    validate_order_items
)

from src.extract import extract_csv

from src.validation import (
    validate_referential_integrity,
    check_shipping_deadline_chronology
)

def run_customers_pipeline() -> None:
    bronze_path = Path(
        "data/bronze/ecommerce_Brazil_dataset/olist_customers_dataset.csv"
    )

    silver_path = Path("data/silver/customers.parquet")

    # Extract 
    df = extract_customers(bronze_path)

    # Transform
    df_silver = transform_customers(df)

    # Validate
    validate_customers(df_silver)

    # Load 
    load_to_parquet(df_silver, silver_path)

    print(f'Customers pipeline completed: {len(df_silver)} rows processed.')

def run_orders_pipeline() -> None:
    bronze_path = Path(
        "data/bronze/ecommerce_Brazil_dataset/olist_orders_dataset.csv"
    )

    silver_path = Path("data/silver/orders.parquet")

    # Extract 
    df = extract_csv(bronze_path)

    # Transform
    df_silver = transform_orders(df)

    # Validate
    validate_orders(df_silver)

    # Data quality checks 
    df_silver = check_order_chronology(df_silver)
    df_silver = check_order_status_timestamps(df_silver)

    # Load
    load_to_parquet(df_silver, silver_path)

    print(f"Orders pipeline completed: {len(df_silver)} rows processed.")

def run_order_items_pipeline() -> None:

    bronze_path = Path(
        "data/bronze/ecommerce_Brazil_dataset/"
        "olist_order_items_dataset.csv"
    )

    orders_path = Path("data/silver/orders.parquet")

    silver_path = Path("data/silver/order_items.parquet")

    # Extract
    df = extract_csv(bronze_path)

    # Transform
    df_silver = transform_order_items(df)

    # Validate
    validate_order_items(df_silver)

    # Load parent dataset
    orders_df = pd.read_parquet(orders_path)

    # Validate referential integrity
    validate_referential_integrity(
        child_df=df_silver,
        parent_df=orders_df,
        child_key="order_id",
        parent_key="order_id"
    )

    # Data quality checks
    df_silver = check_shipping_deadline_chronology(
        order_items_df=df_silver,
        orders_df=orders_df
    )

    # Load
    load_to_parquet(df_silver, silver_path)

    print(f"Order Items pipeline completed: {len(df_silver)} rows processed.")

if __name__ == "__main__":
    run_customers_pipeline()
    run_orders_pipeline()
    run_order_items_pipeline()



