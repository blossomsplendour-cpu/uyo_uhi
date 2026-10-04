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

st.title("🛰️ Uyo Urban Heat Island & Surface Microclimate Explorer")
st.markdown("**Decadal Multi-Temporal Remote Sensing Pipeline (2016, 2019, 2022, 2025) using Landsat 8/9 Level-2 Data**")
st.caption("Host Organization: Space Technology & GIS Solutions | Study Area: Uyo LGA, Akwa Ibom State")

@st.cache_data
def load_data():
    df_summary = pd.read_csv("data/processed/summary_epochs.csv")
    df_reg = pd.read_csv("data/processed/regression_summary.csv") if os.path.exists("data/processed/regression_summary.csv") else None
    df_sampled = pd.read_csv("data/processed/sampled_pixel_statistics.csv") if os.path.exists("data/processed/sampled_pixel_statistics.csv") else None
    df_lulc = pd.read_csv("data/processed/landcover_summary.csv") if os.path.exists("data/processed/landcover_summary.csv") else None
    return df_summary, df_reg, df_sampled, df_lulc

try:
    df_summary, df_reg, df_sampled, df_lulc = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading processed data: {e}")
    data_loaded = False

if data_loaded:
    st.sidebar.header("🕹️ Controls & Navigation")
    
    # Year selector in sidebar
    available_years = df_summary["Epoch"].astype(str).tolist()
    selected_year = st.sidebar.selectbox("Select Focus Year for Metrics", available_years, index=len(available_years)-1)
    
    view_mode = st.sidebar.radio("Navigation Tabs", [
        "Executive KPI Overview",
        "Spatial LST Thermal Maps (4 Epochs)",
        "4-Class Land Surface Maps (4 Epochs)",
        "4-Epoch Time-Series Trends",
        "Statistical Regressions",
        "📖 Full Project Methodology & Documentation"
    ])

    # 1. EXECUTIVE KPI OVERVIEW
    if view_mode == "Executive KPI Overview":
        st.subheader(f"📊 Key Environmental Indicators for {selected_year}")
        
        row = df_summary[df_summary["Epoch"].astype(str) == str(selected_year)].iloc[0]
        baseline = df_summary.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean Surface Temp (LST)", f"{row['Mean_LST_C']:.2f} °C", 
                    delta=f"{row['Mean_LST_C'] - baseline['Mean_LST_C']:.2f} °C vs 2016" if selected_year != "2016" else "Baseline")
        col2.metric("Max Peak Temperature", f"{row['Max_LST_C']:.2f} °C")
        col3.metric("Vegetation Index (NDVI)", f"{row['Mean_NDVI']:.3f}", 
                    delta=f"{row['Mean_NDVI'] - baseline['Mean_NDVI']:.3f} Canopy Change" if selected_year != "2016" else "Baseline")
        col4.metric("Built-up Index (NDBI)", f"{row['Mean_NDBI']:.3f}", 
                    delta=f"{row['Mean_NDBI'] - baseline['Mean_NDBI']:.3f} Built-up Shift" if selected_year != "2016" else "Baseline")
        
        st.markdown("---")
        st.subheader("📋 Complete 4-Epoch Decadal Summary Table (2016 – 2025)")
        st.dataframe(df_summary, use_container_width=True)

    # 2. SPATIAL LST MAPS
    elif view_mode == "Spatial LST Thermal Maps (4 Epochs)":
        st.subheader("🗺️ Thermal Signature Trend Across All 4 Epochs (2016, 2019, 2022, 2025)")
        if os.path.exists("figures/fig3_spatial_lst_comparison.png"):
            st.image(Image.open("figures/fig3_spatial_lst_comparison.png"), 
                     caption="2x2 Cartographic Grid showing Surface Temperature (°C) across 2016, 2019, 2022, and 2025 with Titles, North Arrows, and Temperature Scale", use_container_width=True)
        else:
            st.warning("Figure figures/fig3_spatial_lst_comparison.png not found.")

    # 3. 4-CLASS LAND COVER MAPS
    elif view_mode == "4-Class Land Surface Maps (4 Epochs)":
        st.subheader("🗺️ 4-Class Surface Classification Trend (Built-up, Vegetation, Bare Soil, Water)")
        if os.path.exists("figures/fig4_landcover_classification.png"):
            st.image(Image.open("figures/fig4_landcover_classification.png"), 
                     caption="2x2 Cartographic Grid showing 4-Class Surface Coverage across 2016, 2019, 2022, and 2025 with Titles, North Arrows, and Category Keys", use_container_width=True)
            
        if df_lulc is not None:
            st.markdown("### 📊 4-Epoch Land Surface Coverage & Temperature Breakdown")
            st.dataframe(df_lulc, use_container_width=True)

    # 4. TIME-SERIES TRENDS
    elif view_mode == "4-Epoch Time-Series Trends":
        st.subheader("📈 4-Epoch Time-Series Trends (2016 – 2025)")
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=df_summary["Epoch"], y=df_summary["Mean_NDBI"], name="Built-Up Index (NDBI)", line=dict(color="#d95f02", width=3), mode="lines+markers"))
        fig_trend.add_trace(go.Scatter(x=df_summary["Epoch"], y=df_summary["Mean_NDVI"], name="Vegetation Index (NDVI)", line=dict(color="#2ca02c", width=3), mode="lines+markers"))
        fig_trend.update_layout(title="Decadal Structural Shift: Built-Up Expansion vs Vegetation Canopy Loss", xaxis_title="Epoch", yaxis_title="Index Value")
        st.plotly_chart(fig_trend, use_container_width=True)

        fig_temp = px.line(df_summary, x="Epoch", y="Mean_LST_C", markers=True, title="Mean Surface Temperature (°C) across Epochs", color_discrete_sequence=["#d95f02"])
        st.plotly_chart(fig_temp, use_container_width=True)

    # 5. REGRESSIONS
    elif view_mode == "Statistical Regressions":
        st.subheader("🔬 Microclimate OLS Regression Models")
        if df_sampled is not None:
            col1, col2 = st.columns(2)
            with col1:
                fig_ndvi = px.scatter(df_sampled, x="NDVI", y="LST", color="Year", trendline="ols", title="LST vs Vegetation (NDVI)")
                st.plotly_chart(fig_ndvi, use_container_width=True)
            with col2:
                fig_ndbi = px.scatter(df_sampled, x="NDBI", y="LST", color="Year", trendline="ols", title="LST vs Built-up (NDBI)")
                st.plotly_chart(fig_ndbi, use_container_width=True)

    # 6. FULL DOCUMENTATION & METHODOLOGY PAGE
    elif view_mode == "📖 Full Project Methodology & Documentation":
        st.subheader("📖 Technical Methodology & Project Documentation")
        st.markdown("""
        ### 1. Abstract & Study Objectives
        Quantifying **Surface Urban Heat Island (SUHI)** dynamics across **Uyo Local Government Area (LGA)** across a 4-epoch decadal timeline (**2016, 2019, 2022, 2025**).

        ### 2. Remote Sensing Data & Preprocessing
        * **Data:** USGS Landsat 8/9 Collection 2 Level-2 Surface Reflectance and Surface Temperature.
        * **Spatial Resolution:** 30 meters.
        * **Quality Masking:** Bitmask filtering on `QA_PIXEL` layer for clouds and cloud shadows.

        ### 3. 4 Surface Class Formulations
        * **Water Bodies / Wetlands:** $\\text{MNDWI} > 0$
        * **Vegetation Canopy:** $\\text{NDVI} > 0.35$
        * **Built-Up Infrastructure:** $\\text{NDBI} > 0$
        * **Bare Ground / Cleared Soil:** $\\text{NDVI} \\le 0.35$ and $\\text{NDBI} \\le 0$
        """)