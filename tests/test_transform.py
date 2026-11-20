import pandas as pd

from src.transform import transform_customers

def test_customer_zip_prefix():
    df = pd.DataFrame({
        'customer_zip_code_prefix': [1234, 12345, 987]
    })

    result = transform_customers(df)

    assert result['customer_zip_code_prefix'].tolist() == [
        "01234", "12345", '00987'
    ]

import pytest
from src.transform import validate_customers

def test_duplicate_customer_ids():
    df = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C001']
    })

    with pytest.raises(ValueError):
        validate_customers(df)


def test_missing_customer_values():
    df = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003'],
        'customer_city': ['Sao Paulo', None, 'Rio de Janeiro']
    })

    with pytest.raises(ValueError):
        validate_customers(df)


def test_valid_customers():
    df = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003'],
        'customer_unique_id': ['U001', 'U001', 'U002'],
        'customer_zip_code_prefix': ['01234', '12345', '00987']
    })

def test_customer_row_count():
    df = pd.DataFrame({
        'customer_zip_code_prefix': [1234, 12345, 987]
    })

    result = transform_customers(df)

    assert len(result) == len(df)