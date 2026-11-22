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

def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    date_columns = [ 
        'order_purchase_timestamp', 
        'order_approved_at', 
        'order_delivered_carrier_date',
        'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]

    for column in date_columns:
        missing_before = df[column].isna().sum()

        df[column] = pd.to_datetime(df[column], errors='coerce')

        missing_after = df[column].isna().sum()

        invalid_dates = missing_after - missing_before

        if invalid_dates > 0:
            raise ValueError(
            f'Column {column}: {invalid_dates} invalid dates found'
        )
    
    return df

def validate_orders(df: pd.DataFrame)  -> None:
    if df["order_id"].duplicated().any():
        raise ValueError("Duplicate order_id values found!")

    if df["order_id"].isna().any():
        raise ValueError("Missing order_id values found!")

    if df["customer_id"].isna().any():
        raise ValueError("Missing customer_id values found!")
    
def check_order_chronology(df: pd.DataFrame):
    df = df.copy()


    carrier_before_purchase = (
        df['order_delivered_carrier_date']
        < df['order_purchase_timestamp']
    ) 

    customer_before_carrier = (
        df['order_delivered_customer_date']
        < df['order_delivered_carrier_date']
    )

    approval_before_purchase = (
        df['order_approved_at']
        < df['order_purchase_timestamp']
    )

    customer_before_purchase = (
        df['order_delivered_customer_date']
        < df['order_purchase_timestamp']
    )

    carrier_before_approval = (
        df['order_delivered_carrier_date']
        < df['order_approved_at']
    )

    customer_before_approval = (
        df['order_delivered_customer_date']
        < df['order_approved_at']
    )

    estimated_before_purchase = (
        df['order_estimated_delivery_date'] 
        < df['order_purchase_timestamp']
    )

    df['chronology_issue'] = (
        carrier_before_purchase  
        | customer_before_carrier
        | approval_before_purchase
        | customer_before_purchase
        | carrier_before_approval
        | customer_before_approval
        | estimated_before_purchase
    )
    return df