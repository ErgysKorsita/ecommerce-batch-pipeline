import pandas as pd

from src.transform import transform_customers, validate_customers
from src.load import load_to_parquet

def test_customers_pipeline(tmp_path):
    output_path = tmp_path / 'customers.parquet'

    df = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003'],
        'customer_unique_id': ['U001', 'U002', 'U001'], 
        'customer_zip_code_prefix': [1234, 56789, 123],
        'customer_city':['sao paulo', 'rio de janeiro', 'curitiba'],
        'customer_state': ['SP', 'RJ', 'PR']
    })

    cleaned_df = transform_customers(df)
    validate_customers(cleaned_df)
    load_to_parquet(cleaned_df, output_path)
    saved_df = pd.read_parquet(output_path)

    expected_zip_codes = ["01234", "56789", "00123"]

    for i, expected_zip in enumerate(expected_zip_codes):
        assert saved_df["customer_zip_code_prefix"].iloc[i] == expected_zip

    assert len (saved_df) == 3

    assert saved_df['customer_unique_id'].duplicated().sum() == 1