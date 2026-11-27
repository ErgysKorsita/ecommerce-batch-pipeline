import pandas as pd 
import pytest 

from src.validation import validate_referential_integrity

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