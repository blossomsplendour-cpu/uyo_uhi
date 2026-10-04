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

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df_summary = pd.read_csv("data/processed/summary_epochs.csv")
    df_reg = pd.read_csv("data/processed/regression_summary.csv") if os.path.exists("data/processed/regression_summary.csv") else None
    df_sampled = pd.read_csv("data/processed/sampled_pixel_statistics.csv") if os.path.exists("data/processed/sampled_pixel_statistics.csv") else None
    df_lulc = pd.read_csv("data/processed/landcover_summary.csv") if os.path.exists("data/processed/landcover_summary.csv") else None
    return df_summary, df_reg, df_sampled, df_lulc

try:
    df_summary, df_reg, df_sampled, df_lulc = load_data()
    # Harmonize epoch column name
    if "Epoch" not in df_summary.columns and "Year" in df_summary.columns:
        df_summary = df_summary.rename(columns={"Year": "Epoch"})
    df_summary["Epoch"] = df_summary["Epoch"].astype(str)
    data_loaded = True
except Exception as e:
    st.error(f"Error loading processed data: {e}")
    data_loaded = False
    df_summary = df_reg = df_sampled = df_lulc = None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.title("🛰️ Uyo UHI Explorer")
st.sidebar.caption("Landsat 8/9 · 2016–2025 · Uyo LGA")

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
    "**Tip:** Pages 3–4 show **all four years side-by-side**. "
    "Use the year selector only on the KPI page to focus headline numbers."
)

# ─────────────────────────────────────────────
# PAGE 1 — INTRODUCTION (FIRST)
# ─────────────────────────────────────────────
if view_mode == "1. Project Introduction":
    st.title("End-to-End Geospatial Data Analysis of Urban Heat Island Dynamics in Uyo LGA")
    st.markdown("### A Decadal Multi-Temporal Study (2016 · 2019 · 2022 · 2025)")
    st.caption("Industrial Training Project · Data Analysis · Space Technology / GIS Host Company")

    st.markdown("""
    ## Why this project exists

    Uyo, the capital of Akwa Ibom State, is urbanising rapidly. As vegetation is cleared and
    impermeable surfaces (roads, roofs, concrete) expand, the city absorbs and re-radiates more
    solar energy. This creates a **Surface Urban Heat Island (SUHI)** — built-up zones that run
    significantly hotter than surrounding vegetated land.

    This application turns **free Landsat 8/9 satellite observations** into:
    - quantitative maps of land surface temperature (LST)
    - vegetation (NDVI) and built-up (NDBI) indicators
    - a 4-class land surface map (Vegetation, Built-up, Bare ground, Water/wetland)
    - statistical proof of how green cover cools and built-up cover heats the surface
    - an interactive dashboard any planner can open in a browser

    ## Study design at a glance

    | Item | Detail |
    |---|---|
    | **Study area** | Uyo Local Government Area, Akwa Ibom State, Nigeria |
    | **Epochs** | Four dry-season scenes: **2016, 2019, 2022, 2025** |
    | **Sensor** | USGS Landsat 8/9 Collection 2 **Level-2** (Surface Reflectance + Surface Temperature) |
    | **Resolution** | 30 m (thermal band native 100 m, delivered at 30 m) |
    | **Core indices** | NDVI, NDBI, MNDWI, LST (°C), UTFVI |
    | **Output** | Reproducible Python pipeline + live Streamlit dashboard |

    ## What you can do in this app

    1. Read the project story (this page)  
    2. Inspect headline KPIs for any epoch  
    3. Compare thermal maps across 9 years  
    4. Inspect 4-class land cover change  
    5. Follow multi-year trends in vegetation vs built-up  
    6. See the statistical cooling/heating relationships  
    7. Open the full technical methodology  

    ---
    **Host relevance:** Built during IT placement at a Space Technology / GIS organisation to show how
    open satellite data and Python automation support environmental intelligence products.
    """)

