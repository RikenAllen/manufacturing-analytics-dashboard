import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw/ai4i2020.csv")

# Loads the Dataset
def load_raw_data():
    if not RAW_DATA.exists():
        raise FileNotFountError(f"Data not found at location: {RAW_DATA}")

    df = pd.read_csv(RAW_DATA)
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