from multiprocessing import Value
import pandas as pd 
import pytest 

from src.transform import check_order_chronology, check_order_status_timestamps, transform_orders, validate_orders


def test_transform_orders_converts_dates():

    df = pd.DataFrame({
        "order_purchase_timestamp": ["2018-05-10"],
        "order_approved_at": ["2018-05-11"],
        "order_delivered_carrier_date": ["2018-05-12"],
        "order_delivered_customer_date": ["2018-05-15"],
        "order_estimated_delivery_date": ["2018-05-20"]
    })

    cleaned_df = transform_orders(df)

    for column in df.columns:
        assert pd.api.types.is_datetime64_any_dtype(cleaned_df[column])

def test_transform_orders_invalid_dates():
    df = pd.DataFrame({
        'order_purchase_timestamp': ['invalid_date'], 
        'order_approved_at': ['2018-05-11'],
        'order_delivered_carrier_date': ['2018-05-12'],
        'ordered_delivered_customer_date': ['2018-05-15'],
        'order_estimated_delivery_date': ['2018-05-20']
    })

    with pytest.raises(ValueError, match='invalid dates found'):
        transform_orders(df)

def test_validate_orders_duplicate_ids():
    df = pd.DataFrame({
        'order_id': ['O001', 'O002', 'O001'], 
        'customer_id': ['C001', 'C002', 'C003']
    })

    with pytest.raises(ValueError, match='Duplicate order_id'):
        validate_orders(df)

def test_validate_orders_missing_order_id():
    df = pd.DataFrame({
        'order_id': ['O001', None, 'O003'], 
        'customer_id': ['C001', 'C002', 'C003']
    })

    with pytest.raises(ValueError, match = 'Missing order_id'):
        validate_orders(df)

def test_validate_orders_missing_customer_id():
    df = pd.DataFrame({
    "order_id": ["O001", "O002", "O003"],
    "customer_id": ["C001", None, "C003"]
    })

    with pytest.raises(ValueError, match = "Missing customer_id"):
        validate_orders(df)

def test_validate_orders_valid_data():
    df = pd.DataFrame({
        "order_id": ["O001", "O002", "O003"],
        "customer_id": ["C001", "C002", "C003"]
    })

    result = validate_orders(df)

    assert result is None

def test_check_order_chronology():
    df = pd.DataFrame({
        "order_purchase_timestamp": pd.to_datetime([
            "2018-05-10",
            "2018-05-10",
            "2018-05-10"
        ]),

        "order_approved_at": pd.to_datetime([
            "2018-05-10",
            "2018-05-10",
            "2018-05-10"
        ]),

        "order_delivered_carrier_date": pd.to_datetime([
            "2018-05-12",
            "2018-05-09",
            None
        ]),

         "order_delivered_customer_date": pd.to_datetime([
            "2018-05-15",
            "2018-05-15",
            None
        ]),

        "order_estimated_delivery_date": pd.to_datetime([
        "2018-05-20",
        "2018-05-20",
            "2018-05-20"
        ])
    })

    result = check_order_chronology(df)

    assert result['chronology_issue'].tolist() == [False, True, False]

def test_chronology_customer_before_carrier():
    df = pd.DataFrame({
        "order_purchase_timestamp": pd.to_datetime(["2018-05-10"]),
        'order_approved_at': pd.to_datetime(['2018-05-09']),
        "order_delivered_carrier_date": pd.to_datetime(["2018-05-12"]),
        "order_delivered_customer_date": pd.to_datetime(["2018-05-11"]),
        'order_estimated_delivery_date': pd.to_datetime(["2018-05-20"])
    })

    result = check_order_chronology(df)

    assert result['chronology_issue'].iloc[0] == True

def test_chronology_approval_before_purchase():
    df = pd.DataFrame({
        'order_purchase_timestamp': pd.to_datetime(['2018-05-10']),
        'order_approved_at': pd.to_datetime(['2018-05-09']),
        'order_delivered_carrier_date': pd.to_datetime(['2018-05-11']),
        'order_delivered_customer_date': pd.to_datetime(['2018-05-15']),
        'order_estimated_delivery_date': pd.to_datetime(["2018-05-20"])
    })

    result = check_order_chronology(df)

    assert result['chronology_issue'].iloc[0] == True

def test_chronology_customer_before_purchase():
    df = pd.DataFrame({
    "order_purchase_timestamp": pd.to_datetime(["2018-05-10"]),
    "order_approved_at": pd.to_datetime(["2018-05-11"]),
    "order_delivered_carrier_date": pd.to_datetime([None]),
    "order_delivered_customer_date": pd.to_datetime(["2018-05-09"]),
    'order_estimated_delivery_date': pd.to_datetime(["2018-05-20"])
    })

    result = check_order_chronology(df)

    assert result['chronology_issue'].iloc[0] == True

