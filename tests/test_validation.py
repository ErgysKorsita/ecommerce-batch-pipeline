import pandas as pd 
import pytest 

from src.validation import validate_referential_integrity, check_shipping_deadline_chronology

def test_validate_referential_integrity_valid_references():

    child_df = pd.DataFrame({
        "order_id": ["O001", "O002", "O003"]
    })

    parent_df = pd.DataFrame({
        "order_id": ["O001", "O002", "O003"]
    })

    result = validate_referential_integrity(
        child_df=child_df,
        parent_df=parent_df,
        child_key="order_id",
        parent_key="order_id"
    )

    assert result is None 

def test_validate_referential_integrity_invalid_reference():

    child_df = pd.DataFrame({
        "order_id": ["O001", "O002", "O004"]
    })

    parent_df = pd.DataFrame({
        "order_id": ["O001", "O002", "O003"]
    })

    

    with pytest.raises(ValueError, match = "Referential integrity violation"):
        validate_referential_integrity(
            child_df=child_df,
            parent_df=parent_df,
            child_key="order_id",
            parent_key="order_id"
        )

def test_validate_referential_integrity_multiple_invalid_references():

    child_df = pd.DataFrame({
        "order_id": ["O001", "O004", "O005", "O004"]
    })

    parent_df = pd.DataFrame({
        "order_id": ["O001", "O002", "O003"]
    })

    with pytest.raises(ValueError, match = "3 unmatched records"):
        validate_referential_integrity(
            child_df=child_df,
            parent_df=parent_df,
            child_key="order_id",
            parent_key="order_id"
        )

def test_validate_referential_integrity_repeated_child_keys():

    child_df = pd.DataFrame({
        "order_id": ["O001", "O001", "O002", "O003"]
    })

    parent_df = pd.DataFrame({
        "order_id": ["O001", "O002", "O003"]
    })

    result = validate_referential_integrity(
        child_df=child_df,
        parent_df=parent_df,
        child_key="order_id",
        parent_key="order_id"
    )

    assert result is None 

def test_validate_referential_integrity_unused_parent_key():

    child_df = pd.DataFrame({
    "order_id": ["O001", "O002"]
    })

    parent_df = pd.DataFrame({
        "order_id": ["O001", "O002", "O003", "O004"]
    })

    result = validate_referential_integrity(
        child_df=child_df,
        parent_df=parent_df,
        child_key="order_id",
        parent_key="order_id"
    )

    assert result is None

def test_validate_referential_integrity_different_column_names():

    child_df = pd.DataFrame({
        "customer_id": ["C001", "C002", "C003"]
    })

    parent_df = pd.DataFrame({
        "id": ["C001", "C002", "C003"]
    })

    result = validate_referential_integrity(
        child_df=child_df,
        parent_df=parent_df,
        child_key="customer_id",
        parent_key="id"
    )

    assert result is None

def test_shipping_deadline_chronology_valid():

    order_items_df = pd.DataFrame({
        "order_id": ["O001"],
        "shipping_limit_date": pd.to_datetime(["2018-01-05"])
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-01"]),
        "order_approved_at": pd.to_datetime(["2018-01-02"])
    })

    result = check_shipping_deadline_chronology(
        order_items_df = order_items_df, 
        orders_df = orders_df
    )

    assert result["shipping_deadline_issue"].tolist() == [False]

def test_shipping_deadline_before_purchase():

    order_items_df = pd.DataFrame({
        "order_id": ["O001"],
        "shipping_limit_date": pd.to_datetime(["2018-01-01"])
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-03"]),
        "order_approved_at": pd.to_datetime(["2018-01-04"])
    })

    result = check_shipping_deadline_chronology(
        order_items_df = order_items_df, 
        orders_df = orders_df
    )

    assert result["shipping_deadline_issue"].tolist() == [True]

def test_shipping_deadline_before_approval():

    order_items_df = pd.DataFrame({
        "order_id": ["O001"],
        "shipping_limit_date": pd.to_datetime(["2018-01-03"])
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-01"]),
        "order_approved_at": pd.to_datetime(["2018-01-05"])
    })

    result = check_shipping_deadline_chronology(
        order_items_df = order_items_df, 
        orders_df = orders_df
    )

    assert result["shipping_deadline_issue"].tolist() == [True]


def test_shipping_deadline_missing_approval():

    order_items_df = pd.DataFrame({
        "order_id": ["O001"],
        "shipping_limit_date": pd.to_datetime(["2018-01-05"])
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-01"]),
        "order_approved_at": pd.to_datetime([None])
    })

    result = check_shipping_deadline_chronology(
        order_items_df = order_items_df, 
        orders_df = orders_df
    )

    assert result["shipping_deadline_issue"].tolist() == [False]

def test_shipping_deadline_before_purchase_missing_approval():

    order_items_df = pd.DataFrame({
        "order_id": ["O001"],
        "shipping_limit_date": pd.to_datetime(["2018-01-01"])
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-03"]),
        "order_approved_at": pd.to_datetime([None])
    })

    result = check_shipping_deadline_chronology(
        order_items_df = order_items_df, 
        orders_df = orders_df
    )

    assert result["shipping_deadline_issue"].tolist() == [True]

def test_shipping_deadline_equal_to_approval():

    order_items_df = pd.DataFrame({
        "order_id": ["O001"],
        "shipping_limit_date": pd.to_datetime(["2018-01-03"])
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-01"]),
        "order_approved_at": pd.to_datetime(["2018-01-03"])
    })

    result = check_shipping_deadline_chronology(
        order_items_df = order_items_df, 
        orders_df = orders_df
    )

    assert result["shipping_deadline_issue"].tolist() == [False]

def test_shipping_deadline_preserves_original_data():

    order_items_df = pd.DataFrame({
        "order_id": ["O001", "O001", "O002"],
        "order_item_id": [1, 2, 1],
        "shipping_limit_date": pd.to_datetime([
            "2018-01-05",
            "2018-01-06",
            "2018-01-07"
        ]),
        "price": [100.0, 150.0, 200.0]
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001", "O002"],
        "order_purchase_timestamp": pd.to_datetime([
            "2018-01-01",
            "2018-01-02"
        ]),
        "order_approved_at": pd.to_datetime([
            "2018-01-03",
            "2018-01-04"
        ])
    })

    result = check_shipping_deadline_chronology(
        order_items_df = order_items_df, 
        orders_df = orders_df
    )

    assert len(result) == len(order_items_df)
    assert result.shape[1] == order_items_df.shape[1] + 1
    pd.testing.assert_frame_equal(
        result[order_items_df.columns],
        order_items_df
    )
    assert "order_purchase_timestamp" not in result.columns
    assert "order_approved_at" not in result.columns
    assert result["shipping_deadline_issue"].tolist() == [
        False, False, False
    ]

def test_shipping_deadline_duplicate_parent_keys():

    order_items_df = pd.DataFrame({
        "order_id": ["O001", "O001"],
        "order_item_id": [1, 2],
        "shipping_limit_date": pd.to_datetime([
            "2018-01-05",
            "2018-01-06"
        ])
    })

    orders_df = pd.DataFrame({
        "order_id": ["O001", "O001"],
        "order_purchase_timestamp": pd.to_datetime([
            "2018-01-01",
            "2018-01-02"
        ]),
        "order_approved_at": pd.to_datetime([
            "2018-01-03",
            "2018-01-04"
        ])
    })

    with pytest.raises(pd.errors.MergeError):
        check_shipping_deadline_chronology(
            order_items_df = order_items_df, 
            orders_df = orders_df
        )