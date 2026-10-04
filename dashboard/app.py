
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os

st.set_page_config(
    page_title="Uyo Urban Heat Island Explorer",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🛰️ Uyo Urban Heat Island & Surface Microclimate Explorer")
st.markdown("**Decadal Geospatial Analysis (2016 vs. 2025) using Landsat 8/9 Level-2 Remote Sensing**")
st.caption("Host Organization: Space Technology & GIS Solutions | Local Government Area: Uyo, Akwa Ibom State")

# Load Summary Data
@st.cache_data
def load_data():
    df_summary = pd.read_csv("data/processed/summary_epochs.csv")
    df_reg = pd.read_csv("data/processed/regression_summary.csv")
    df_sampled = pd.read_csv("data/processed/sampled_pixel_statistics.csv")
    return df_summary, df_reg, df_sampled

try:
    df_summary, df_reg, df_sampled = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Please ensure processed CSV files are in the data/processed/ directory. Error: {e}")
    data_loaded = False

if data_loaded:
    # Sidebar
    st.sidebar.header("🕹️ Controls & Navigation")
    year_selected = st.sidebar.selectbox("Select Observation Epoch", ["2025 (Recent)", "2016 (Baseline)"])
    active_year = "2025" if "2025" in year_selected else "2016"
    
    view_mode = st.sidebar.radio("Analysis View", [
        "Executive KPI Overview",
        "Spatial Maps & Remote Sensing",
        "Statistical Modeling & Regressions",
        "Decadal Trend & Findings"
    ])

    # 1. KPI OVERVIEW
    if view_mode == "Executive KPI Overview":
        st.subheader("📊 Key Environmental & Thermal Indicators")
        row = df_summary[df_summary["Epoch"].str.contains(active_year)].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean Surface Temp (LST)", f"{row['Mean_LST_C']:.2f} °C", delta=f"{'+' if active_year=='2025' else '-'} Decadal Baseline")
        col2.metric("Max Peak Temperature", f"{row['Max_LST_C']:.2f} °C")
        col3.metric("Vegetation Index (NDVI)", f"{row['Mean_NDVI']:.3f}", delta="-0.036 Loss" if active_year=="2025" else None)
        col4.metric("Built-up Index (NDBI)", f"{row['Mean_NDBI']:.3f}", delta="+0.026 Growth" if active_year=="2025" else None)
        
        st.markdown("---")
        st.subheader("📈 Multi-Temporal Comparison Summary")
        st.dataframe(df_summary, use_container_width=True)

        st.subheader("💡 Key Takeaways for Urban Planners")
        st.info(
            "• **Urban Expansion:** Mean NDBI increased by **+0.026**, confirming accelerated built-up infrastructure growth in Uyo LGA.\n"
            "• **Vegetation Loss:** Mean NDVI declined from **0.418** to **0.382**, reflecting canopy loss due to construction and clearing.\n"
            "• **Microclimate Response:** Strong negative correlation between NDVI and LST confirms that green spaces provide active surface cooling."
        )

    # 2. SPATIAL MAPS
    elif view_mode == "Spatial Maps & Remote Sensing":
        st.subheader("🗺️ Spatial Distribution of Land Surface Temperature")
        if os.path.exists("figures/fig3_spatial_lst_comparison.png"):
            img = Image.open("figures/fig3_spatial_lst_comparison.png")
            st.image(img, caption="Comparative Spatial LST Map of Uyo LGA (2016 vs. 2025) derived from Landsat 8 TIRS Band 10", use_container_width=True)
        else:
            st.warning("Spatial map figure not found in figures/ directory.")

        if os.path.exists("figures/uyo_boundary.png"):
            st.image(Image.open("figures/uyo_boundary.png"), caption="Official Uyo LGA Administrative Boundary (139.41 km²)", width=450)

    # 3. STATISTICAL MODELING
    elif view_mode == "Statistical Modeling & Regressions":
        st.subheader("🔬 Statistical EDA & OLS Regression Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🌿 LST vs. Vegetation (NDVI)")
            fig_ndvi = px.scatter(
                df_sampled[df_sampled["Year"] == int(active_year)],
                x="NDVI", y="LST",
                trendline="ols",
                color_discrete_sequence=["#2ca02c"],
                opacity=0.25,
                title=f"Cooling Effect of Vegetation ({active_year})"
            )
            st.plotly_chart(fig_ndvi, use_container_width=True)

        with col2:
            st.markdown("### 🏙️ LST vs. Built-up Density (NDBI)")
            fig_ndbi = px.scatter(
                df_sampled[df_sampled["Year"] == int(active_year)],
                x="NDBI", y="LST",
                trendline="ols",
                color_discrete_sequence=["#d95f02"],
                opacity=0.25,
                title=f"Heating Effect of Built-up Areas ({active_year})"
            )
            st.plotly_chart(fig_ndbi, use_container_width=True)

        st.subheader("📋 Statistical Model Summary")
        st.dataframe(df_reg, use_container_width=True)

    # 4. DECADAL TRENDS
    elif view_mode == "Decadal Trend & Findings":
        st.subheader("📉 Decadal Distribution Shift (2016 vs 2025)")
        if os.path.exists("figures/fig1_eda_distributions.png"):
            st.image(Image.open("figures/fig1_eda_distributions.png"), caption="KDE Distribution Shifts for LST, NDVI, and NDBI", use_container_width=True)

        st.download_button(
            label="📥 Download Processed Data (CSV)",
            data=df_sampled.to_csv(index=False),
            file_name="uyo_uhi_sampled_data.csv",
            mime="text/csv"
        )
