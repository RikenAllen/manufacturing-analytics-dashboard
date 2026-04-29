import pandas as pd
from ..config import RAW_DATA_PATH

# Loads the Dataset
def load_raw_data():
    if not RAW_DATA_PATH.exists():
        raise FileNotFountError(f"Data not found at location: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH)
    return df

if __name__ == "__main__":
    df = load_raw_data()

    print("Data loaded")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())