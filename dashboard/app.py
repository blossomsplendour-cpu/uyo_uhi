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

# DATA LOADING
@st.cache_data
def load_data():
    df_summary = pd.read_csv("data/processed/summary_epochs.csv")
    df_reg = pd.read_csv("data/processed/regression_summary.csv") if os.path.exists("data/processed/regression_summary.csv") else None
    df_sampled = pd.read_csv("data/processed/sampled_pixel_statistics.csv") if os.path.exists("data/processed/sampled_pixel_statistics.csv") else None
    df_lulc = pd.read_csv("data/processed/landcover_summary.csv") if os.path.exists("data/processed/landcover_summary.csv") else None
    return df_summary, df_reg, df_sampled, df_lulc

try:
    df_summary, df_reg, df_sampled, df_lulc = load_data()
    if "Epoch" not in df_summary.columns and "Year" in df_summary.columns:
        df_summary = df_summary.rename(columns={"Year": "Epoch"})
    df_summary["Epoch"] = df_summary["Epoch"].astype(str)
    data_loaded = True
except Exception as e:
    st.error(f"Error loading processed data: {e}")
    data_loaded = False
    df_summary = df_reg = df_sampled = df_lulc = None

# SIDEBAR
st.sidebar.title("🛰️ Uyo UHI Explorer")
st.sidebar.caption("Landsat 8/9, 2016-2025, Uyo LGA")

