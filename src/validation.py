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