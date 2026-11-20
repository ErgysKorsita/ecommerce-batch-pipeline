from pathlib import Path
import pandas as pd

def load_to_parquet(df: pd.DataFrame, file_path:str | Path) -> None:
    file_path = Path(file_path)

    file_path.parent.mkdir(parents = True, exist_ok = True)

    df.to_parquet(file_path, engine='pyarrow', index = False)
