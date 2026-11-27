import pandas as pd
from pandas.core import missing

def validate_referential_integrity(
    child_df: pd.DataFrame,
    parent_df: pd.DataFrame,
    child_key: str, 
    parent_key: str
) -> None:

    missing_references = ~child_df[child_key].isin(
        parent_df[parent_key]
    )

    if missing_references.any():
        missing_count = missing_references.sum()
        raise ValueError(
            f"Referential integrity violation: "
            f"{missing_count} unmatched records in "
            f"{child_key} referencing {parent_key}"
        )


def check_shipping_deadline_chronology(
    order_items_df: pd.DataFrame, 
    orders_df: pd.DataFrame
) -> pd.DataFrame:

    order_columns =[
        "order_id",
        "order_purchase_timestamp",
        "order_approved_at"
    ]

    merged_df = pd.merge(
        left = order_items_df, 
        right = orders_df[order_columns],
        on = "order_id", 
        how = "left", 
        validate = "many_to_one"
    )
    
    deadline_before_purchase = (
        merged_df["shipping_limit_date"] 
        < merged_df["order_purchase_timestamp"]
        )
    
    deadline_before_approval = (
        merged_df["shipping_limit_date"]
        < merged_df["order_approved_at"]
    )

    merged_df["shipping_deadline_issue"] = (
        deadline_before_purchase | deadline_before_approval
    )

    merged_df = merged_df.drop(
        columns = [
            "order_purchase_timestamp", 
            "order_approved_at"
        ]
    )

    return merged_df