def test_chronology_carrier_before_approval():
    df = pd.DataFrame({
    "order_purchase_timestamp": pd.to_datetime(["2018-05-10"]),
    "order_approved_at": pd.to_datetime(["2018-05-11"]),
    "order_delivered_carrier_date": pd.to_datetime(['2018-05-10']),
    "order_delivered_customer_date": pd.to_datetime(["2018-05-12"]),
    'order_estimated_delivery_date': pd.to_datetime(["2018-05-20"])
    })

    result = check_order_chronology(df)

    assert result['chronology_issue'].iloc[0] == True

def test_chronology_customer_before_approval():
    df = pd.DataFrame({
    "order_purchase_timestamp": pd.to_datetime(["2018-05-10"]),
    "order_approved_at": pd.to_datetime(["2018-05-12"]),
    "order_delivered_carrier_date": pd.to_datetime([None]),
    "order_delivered_customer_date": pd.to_datetime(["2018-05-11"]),
    'order_estimated_delivery_date': pd.to_datetime(["2018-05-20"])
    })

    result = check_order_chronology(df)
    assert result['chronology_issue'].iloc[0] == True

def test_chronology_estimated_before_purchase():
    df = pd.DataFrame({
        "order_purchase_timestamp": pd.to_datetime(["2018-05-10"]),
        "order_approved_at": pd.to_datetime(["2018-05-10"]),
        "order_delivered_carrier_date": pd.to_datetime(["2018-05-11"]),
        "order_delivered_customer_date": pd.to_datetime(["2018-05-15"]),
        "order_estimated_delivery_date": pd.to_datetime(["2018-05-08"])
    })

    result = check_order_chronology(df)

    assert result['chronology_issue'].iloc[0] == True

def test_chronology_valid_order():
    df = pd.DataFrame({
    "order_purchase_timestamp": pd.to_datetime(["2018-05-10"]),
    "order_approved_at": pd.to_datetime(["2018-05-10"]),
    "order_delivered_carrier_date": pd.to_datetime(["2018-05-12"]),
    "order_delivered_customer_date": pd.to_datetime(["2018-05-15"]),
    "order_estimated_delivery_date": pd.to_datetime(["2018-05-20"])
    })

    result = check_order_chronology(df)

    assert result["chronology_issue"].iloc[0] == False

def test_chronology_preserves_original():
    df = pd.DataFrame({
    "order_purchase_timestamp": pd.to_datetime(["2018-05-10"]),
    "order_approved_at": pd.to_datetime(["2018-05-10"]),
    "order_delivered_carrier_date": pd.to_datetime(["2018-05-12"]),
    "order_delivered_customer_date": pd.to_datetime(["2018-05-15"]),
    "order_estimated_delivery_date": pd.to_datetime(["2018-05-20"])
    })

    result = check_order_chronology(df)

    assert "chronology_issue" not in df.columns
    "chronology_issue" in result.columns

def test_status_delivered_missing_timestamp():
    df = pd.DataFrame({
        "order_status": ["delivered"],
        "order_delivered_customer_date": pd.to_datetime([None]),
        "order_delivered_carrier_date": pd.to_datetime(["2018-05-14"])
    })

    result = check_order_status_timestamps(df)

    assert result["status_timestamp_issue"].iloc[0] == True

def test_status_delivered_valid_timestamp():
    df = pd.DataFrame({
        "order_status": ["delivered"],
        "order_delivered_customer_date": pd.to_datetime(["2018-05-15"]),
        "order_delivered_carrier_date": pd.to_datetime(["2018-05-14"])
    })

    result = check_order_status_timestamps(df)

    assert result["status_timestamp_issue"].iloc[0] == False

def test_status_canceled_missing_timestamp():
    df = pd.DataFrame({
        "order_status": ["canceled"],
        "order_delivered_customer_date": pd.to_datetime([None]),
        "order_delivered_customer_date": pd.to_datetime([None]),
        "order_delivered_carrier_date": pd.to_datetime([None])
    })

    result = check_order_status_timestamps(df)

    assert result["status_timestamp_issue"].iloc[0] == False

def  test_status_shipped_missing_carrier_timestamp():
    df = pd.DataFrame({
        "order_status": ["shipped"],
        "order_delivered_carrier_date": pd.to_datetime([None]),
        "order_delivered_customer_date": pd.to_datetime([None]),
        "order_delivered_customer_date": pd.to_datetime([None])
    })

    result = check_order_status_timestamps(df)

    assert result["status_timestamp_issue"].iloc[0] == True

def test_status_shipped_carrier_timestamp():
    df = pd.DataFrame({
        "order_status": ["shipped"],
        "order_delivered_carrier_date": pd.to_datetime(["2018-05-15"]),
        "order_delivered_customer_date": pd.to_datetime([None])
    })

    result = check_order_status_timestamps(df)

    assert result["status_timestamp_issue"].iloc[0] == False

def test_status_timestamps_preserves_original():
    df = pd.DataFrame({
        "order_status": ["delivered"],
        "order_delivered_carrier_date": pd.to_datetime(["2018-05-14"]),
        "order_delivered_customer_date": pd.to_datetime(["2018-05-15"])
    })

    result = check_order_status_timestamps(df)

    assert "status_timestamp_issue" not in df.columns
    assert "status_timestamp_issue" in result.columns