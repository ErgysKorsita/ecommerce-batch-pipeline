import pandas as pd 
import pytest 

from src.transform import transform_order_items, validate_order_items

@pytest.fixture
def valid_order_items_df():
    return pd.DataFrame({
        "order_id": ["O001", "O001", "O002", "O002"],
        "order_item_id": [1, 2, 1, 2],
        "product_id": ["P001", "P002", "P003", "P004"],
        "seller_id": ["S001", "S002", "S001", "S002"],
        "price": [100.0, 150.0, 75.0, 200.0],
        "freight_value": [10.0, 15.0, 0.0, 20.0],
        "shipping_limit_date": pd.to_datetime([
            "2017-10-02",
            "2017-10-03",
            "2017-10-04",
            "2017-10-05"
        ])
    })

def test_transform_order_items_converts_dates():
    df = pd.DataFrame({
        "shipping_limit_date": ["2018-05-10", "2018-05-15"]
    })

    result = transform_order_items(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipping_limit_date"]
    )

def test_transform_order_items_invalid_dates():
    df = pd.DataFrame({
        "shipping_limit_date": ["2018-05-10", "invalid_date"]
    })

    with pytest.raises(ValueError, match="invalid dates found"):
        transform_order_items(df)

def test_transform_order_items_preserves_missing_dates():
    df = pd.DataFrame({
        "shipping_limit_date" : ["2018-05-10", None]
    })

    result = transform_order_items(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipping_limit_date"]
    )
    assert pd.isna(result["shipping_limit_date"].iloc[1])
    assert result["shipping_limit_date"].isna().sum() == 1

def test_transform_order_items_preserves_original():
    df = pd.DataFrame({
        "shipping_limit_date": ["2018-05-10", "2018-05-15"]
    })

    result = transform_order_items(df)

    assert not pd.api.types.is_datetime64_any_dtype(
        df["shipping_limit_date"]
    )

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipping_limit_date"]
    )

def test_validate_order_items_duplicate_composite_key(valid_order_items_df):

    valid_order_items_df.loc[1, "order_item_id"] = 1
    with pytest.raises(ValueError, match = "Duplicate composite key"):
        validate_order_items(valid_order_items_df)

def test_validate_order_items_valid_composite_keys(valid_order_items_df):
    assert validate_order_items(valid_order_items_df) is None

@pytest.mark.parametrize("column", [
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id", 
    "price", 
    "freight_value"
])

def test_valid_order_items_missing_identifiers(valid_order_items_df,column):
    valid_order_items_df.loc[0,column] =  None
    with pytest.raises(ValueError, match=f"Missing values in {column}"):
        validate_order_items(valid_order_items_df)

@pytest.mark.parametrize("invalid_id", [0, -1, 1.5])

def test_validate_order_items_invalid_item_id(valid_order_items_df, invalid_id):

    valid_order_items_df["order_item_id"] = (
        valid_order_items_df["order_item_id"].astype(float)
    )

    valid_order_items_df.loc[0, "order_item_id"] = invalid_id

    with pytest.raises(ValueError, match = "Invalid order_item_id"):
        validate_order_items(valid_order_items_df)


@pytest.mark.parametrize("invalid_price", [0, -10.50])

def test_validate_order_items_invalid_price(valid_order_items_df, invalid_price):

    valid_order_items_df.loc[0, "price"] = invalid_price
    with pytest.raises(ValueError, match = "Invalid price"):
        validate_order_items(valid_order_items_df)


def test_validate_order_items_invalid_freight_value(valid_order_items_df):
    valid_order_items_df.loc[0, "freight_value"] = -5.0
    with pytest.raises(ValueError, match = "Invalid freight_value"):
        validate_order_items(valid_order_items_df)

