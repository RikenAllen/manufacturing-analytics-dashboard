import pandas as pd

from src.config import PROCESSED_DATA_PATH
from src.data.load_data import load_raw_data


# Schema validation

def validate_schema(df: pd.DataFrame):

    EXPECTED_COLUMNS = {
        "entry_temperature",
        "exit_temperature",
        "rolling_speed",
        "strip_thickness",
        "material_grade",
        "deformation_resistance",
        "friction_coefficient",
        "roll_diameter",
        "reduction_ratio",
        "strain_rate",
        "lubrication_type",
        "material_grade_encoded",
        "lubrication_type_encoded",
        "bending_force"
        
    }

    missing_columns = EXPECTED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")
    

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    newDf = df.copy()

    newDf.columns = (
        newDf.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    return newDf

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().copy()


# This function enforces columns to be of a specific datatype
# Ensures numerical data is a number
# Object type data becomes categorical for better semantics and memory efficiency
# Replaces bad values with NaN
def enforce_data_types(df: pd.DataFrame) -> pd.DataFrame:
    newDf = df.copy()

    numeric_cols = [
        "entry_temperature",
        "exit_temperature",
        "rolling_speed",
        "strip_thickness",
        "deformation_resistance",
        "friction_coefficient",
        "roll_diameter",
        "reduction_ratio",
        "strain_rate",
        "material_grade_encoded",
        "lubrication_type_encoded",
        "bending_force",
    ]

    for col in numeric_cols:
        newDf[col] = pd.to_numeric(newDf[col], errors="coerce")

    newDf["material_grade"] = newDf["material_grade"].astype("category")
    newDf["lubrication_type"] = newDf["lubrication_type"].astype("category")

    return newDf


# This function replaces missing values with the most likely value
# Numerical values use median (Middle value)
# Categorical values use mode (Most common)
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    newDf = df.copy()

    numeric_columns = newDf.select_dtypes(include="number").columns
    categorical_columns = newDf.select_dtypes(include=["object", "category"]).columns

    for col in numeric_columns:
        newDf[col] = newDf[col].fillna(newDf[col].median())
    
    for col in categorical_columns:
        newDf[col] = newDf[col].fillna(newDf[col].mode()[0])

    return newDf


# Creates features for later analysis
def create_process_features(df: pd.DataFrame) -> pd.DataFrame:
    newDf = df.copy()

    # Temp lost during rolling process
    newDf["temperature_drop"] = (newDf["entry_temperature"] - newDf["exit_temperature"])

    # Percentage temp loss relative to entry temp
    newDf["temperature_drop_percent"] = (newDf["temperature_drop"] / newDf["entry_temperature"]) * 100

    # Estimated final thickness after applying reduction ratio
    newDf["estimated_exit_thickness"] = (newDf["strip_thickness"] * (1 - newDf["reduction_ratio"]))

    # Amount of thickness reduced during rolling
    newDf["thickness_reduction"] = (newDf["strip_thickness"] - newDf["estimated_exit_thickness"])

    # Bending force normalized by incoming strip thickness.
    newDf["force_per_thickness"] = (newDf["bending_force"] / newDf["strip_thickness"])

    # Proxy for rolling difficulty due to friction and material resistance
    newDf["friction_load_proxy"] = (newDf["friction_coefficient"] * newDf["deformation_resistance"])

    # Proxy for process intensity
    newDf["rolling_intensity"] = (newDf["rolling_speed"] * newDf["reduction_ratio"] * newDf["strain_rate"])

    return newDf


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(df)
    validate_schema(df)
    df = remove_duplicates(df)
    df = enforce_data_types(df)
    df = handle_missing_values(df)
    df = create_process_features(df)

    return df

def save_cleaned_data(df: pd.DataFrame) -> None:
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)


if __name__ == "__main__":
    raw_df = load_raw_data()
    cleaned_df = clean_data(raw_df)
    save_cleaned_data(cleaned_df)

    print("Performed Cleaning")
    print(f"Rows: {cleaned_df.shape[0]}")
    print(f"Columns: {cleaned_df.shape[1]}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")
    print(cleaned_df.head())
