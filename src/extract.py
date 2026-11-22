from pathlib import Path
import pandas as pd

def extract_customers(file_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(
        file_path,
        dtype = {'customer_zip_code_prefix' : 'string'}
    )

    return df

def extract_csv(
    file_path: str | Path,
    dtype: dict | None = None
) -> pd.DataFrame:

    df = pd.read_csv(file_path, dtype=dtype)

    return df