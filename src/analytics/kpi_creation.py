# This KPI module loads the processed data and calculates operational metrics related to:
# - bending force
# - temp drop
# - rolling speed
# - reduction ratio
# - material grade
# - lube type
# These KPIs are created to support operational decision making

import pandas as pd

from src.config import PROCESSED_DATA_PATH

def load_cleaned_data() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DATA_PATH)


# Summary of high-level metrics
# This KPIs give a quick overview of process behaviour across the full dataset.
def overall_kpis(df: pd.DataFrame) -> dict:
    return {
        "record_count": len(df),
        "avg_bending_force": round(df["bending_force"].mean(), 2),
        "max_bending_force": round(df["bending_force"].max(), 2),
        "avg_entry_temperature": round(df["entry_temperature"].mean(), 2),
        "avg_exit_temperature": round(df["exit_temperature"].mean(), 2),
        "avg_temperature_drop": round(df["temperature_drop"].mean(), 2),
        "avg_rolling_speed": round(df["rolling_speed"].mean(), 2),
        "avg_reduction_ratio": round(df["reduction_ratio"].mean(), 4),
        "avg_strip_thickness": round(df["strip_thickness"].mean(), 2),
        "avg_force_per_thickness": round(df["force_per_thickness"].mean(), 2),
        "avg_rolling_intensity": round(df["rolling_intensity"].mean(), 2),
    }

# Groups the data by material type and calculates averages for each group
def kpis_by_material_grade(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("material_grade", observed=True)
        .agg(
            record_count=("bending_force", "count"),
            avg_bending_force=("bending_force", "mean"),
            avg_temperature_drop=("temperature_drop", "mean"),
            avg_rolling_speed=("rolling_speed", "mean"),
            avg_reduction_ratio=("reduction_ratio", "mean"),
            avg_force_per_thickness=("force_per_thickness", "mean"),
        )
        .round(2)
        .reset_index()
    )


# Compares process metrics across lube types.
# Lubrication affections fricion which influences rolling force and process efficiency
def kpis_by_lubrication_type(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("lubrication_type", observed=True)
        .agg(
            record_count=("bending_force", "count"),
            avg_bending_force=("bending_force", "mean"),
            avg_friction_coefficient=("friction_coefficient", "mean"),
            avg_force_per_thickness=("force_per_thickness", "mean"),
            avg_rolling_intensity=("rolling_intensity", "mean"),
        )
        .round(2)
        .reset_index()
    )


# Checks numeric variables which move most closely with bending force.
# Bending force is the target variable of the dataset.
def correlation_with_bending_force(df: pd.DataFrame) -> pd.Series:
    numeric_df = df.select_dtypes(include="number")

    return (
        numeric_df.corr()["bending_force"]
        .sort_values(ascending=False)
    )

if __name__ == "__main__":
    df = load_cleaned_data()

    print("Overall KPIs")
    print(overall_kpis(df))

    print("\nKPIs by Material Grade")
    print(kpis_by_material_grade(df))

    print("\nKPIs by Lubrication Type")
    print(kpis_by_lubrication_type(df))

    print("\nCorrelation with Bending Force")
    print(correlation_with_bending_force(df))