# ─────────────────────────────────────────────
# PAGE 2 — KPI OVERVIEW
# ─────────────────────────────────────────────
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
    st.subheader("Complete 4-Epoch Summary (2016 · 2019 · 2022 · 2025)")
    st.dataframe(df_summary, use_container_width=True)

    st.success(
        """
        **How to read the deltas**  
        • Rising **NDBI** → more built-up / impervious surface signal  
        • Falling **NDVI** → vegetation canopy loss  
        • **Mean LST** can move up or down with weather on the satellite overpass day;
          that is why we emphasise NDVI/NDBI relationships and spatial patterns, not only city-wide mean °C.
        """
    )

# ─────────────────────────────────────────────
# PAGE 3 — THERMAL MAPS
# ─────────────────────────────────────────────
elif view_mode == "3. Thermal Maps (All 4 Epochs)":
    st.title("🗺️ Surface Thermal Signature — All 4 Epochs")
    st.markdown(
        "Side-by-side Land Surface Temperature (LST) maps for **2016, 2019, 2022 and 2025**. "
        "Each panel includes title, north arrow, and temperature scale."
    )

    if os.path.exists("figures/fig3_spatial_lst_comparison.png"):
        st.image(
            Image.open("figures/fig3_spatial_lst_comparison.png"),
            caption="Uyo LGA LST (°C) · Landsat 8/9 Collection 2 Level-2 · Dry-season acquisitions",
            use_container_width=True,
        )
    else:
        st.warning("`figures/fig3_spatial_lst_comparison.png` not found. Re-export figures from Colab.")

    st.markdown("### How to read the colours (practical legend)")
    leg1, leg2, leg3, leg4 = st.columns(4)
    leg1.info("**Dark purple / black**\nCooler surfaces\n(often dense vegetation, shade, residual moisture)")
    leg2.success("**Orange / yellow**\nIntermediate / typical urban–peri-urban surfaces")
    leg3.warning("**Bright yellow / white-hot**\nHottest surfaces\n(built-up cores, bare dry soil, exposed roofs)")
    leg4.error("**Light grey patches**\nCloud / shadow masked\n(no valid observation)")

    st.markdown("""
    ### UHI intensity interpretation (relative to city mean)
    | Relative LST | Practical label | Planning meaning |
    |---|---|---|
    | Well below city mean | Cool island | Protect existing greenery / water |
    | Near city mean | Typical | Background urban fabric |
    | Above mean + 0.5σ | Warm / moderate UHI | Monitor; greening opportunity |
    | Strongly above mean | Hot / strong UHI | Priority mitigation zone |

    **Note:** Absolute °C on two different dates is also affected by weather. Compare **spatial pattern**
    and **index relationships** when discussing multi-year change.
    """)

# ─────────────────────────────────────────────
# PAGE 4 — LAND COVER
# ─────────────────────────────────────────────
elif view_mode == "4. Land Cover Maps (4 Classes)":
    st.title("🗺️ Four-Class Land Surface Maps")
    st.markdown(
        "Classification into **Water/Wetland · Vegetation · Built-up · Bare ground** "
        "for each epoch, with north arrows and categorical legend."
    )

    if os.path.exists("figures/fig4_landcover_classification.png"):
        st.image(
            Image.open("figures/fig4_landcover_classification.png"),
            caption="4-class surface maps · threshold rules on NDVI, NDBI, MNDWI",
            use_container_width=True,
        )
    else:
        st.warning("`figures/fig4_landcover_classification.png` not found.")

    st.markdown("### Class rules (transparent methodology)")
    st.code(
        """
Water / Wetland : MNDWI > 0
Vegetation      : NDVI > 0.35  (and not water)
Built-up        : NDBI > 0     (and not water/veg)
Bare ground     : remaining valid land pixels (low NDVI, low NDBI)
Cloud / Mask    : QA_PIXEL cloud & shadow bits
        """.strip()
    )

    if df_lulc is not None:
        st.subheader("Class area share (%) and mean LST by class")
        st.dataframe(df_lulc, use_container_width=True)

        # Mean temperature by class chart if columns exist
        temp_cols = [c for c in df_lulc.columns if "Mean_Temp" in c]
        if temp_cols:
            st.markdown("#### 🔥 Linking land cover to heat (Mean LST by class)")
            st.caption("Built-up and bare ground typically run hotter than vegetation — this is the UHI mechanism.")
            plot_df = df_lulc.melt(id_vars=[c for c in df_lulc.columns if "Temp" not in c and c != "Year"],
                                   value_vars=temp_cols, var_name="Class", value_name="Mean_LST_C")
            # Clean class names
            plot_df["Class"] = plot_df["Class"].str.replace("Mean_Temp_", "").str.replace("_C", "")
            if "Year" in df_lulc.columns:
                fig = px.bar(df_lulc, x="Year", y=temp_cols, barmode="group",
                             title="Mean Land Surface Temperature by Land-Cover Class")
                st.plotly_chart(fig, use_container_width=True)

    st.warning(
        """
        **About the 2019 bare-ground surge**  
        A single dry-season scene can show more bare soil after harvest or under drier Harmattan conditions.
        Threshold classification is **indicative**, not a full supervised land-cover product.
        The multi-year story that remains robust is: **NDBI up, NDVI down** across the decade.
        """
    )