view_mode = st.sidebar.radio(
    "Navigate the study",
    [
        "1. Project Introduction",
        "2. Executive KPI Overview",
        "3. Thermal Maps (All 4 Epochs)",
        "4. Land Cover Maps (4 Classes)",
        "5. Decadal Time-Series Trends",
        "6. Statistical Relationships (OLS)",
        "7. Full Methodology & Documentation",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Tip: Pages 3 and 4 show all four years side-by-side. "
    "Use the year selector only on the KPI page to focus headline numbers."
)

# PAGE 1: INTRODUCTION
if view_mode == "1. Project Introduction":
    st.title("End-to-End Geospatial Data Analysis of Urban Heat Island Dynamics in Uyo LGA")
    st.markdown("### A Decadal Multi-Temporal Study (2016, 2019, 2022, 2025)")
    st.caption("Host Organization: Advanced Space Technology And Applications Laboratories, Uyo, Akwa Ibom State")

    st.markdown("### Abstract")
    st.markdown("""
    Rapid urbanization in Uyo Local Government Area has led to the continuous replacement of natural vegetation 
    with impervious surfaces such as concrete and asphalt. This framework utilizes satellite remote sensing to 
    quantify the resulting Surface Urban Heat Island (SUHI) effect. By analyzing Landsat 8 and 9 imagery across 
    a decadal span (2016 to 2025), this project computes spectral indices and surface temperatures to demonstrate 
    the statistical relationship between land cover changes and microclimate heating.
    """)

    st.markdown("### Dedication & Acknowledgements")
    st.markdown("""
    This project is dedicated to the pursuit of sustainable urban planning and data-driven environmental management 
    in Nigeria. Special appreciation goes to my supervisors, the Department of Data Analysis, and the management 
    and staff of **Advanced Space Technology And Applications Laboratories, Uyo**, for providing the industrial 
    training platform, mentorship, and resources that made this geospatial research possible.
    """)

    st.markdown("""
    ### Study Design at a Glance
    | Item | Detail |
    |---|---|
    | **Study area** | Uyo Local Government Area, Akwa Ibom State, Nigeria |
    | **Epochs** | Four dry-season scenes: 2016, 2019, 2022, 2025 |
    | **Sensor** | USGS Landsat 8/9 Collection 2 Level-2 (Surface Reflectance & Surface Temperature) |
    | **Resolution** | 30 meters |
    | **Core indices** | NDVI, NDBI, MNDWI, LST (°C) |
    | **Output** | Reproducible geospatial framework and interactive dashboard |
    """)

# PAGE 2: KPI OVERVIEW
elif view_mode == "2. Executive KPI Overview" and data_loaded:
    st.title("📊 Executive KPI Overview")
    st.markdown("Headline environmental indicators derived from Landsat Level-2 products.")

    years = df_summary["Epoch"].tolist()
    selected_year = st.selectbox("Focus year for KPI cards", years, index=len(years) - 1)

    row = df_summary[df_summary["Epoch"] == selected_year].iloc[0]
    baseline = df_summary.iloc[0]

    def delta_txt(curr, base, suffix=""):
        d = curr - base
        sign = "+" if d >= 0 else ""
        return f"{sign}{d:.3f}{suffix} vs {baseline['Epoch']}" if selected_year != str(baseline["Epoch"]) else "Baseline year"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean LST", f"{row['Mean_LST_C']:.2f} °C", delta=delta_txt(row["Mean_LST_C"], baseline["Mean_LST_C"], " °C"))
    c2.metric("Max LST", f"{row['Max_LST_C']:.2f} °C")
    c3.metric("Mean NDVI (Vegetation)", f"{row['Mean_NDVI']:.3f}", delta=delta_txt(row["Mean_NDVI"], baseline["Mean_NDVI"]))
    c4.metric("Mean NDBI (Built-up)", f"{row['Mean_NDBI']:.3f}", delta=delta_txt(row["Mean_NDBI"], baseline["Mean_NDBI"]))

    st.markdown("---")
    st.subheader("Complete 4-Epoch Summary (2016, 2019, 2022, 2025)")
    st.dataframe(df_summary, use_container_width=True)

# PAGE 3: THERMAL MAPS
elif view_mode == "3. Thermal Maps (All 4 Epochs)":
    st.title("🗺️ Surface Thermal Signature: All 4 Epochs")
    st.markdown("Side-by-side Land Surface Temperature (LST) maps for 2016, 2019, 2022 and 2025.")

    if os.path.exists("figures/fig3_spatial_lst_comparison.png"):
        st.image(
            Image.open("figures/fig3_spatial_lst_comparison.png"),
            caption="Uyo LGA LST (°C): Landsat 8/9 Collection 2 Level-2",
            use_container_width=True,
        )
    else:
        st.warning("Map file not found.")

    st.markdown("### How to read the colors")
    leg1, leg2, leg3, leg4 = st.columns(4)
    leg1.info("**Dark purple / black**: Cooler surfaces (vegetation, shade, water)")
    leg2.success("**Orange / yellow**: Intermediate urban surfaces")
    leg3.warning("**Bright yellow / white**: Hottest surfaces (built-up cores, bare soil)")
    leg4.error("**Light grey patches**: Cloud or shadow masked (no data)")

# PAGE 4: LAND COVER
elif view_mode == "4. Land Cover Maps (4 Classes)":
    st.title("🗺️ Four-Class Land Surface Maps")
    st.markdown("""
    **How to read this page:**
    The map below categorizes the physical surface of Uyo into four groups: Water, Vegetation, Built-up infrastructure, and Bare Ground.
    """)

    if os.path.exists("figures/fig4_landcover_classification.png"):
        st.image(
            Image.open("figures/fig4_landcover_classification.png"),
            caption="4-class surface maps based on NDVI, NDBI, and MNDWI thresholds",
            use_container_width=True,
        )

    if df_lulc is not None:
        temp_cols = [c for c in df_lulc.columns if "Mean_Temp" in c]
        if temp_cols:
            st.markdown("### 🔥 How hot does each land type get?")
            st.markdown("This chart takes the classes from the map above and calculates their average temperature. Notice that the Orange (Built-up) and Brown (Bare Ground) bars are always taller (hotter) than the Green (Vegetation) bars.")
            
            plot_df = df_lulc.melt(id_vars=["Year"], value_vars=temp_cols, var_name="Class", value_name="Mean_LST_C")
            plot_df["Class"] = plot_df["Class"].str.replace("Mean_Temp_", "").str.replace("_C", "")
            
            # Map colors strictly to land cover types
            color_map = {
                "Veg": "#2ca02c",     # Green
                "Built": "#d95f02",   # Orange
                "Bare": "#8c564b",    # Brown
                "Water": "#1f77b4"    # Blue
            }
            
            fig = px.bar(
                plot_df, x="Year", y="Mean_LST_C", color="Class", barmode="group",
                color_discrete_map=color_map,
                labels={"Mean_LST_C": "Mean Temperature (°C)", "Year": "Epoch Year", "Class": "Land Category"},
                title="Mean Land Surface Temperature by Land Cover Class"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Class Area Percentages")
        st.dataframe(df_lulc, use_container_width=True)

    st.warning(
        "Note on 2019 Bare Ground: "
        "A single dry-season scene can show higher bare soil coverage due to agricultural harvest cycles or drier weather conditions prior to image acquisition. "
        "The primary focus of this framework is the long-term decadal trend."
    )

# PAGE 5: TIME SERIES
elif view_mode == "5. Decadal Time-Series Trends" and data_loaded:
    st.title("📈 Decadal Time-Series Trends (2016 - 2025)")
    st.markdown("Tracking structural shifts in vegetation and built-up land over 9 years.")

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_summary["Epoch"], y=df_summary["Mean_NDBI"],
        name="Built-Up Index (NDBI)", mode="lines+markers",
        line=dict(color="#d95f02", width=3)
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_summary["Epoch"], y=df_summary["Mean_NDVI"],
        name="Vegetation Index (NDVI)", mode="lines+markers",
        line=dict(color="#2ca02c", width=3)
    ))
    fig_trend.update_layout(
        title="Structural shift across Uyo LGA: Built-up Expansion vs Vegetation Decline",
        xaxis_title="Epoch",
        yaxis_title="Index value",
        legend_title="Indicator",
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    fig_temp = px.line(
        df_summary, x="Epoch", y="Mean_LST_C", markers=True,
        title="Mean Land Surface Temperature (°C) by epoch (2016 - 2025)",
        labels={"Mean_LST_C": "Mean LST (°C)", "Epoch": "Epoch"},
    )
    fig_temp.update_traces(line_color="#c51b8a", line_width=3)
    st.plotly_chart(fig_temp, use_container_width=True)

# PAGE 6: OLS
elif view_mode == "6. Statistical Relationships (OLS)":
    st.title("🔬 Statistical Relationships: Ordinary Least Squares (OLS)")

    st.markdown("""
    ### The Core Research Question
    Does vegetation cool the city? Do concrete and asphalt heat the city?
    
    To prove this mathematically, we plot thousands of individual locations (pixels) on a graph and draw a trendline.
    """)

    if df_sampled is not None:
        df_plot = df_sampled.copy()
        if "Year" in df_plot.columns:
            df_plot["Year"] = df_plot["Year"].astype(str)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🌿 Vegetation Cooling Effect")
            fig1 = px.scatter(
                df_plot, x="NDVI", y="LST", color="Year" if "Year" in df_plot.columns else None,
                trendline="ols", opacity=0.25,
                title="LST vs NDVI",
                labels={"NDVI": "NDVI (Greenness)", "LST": "Surface Temp (°C)"},
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.success("Interpretation: The line slopes downwards. This proves mathematically that as vegetation increases, surface temperature decreases.")

        with c2:
            st.subheader("🏙️ Built-up Heating Effect")
            fig2 = px.scatter(
                df_plot, x="NDBI", y="LST", color="Year" if "Year" in df_plot.columns else None,
                trendline="ols", opacity=0.25,
                title="LST vs NDBI",
                labels={"NDBI": "NDBI (Built-up density)", "LST": "Surface Temp (°C)"},
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.error("Interpretation: The line slopes upwards. This proves mathematically that as concrete and infrastructure increase, surface temperature increases.")

# PAGE 7: FULL METHODOLOGY
elif view_mode == "7. Full Methodology & Documentation":
    st.title("📖 Full Project Methodology & Documentation")

    st.markdown("""
    ### 1. Research Objectives
    1. Acquire and preprocess multi-temporal Landsat Level-2 imagery for Uyo LGA.  
    2. Derive NDVI, NDBI, MNDWI and Land Surface Temperature (°C) with correct scale factors.  
    3. Classify the landscape into four surface types and link each class to mean temperature.  
    4. Quantify statistical associations between temperature and land cover indicators.  

    ### 2. Data Acquisition
    * **Sensor:** USGS Landsat 8/9 Collection 2 Level-2.
    * **Cloud QA Masking:** Applied bitmask filtering on the `QA_PIXEL` layer to remove atmospheric artifacts.
    * **Scale Factors (USGS Standard):**
      Reflectance = DN * 0.0000275 - 0.2  
      LST (°C) = (DN * 0.00341802 + 149.0) - 273.15

    ### 3. Spectral Indices
    * **NDVI:** (NIR - Red) / (NIR + Red)
    * **NDBI:** (SWIR1 - NIR) / (SWIR1 + NIR)
    * **MNDWI:** (Green - SWIR1) / (Green + SWIR1)

    ### 4. Software Stack & Environments
    * **Programming Language:** Python 3
    * **Development Environments:** Google Colab (Cloud processing), Visual Studio Code (VS Code)
    * **Geospatial Libraries:** Rasterio, GeoPandas, Rioxarray, PySTAC
    * **Data Visualization & UI:** Plotly, Matplotlib, Streamlit

    ### 5. Key Findings
    * Built-up spectral signal (NDBI) increased across the decade, indicating urban sprawl.  
    * Vegetation signal (NDVI) declined, indicating canopy loss.  
    * Built-up areas and bare soil consistently recorded higher mean temperatures than dense vegetation.

    ### 6. Organizational Relevance (IT Defense)
    This framework demonstrates how **Advanced Space Technology And Applications Laboratories** can leverage open-source Python programming to automate satellite data processing, reducing reliance on expensive proprietary GIS software licenses while delivering interactive web-based data products.

    ### 7. References
    * United States Geological Survey (USGS). (2021). *Landsat 8-9 OLI/TIRS Collection 2 Level-2 Data Format Control Book*.
    * Tucker, C. J. (1979). *Red and photographic infrared linear combinations for monitoring vegetation*. Remote Sensing of Environment, 8(2), 127-150.
    * Zha, Y., Gao, J., & Ni, S. (2003). *Use of normalized difference built-up index in automatically mapping urban areas from TM imagery*. International Journal of Remote Sensing, 24(3), 583-594.
    """)