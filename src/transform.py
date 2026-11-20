import pandas as pd

def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['customer_zip_code_prefix'] = (
        df['customer_zip_code_prefix']
        .astype('string')
        .str.zfill(5)
    )

    return df

def validate_customers(df: pd.DataFrame) -> None:
    if df['customer_id'].duplicated().any():
        raise ValueError('Duplicate customer_id values found!')

    if df.isna().any().any():
        raise ValueError('Missing values found in customers dataset')