# ─────────────────────────────────────────────
# PAGE 5 — TIME SERIES
# ─────────────────────────────────────────────
elif view_mode == "5. Decadal Time-Series Trends" and data_loaded:
    st.title("📈 Decadal Time-Series Trends (2016 – 2025)")
    st.markdown("Four-point trajectories for vegetation, built-up signal, and mean surface temperature.")

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
        title="Structural shift across Uyo LGA (2016–2025): Built-up vs Vegetation",
        xaxis_title="Epoch",
        yaxis_title="Index value (dimensionless)",
        legend_title="Indicator",
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    fig_temp = px.line(
        df_summary, x="Epoch", y="Mean_LST_C", markers=True,
        title="Mean Land Surface Temperature (°C) by epoch (2016–2025)",
        labels={"Mean_LST_C": "Mean LST (°C)", "Epoch": "Epoch"},
    )
    fig_temp.update_traces(line_color="#c51b8a", line_width=3)
    st.plotly_chart(fig_temp, use_container_width=True)

    st.info(
        """
        **Interpretation guide**  
        • **NDBI rising** = stronger built-up / bare-impervious spectral signal  
        • **NDVI falling** = reduced green canopy  
        • **Mean LST** alone is weather-sensitive (different atmospheric conditions each overpass).  
          Use LST together with NDVI/NDBI and spatial maps — not as a lone climate trend.
        """
    )

