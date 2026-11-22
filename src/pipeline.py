from pathlib import Path
from src.extract import extract_customers
from src.transform import transform_customers, validate_customers
from src.load import load_to_parquet
from src.transform import (
    transform_orders, 
    validate_orders, 
    check_order_chronology, 
    check_order_status_timestamps,
)
from src.extract import extract_csv

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

if __name__ == "__main__":
    run_customers_pipeline()
    run_orders_pipeline()



