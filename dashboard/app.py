import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import PROCESSED_DATA_PATH
from src.analytics.kpi_creation import overall_kpis


st.set_page_config(
    page_title="Rolling Mill Analytics Dashboard",
    layout="wide"
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DATA_PATH)


df = load_data()

st.title("Rolling Mill Process Analytics Dashboard")


# Sidebar filters
st.sidebar.header("Filters")

material_options = sorted(df["material_grade"].dropna().unique())
lubrication_options = sorted(df["lubrication_type"].dropna().unique())

selected_materials = st.sidebar.multiselect(
    "Material Grade",
    material_options,
    default=material_options
)

selected_lubrication = st.sidebar.multiselect(
    "Lubrication Type",
    lubrication_options,
    default=lubrication_options
)

filtered_df = df[
    (df["material_grade"].isin(selected_materials)) &
    (df["lubrication_type"].isin(selected_lubrication))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# KPI Summary
st.header("Operational KPI Summary")

kpis = overall_kpis(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Avg Bending Force", 
    f"{kpis['avg_bending_force']} kN"
)

col2.metric(
    "Max Bending Force", 
    f"{kpis['max_bending_force']} kN"
)

col3.metric(
    "Avg Rolling Speed", 
    f"{kpis['avg_rolling_speed']} m/s"
)


col4, col5, col6 = st.columns(3)

col4.metric(
    "Avg Temperature Drop", 
    f"{kpis['avg_temperature_drop']} °C"
)

col5.metric(
    "Avg Reduction Ratio", 
    f"{kpis["avg_reduction_ratio"]}"
)

col6.metric(
    "Avg Force / Thickness",
    f"{kpis['avg_force_per_thickness']} kN/mm"
)


# Bending Force Drivers
st.header("Bending Force Drivers")

col1, col2 = st.columns(2)

with col1:
    fig = px.scatter(
        filtered_df,
        x="strip_thickness",
        y="bending_force",
        color="material_grade",
        hover_data=["rolling_speed", "reduction_ratio", "lubrication_type"],
        title="Bending Force vs Strip Thickness",
        labels={
            "strip_thickness": "Strip Thickness (mm)",
            "bending_force": "Bending Force (kN)"
        }
    )
    st.plotly_chart(fig, width='content')

with col2:
    fig = px.scatter(
        filtered_df,
        x="deformation_resistance",
        y="bending_force",
        color="material_grade",
        hover_data=["rolling_speed", "reduction_ratio", "lubrication_type"],
        title="Bending Force vs Deformation Resistance",
        labels={
            "deformation_resistance": "Deformation Resistance (MPa)",
            "bending_force": "Bending Force (kN)"
        }
    )
    st.plotly_chart(fig, width='content')

col3, col4 = st.columns(2)

with col3:
    fig = px.scatter(
        filtered_df,
        x="rolling_speed",
        y="bending_force",
        color="material_grade",
        hover_data=["strip_thickness", "reduction_ratio", "lubrication_type"],
        title="Bending Force vs Rolling Speed",
        labels={
            "rolling_speed": "Rolling Speed (m/s)",
            "bending_force": "Bending Force (kN)"
        }
    )
    st.plotly_chart(fig, width='content')

with col4:
    fig = px.scatter(
        filtered_df,
        x="rolling_intensity",
        y="bending_force",
        color="material_grade",
        hover_data=["strip_thickness", "strain_rate", "reduction_ratio"],
        title="Bending Force vs Rolling Intensity",
        labels={
            "rolling_intensity": "Rolling Intensity (Index)",
            "bending_force": "Bending Force (kN)"
        }
    )
    st.plotly_chart(fig, width='content')


# Material Grade Analysis
st.header("Material Grade Comparison")

material_summary = (
    filtered_df.groupby("material_grade", observed=True)
    .agg(
        avg_bending_force=("bending_force", "mean"),
        avg_temperature_drop=("temperature_drop", "mean"),
        avg_rolling_speed=("rolling_speed", "mean"),
        record_count=("bending_force", "count")
    )
    .reset_index()
)

material_summary["force_vs_avg"] = (
    material_summary["avg_bending_force"]
    - material_summary["avg_bending_force"].mean()
)


col1, col2= st.columns(2)

with col1:
    fig = px.bar(
        material_summary,
        x="material_grade",
        y="avg_bending_force",
        title="Average Bending Force by Material Grade",
        labels={
            "material_grade": "Material Grade",
            "avg_bending_force": "Average Bending Force (kN)"
        },
        color="material_grade",
    )

    min_val = material_summary["avg_bending_force"].min()
    max_val = material_summary["avg_bending_force"].max()

    fig.update_yaxes(range=[min_val * 0.98, max_val * 1.02])

    st.plotly_chart(fig, width='content')


with col2:
    fig = px.bar(
        material_summary,
        x="material_grade",
        y="avg_temperature_drop",
        title="Average Temperature Drop by Material Grade",
        labels={
            "material_grade": "Material Grade",
            "avg_temperature_drop": "Average Temperature Drop (°C)"
        },
        color="material_grade"
        
    )
    min_val = material_summary["avg_temperature_drop"].min()
    max_val = material_summary["avg_temperature_drop"].max()

    fig.update_yaxes(range=[min_val * 0.98, max_val * 1.02])

    st.plotly_chart(fig, width='content')
    


# Lubrication Analysis
st.header("Lubrication Type Comparison")

lubrication_summary = (
    filtered_df.groupby("lubrication_type", observed=True)
    .agg(
        avg_bending_force=("bending_force", "mean"),
        avg_friction_coefficient=("friction_coefficient", "mean"),
        avg_force_per_thickness=("force_per_thickness", "mean"),
        record_count=("bending_force", "count")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        lubrication_summary,
        x="lubrication_type",
        y="avg_bending_force",
        title="Average Bending Force by Lubrication Type",
        labels={
            "lubrication_type": "Lubrication Type",
            "avg_bending_force": "Average Bending Force (kN)"
        },
        color="lubrication_type",
        color_discrete_map={
        "dry": "#b9b9b9",
        "oil": "#91A82A",
        "water-based": "#3e84ad"
        }

    )
    min_val = lubrication_summary["avg_bending_force"].min()
    max_val = lubrication_summary["avg_bending_force"].max()

    fig.update_yaxes(range=[min_val * 0.98, max_val * 1.02])

    st.plotly_chart(fig, width='content')

with col2:
    fig = px.bar(
        lubrication_summary,
        x="lubrication_type",
        y="avg_friction_coefficient",
        title="Average Friction Coefficient by Lubrication Type",
        labels={
            "lubrication_type": "Lubrication Type",
            "avg_friction_coefficient": "Average Friction Coefficient"
        },
        color="lubrication_type",
        color_discrete_map={
        "dry": "#b9b9b9",
        "oil": "#91A82A",
        "water-based": "#3e84ad"
        }
    )

    min_val = lubrication_summary["avg_friction_coefficient"].min()
    max_val = lubrication_summary["avg_friction_coefficient"].max()

    fig.update_yaxes(range=[min_val * 0.98, max_val * 1.02])

    st.plotly_chart(fig, width='content')


# Process Feature Distributions
st.header("Process Feature Distributions")

col1, col2, col3, = st.columns(3)

# 1. Bending Force Distribution by Material Grade
with col1:
    fig = px.box(
        filtered_df,
        x="material_grade",
        y="bending_force",
        color="material_grade",
        points="outliers",
        title="Bending Force Distribution by Material Grade",
        labels={
            "material_grade": "Material Grade",
            "bending_force": "Bending Force (kN)"
        }
    )

    st.plotly_chart(fig, width='content')


# 2. Temperature Drop Distribution by Material Grade
with col2:
    fig = px.histogram(
        filtered_df,
        x="temperature_drop",
        color="material_grade",
        nbins=30,
        marginal="box",
        barmode="overlay",
        opacity=0.65,
        title="Temperature Drop Distribution by Material Grade",
        labels={
            "temperature_drop": "Temperature Drop (°C)",
            "material_grade": "Material Grade"
        }
    )

    st.plotly_chart(fig, width='content')


# 3. Bending Force Deviation from Average
deviation_df = filtered_df.copy()

deviation_df["bending_force_deviation"] = (
    deviation_df["bending_force"]
    - deviation_df["bending_force"].mean()
)

with col3:
    fig = px.histogram(
        deviation_df,
        x="bending_force_deviation",
        nbins=30,
        title="Bending Force Deviation from Average",
        labels={
            "bending_force_deviation": "Deviation from Average Bending Force (kN)"
        }
    )

    fig.add_vline(
        x=0,
        line_dash="dash",
        annotation_text="Average",
        annotation_position="top"
    )

    st.plotly_chart(fig, width='content')


# Correlation Analysis
st.header("Correlation with Bending Force")

numeric_df = filtered_df.select_dtypes(include="number")
correlation = (
    numeric_df.corr()["bending_force"]
    .sort_values(ascending=False)
    .reset_index()
)

correlation.columns = ["feature", "correlation_with_bending_force"]

fig = px.bar(
    correlation,
    x="correlation_with_bending_force",
    y="feature",
    orientation="h",
    color="correlation_with_bending_force",
    color_continuous_scale="RdBu",
    title="Correlation of Features with Bending Force",
    labels={
        "correlation_with_bending_force": "Correlation with Bending Force",
        "feature": "Metric"
    }
)

fig.update_layout(coloraxis_colorbar_title="Correlation")

st.plotly_chart(fig, width='content')


# Raw Data Preview
st.header("Filtered Data Preview")

st.dataframe(filtered_df.head(100), width='content')