# ─────────────────────────────────────────────
# PAGE 6 — OLS (EXPLAINED SIMPLY)
# ─────────────────────────────────────────────
elif view_mode == "6. Statistical Relationships (OLS)":
    st.title("🔬 Statistical Relationships (Simple Explanation)")

    st.markdown("""
    ## What question are we answering?

    > **When vegetation is higher, is the ground cooler?**  
    > **When built-up index is higher, is the ground hotter?**

    We answer with **scatter plots** of thousands of satellite pixels and a straight trend line
    (**Ordinary Least Squares regression**).
    """)

    st.markdown("""
    | Relationship | What we expect for UHI | What a trend line means |
    |---|---|---|
    | **LST vs NDVI** | Negative | More green → lower surface temperature (cooling) |
    | **LST vs NDBI** | Positive | More built-up → higher surface temperature (heating) |
    """)

    if df_sampled is not None:
        # Ensure Year column is string for colour
        df_plot = df_sampled.copy()
        if "Year" in df_plot.columns:
            df_plot["Year"] = df_plot["Year"].astype(str)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🌿 Vegetation cools the surface")
            fig1 = px.scatter(
                df_plot, x="NDVI", y="LST", color="Year" if "Year" in df_plot.columns else None,
                trendline="ols", opacity=0.25,
                title="LST vs NDVI (cooling relationship)",
                labels={"NDVI": "NDVI (greenness)", "LST": "Land Surface Temp (°C)"},
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.success("**Takeaway:** Points slope **downward**. Greener pixels are generally cooler.")

        with c2:
            st.subheader("🏙️ Built-up heats the surface")
            fig2 = px.scatter(
                df_plot, x="NDBI", y="LST", color="Year" if "Year" in df_plot.columns else None,
                trendline="ols", opacity=0.25,
                title="LST vs NDBI (heating relationship)",
                labels={"NDBI": "NDBI (built-up signal)", "LST": "Land Surface Temp (°C)"},
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.error("**Takeaway:** Points slope **upward**. More built-up pixels are generally hotter.")
    else:
        st.warning("Sampled pixel CSV not found — regression charts unavailable in this build.")

    with st.expander("How to read OLS in one minute (for the panel)"):
        st.markdown("""
        1. Each dot = one 30 m satellite pixel inside Uyo LGA.  
        2. The line is the best straight-line fit through the cloud of dots.  
        3. **Downward line (NDVI)** = negative association = cooling effect of vegetation.  
        4. **Upward line (NDBI)** = positive association = heating effect of built-up surfaces.  
        5. We say **“associated with”**, not “causes”, because other factors (moisture, slope, time of day) also matter.  
        6. Pixels near each other are spatially correlated; that is a known limitation of pixel-level Pearson/OLS
           and a reason advanced work adds Moran’s I / spatial regression.
        """)

    if df_reg is not None:
        st.subheader("Numeric model summary")
        st.dataframe(df_reg, use_container_width=True)

# ─────────────────────────────────────────────
# PAGE 7 — FULL DOCUMENTATION
# ─────────────────────────────────────────────
elif view_mode == "7. Full Methodology & Documentation":
    st.title("📖 Full Project Methodology & Documentation")

    st.markdown("""
    ## 1. Project identity

    **Title:** End-to-End Geospatial Data Analysis of Urban Heat Island Dynamics in Uyo LGA:  
    A Reproducible Python Pipeline and Interactive Dashboard for Satellite-Derived Surface Temperature Monitoring (2016–2025)

    **Type:** Industrial Training (IT) defence project · Data Analysis track  
    **Host domain:** Space Technology / GIS / Earth Observation  

    ---

    ## 2. Aim

    To develop a reproducible Python-based geospatial analytics pipeline that quantifies multi-temporal
    Surface Urban Heat Island patterns in Uyo LGA using Landsat 8/9 Collection 2 Level-2 data, and to
    deliver results through an interactive dashboard usable by non-GIS specialists.

    ### Objectives
    1. Acquire and preprocess multi-temporal Landsat Level-2 imagery and the Uyo LGA boundary.  
    2. Derive NDVI, NDBI, MNDWI and Land Surface Temperature (°C) with correct scale factors and QA masking.  
    3. Classify the landscape into four surface types and link each class to mean LST.  
    4. Quantify statistical associations between LST and vegetation/built-up indicators.  
    5. Communicate findings via publication-style maps and a live Streamlit application.

    ### Research questions
    1. What is the spatial pattern of daytime surface temperature across Uyo LGA?  
    2. How did vegetation and built-up spectral signals change from 2016 to 2025?  
    3. How strongly are NDVI and NDBI associated with LST?  
    4. Which surface classes should greening interventions prioritise?

    ---

    ## 3. Study area

    - **Location:** Uyo LGA, Akwa Ibom State, Nigeria (state capital; rapidly urbanising)  
    - **Approx. centre:** 5.03°N, 7.93°E  
    - **Boundary source:** geoBoundaries ADM2  
    - **Analysis CRS:** EPSG:4326 for display; raster analysis in native Landsat UTM  
    - **Climate note:** Humid tropical; dry season ~November–February is the practical clear-sky window  

    ---

    ## 4. Data

    | Dataset | Source | Role |
    |---|---|---|
    | Landsat 8/9 C2 L2 | Microsoft Planetary Computer / USGS | SR bands + ST_B10 + QA_PIXEL |
    | Uyo LGA polygon | geoBoundaries | Clip & study extent |
    | Epochs | Dry-season scenes ~**2016, 2019, 2022, 2025** | Multi-temporal change |

    ### Level-2 scale factors (mandatory)
    $$
    \\text{Reflectance} = DN \\times 0.0000275 - 0.2
    $$
    $$
    \\text{LST (°C)} = (DN \\times 0.00341802 + 149.0) - 273.15
    $$

    **Important:** Collection 2 Level-2 `ST_B10` is already a surface temperature product.
    Do **not** re-apply Planck / emissivity single-channel formulas meant for Level-1 data.

    ### QA masking
    Pixels flagged as fill, dilated cloud, cloud, or cloud shadow in `QA_PIXEL` are removed before index computation.

    ---

    ## 5. Spectral indices

    $$
    \\mathrm{NDVI} = \\frac{NIR - Red}{NIR + Red} = \\frac{B5 - B4}{B5 + B4}
    $$
    $$
    \\mathrm{NDBI} = \\frac{SWIR1 - NIR}{SWIR1 + NIR} = \\frac{B6 - B5}{B6 + B5}
    $$
    $$
    \\mathrm{MNDWI} = \\frac{Green - SWIR1}{Green + SWIR1} = \\frac{B3 - B6}{B3 + B6}
    $$
    $$
    \\mathrm{UTFVI} = \\frac{LST - \\overline{LST}}{LST}
    $$

    ### Four-class surface rules
    - **Water/Wetland:** MNDWI > 0  
    - **Vegetation:** NDVI > 0.35  
    - **Built-up:** NDBI > 0  
    - **Bare ground:** remaining valid land (low NDVI & low NDBI)

    ---

    ## 6. Analytical methods

    1. **EDA** — distributions of LST, NDVI, NDBI per epoch  
    2. **Pearson correlation + OLS trend lines** — LST vs NDVI; LST vs NDBI  
    3. **Multi-temporal comparison** — 4 epochs, index trajectories  
    4. **Class-wise mean LST** — links land cover to heat  
    5. **Interactive dashboard** — Streamlit + Plotly for stakeholder communication  

    ---

    ## 7. Key findings (fill with your live numbers during defence)

    - Built-up spectral signal (**NDBI**) increased across the decade.  
    - Vegetation signal (**NDVI**) declined.  
    - LST is **negatively** associated with NDVI (cooling) and **positively** associated with NDBI (heating).  
    - Built-up and bare classes show higher mean LST than dense vegetation.  
    - Narrow streams in Uyo are partly **sub-pixel** at 30 m, so open-water % is modest — expected for an inland LGA.

    ---

    ## 8. Scientific limitations (state these confidently)

    1. **LST ≠ air temperature.** Satellite measures surface skin temperature near ~10:30 local overpass.  
    2. **Snapshot bias.** Each map is one clear-sky morning, not a seasonal average.  
    3. **Weather between dates.** City-mean LST can differ because the atmosphere differed that morning.  
    4. **30 m resolution.** Fine courtyards and narrow streams are mixed pixels.  
    5. **Threshold classification** is transparent but not a full supervised LULC product with field validation.  
    6. **Spatial autocorrelation.** Neighbouring pixels are not independent; pixel OLS is associative, not a full spatial econometric model.

    ---

    ## 9. Recommendations

    1. Protect and expand tree canopy along major corridors and new estates.  
    2. Prioritise greening in persistent high-LST built-up cores visible on the thermal maps.  
    3. Avoid leaving large bare cleared sites exposed for long periods (high heat loading).  
    4. Institutionalise this open-source pipeline as a low-cost monitoring product for the host company.

    ---

    ## 10. Reproducibility & stack

    - **Language:** Python 3  
    - **Core libraries:** rasterio/rioxarray, geopandas, numpy, pandas, matplotlib, plotly, streamlit  
    - **Data access:** Planetary Computer STAC (signed HTTPS assets)  
    - **Code repository:** GitHub `uyo_uhi`  
    - **Live app:** Streamlit Community Cloud  

    ---

    ## 11. Organisational relevance (IT defence)

    This project demonstrates that a Space Technology / GIS company can:
    - replace slow manual GIS clicks with a **reproducible scripted pipeline**  
    - deliver client-facing **interactive intelligence** without proprietary licence lock-in for every viewer  
    - scale the same workflow from Uyo to other Nigerian cities by changing the AOI polygon and re-running the pipeline
    """)

else:
    if not data_loaded and view_mode not in ["1. Project Introduction", "7. Full Methodology & Documentation"]:
        st.warning("Data files not fully loaded. Introduction and Methodology pages still work.")