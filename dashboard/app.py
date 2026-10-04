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

st.sidebar.title("🛰️ Uyo UHI Explorer")
st.sidebar.caption("Landsat 8/9 · 2016-2025 · Uyo LGA")
st.sidebar.markdown("**Host:** Advanced Space Technology And Applications Laboratories")

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
st.sidebar.success(
    "Quick tip: Pages 3 and 4 show all four years side by side. "
    "Use the year selector on the KPI page when you want one year in focus."
)
st.sidebar.info(
    "Defence tip: When asked 'what did you build?', say: "
    "a reproducible geospatial framework that turns free Landsat data into "
    "maps, statistics, and a live dashboard for Uyo LGA."
)

# ─────────────────────────────────────────────
# PAGE 1
# ─────────────────────────────────────────────
if view_mode == "1. Project Introduction":
    st.title("End-to-End Geospatial Data Analysis of Urban Heat Island Dynamics in Uyo LGA")
    st.markdown("### A Decadal Multi-Temporal Study (2016 · 2019 · 2022 · 2025)")
    st.caption(
        "Industrial Training Project · Data Analysis · "
        "Advanced Space Technology And Applications Laboratories, Uyo, Akwa Ibom State"
    )

    st.markdown("### Abstract")
    st.markdown("""
    Rapid urbanisation in Uyo Local Government Area continues to replace natural vegetation with
    impervious surfaces such as concrete, asphalt, and rooftops. This project develops a reproducible
    geospatial **framework** that quantifies the resulting Surface Urban Heat Island (SUHI) effect using
    Landsat 8/9 Collection 2 Level-2 satellite data for four dry-season epochs: **2016, 2019, 2022, and 2025**.

    The framework computes vegetation (NDVI), built-up (NDBI), water (MNDWI), and land surface
    temperature (LST), classifies the landscape into four surface types, and tests statistical
    associations between land cover and heat. Results are delivered through an interactive Streamlit
    dashboard so planners and non-GIS specialists can explore the evidence directly in a browser.
    """)

    st.markdown("### Dedication")
    st.markdown("""
    This work is dedicated to sustainable, data-driven urban planning in Nigeria, and to every young
    analyst learning to turn satellite observations into decisions that protect people and places.
    """)

    st.markdown("### Acknowledgements")
    st.markdown("""
    I appreciate my academic supervisors and the Department of Data Analysis for guidance throughout
    this Industrial Training defence project. Special thanks go to the management and staff of
    **Advanced Space Technology And Applications Laboratories, Uyo, Akwa Ibom State**, for the
    placement opportunity, mentorship, and exposure to operational Earth Observation and GIS workflows
    that shaped this study.
    """)

    st.markdown("---")
    st.markdown("## Why this project exists")
    st.markdown("""
    Uyo, the capital of Akwa Ibom State, is urbanising quickly. As tree canopy is cleared and impermeable
    surfaces expand, the city absorbs and re-radiates more solar energy. The result is a **Surface Urban
    Heat Island**: built-up zones that run hotter than surrounding vegetated land.

    This application turns free Landsat 8/9 observations into:
    - quantitative maps of land surface temperature (LST)
    - vegetation (NDVI) and built-up (NDBI) indicators
    - a four-class land surface map (Vegetation, Built-up, Bare ground, Water/wetland)
    - statistical evidence of how green cover cools and built-up cover heats the surface
    - an interactive dashboard any stakeholder can open without installing GIS software
    """)

    st.markdown("## Study design at a glance")
    st.markdown("""
    | Item | Detail |
    |---|---|
    | **Study area** | Uyo Local Government Area, Akwa Ibom State, Nigeria |
    | **Epochs** | Four dry-season scenes: **2016, 2019, 2022, 2025** |
    | **Sensor** | USGS Landsat 8/9 Collection 2 Level-2 (Surface Reflectance + Surface Temperature) |
    | **Resolution** | 30 m |
    | **Core indices** | NDVI, NDBI, MNDWI, LST (°C), UTFVI |
    | **Host organisation** | Advanced Space Technology And Applications Laboratories, Uyo |
    | **Output** | Reproducible geospatial framework + live Streamlit dashboard |
    """)

    st.markdown("## What you can explore in this app")
    st.markdown("""
    1. Read the project story and academic framing (this page)  
    2. Inspect headline KPIs for any epoch  
    3. Compare thermal maps across nine years  
    4. Inspect four-class land cover change and heat by class  
    5. Follow multi-year trends in vegetation versus built-up cover  
    6. See the statistical cooling and heating relationships  
    7. Open the full technical methodology and references  
    """)

    with st.expander("💬 One-minute pitch you can use in the defence"):
        st.markdown("""
        *"I built an open geospatial framework that ingests Landsat Level-2 imagery for Uyo LGA,
        derives temperature and land-cover indicators for 2016, 2019, 2022 and 2025, and publishes
        the results in a live dashboard. The evidence shows vegetation is associated with cooler
        surfaces and built-up cover with hotter surfaces, which supports targeted greening for
        Advanced Space Technology And Applications Laboratories and urban planning stakeholders."*
        """)

# ─────────────────────────────────────────────
# PAGE 2
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
        • Rising **NDBI** points to a stronger built-up / impervious surface signal.  
        • Falling **NDVI** points to vegetation canopy loss.  
        • **Mean LST** can move up or down with weather on the satellite overpass day.
          That is why this framework emphasises NDVI/NDBI relationships and spatial patterns,
          not only city-wide mean temperature.
        """
    )

    with st.expander("❓ Likely panel question: Why is mean LST not always higher in later years?"):
        st.markdown("""
        Because each Landsat scene is a morning snapshot. Air mass, humidity, and recent rainfall
        differ by date. A cooler city-mean in a later year does **not** cancel the urban heat mechanism.
        The stable evidence is: greener pixels stay cooler, built-up pixels stay hotter, and NDBI
        trends upward while NDVI trends downward across the decade.
        """)

# ─────────────────────────────────────────────
# PAGE 3
# ─────────────────────────────────────────────
elif view_mode == "3. Thermal Maps (All 4 Epochs)":
    st.title("🗺️ Surface Thermal Signature: All 4 Epochs")
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
        st.warning("`figures/fig3_spatial_lst_comparison.png` not found.")

    st.markdown("### Practical colour legend")
    leg1, leg2, leg3, leg4 = st.columns(4)
    leg1.info("**Dark purple / black**\nCooler surfaces\n(vegetation, shade, residual moisture)")
    leg2.success("**Orange / yellow**\nTypical urban and peri-urban surfaces")
    leg3.warning("**Bright yellow / white-hot**\nHottest surfaces\n(built-up cores, bare dry soil, roofs)")
    leg4.error("**Light grey patches**\nCloud / shadow masked\n(no valid observation)")

    st.markdown("""
    ### UHI intensity interpretation (relative to city mean)
    | Relative LST | Practical label | Planning meaning |
    |---|---|---|
    | Well below city mean | Cool island | Protect greenery and moisture corridors |
    | Near city mean | Typical | Background urban fabric |
    | Above mean | Warm / moderate UHI | Greening opportunity |
    | Strongly above mean | Hot / strong UHI | Priority mitigation zone |
    """)

    with st.expander("💬 What should I say while pointing at these maps?"):
        st.markdown("""
        *"These are land surface temperatures, not air temperatures. The bright cores mark surfaces
        that heated strongly by mid-morning overpass. Grey holes are intentional quality masking of
        cloud and shadow, not missing software output."*
        """)

# ─────────────────────────────────────────────
# PAGE 4
# ─────────────────────────────────────────────
elif view_mode == "4. Land Cover Maps (4 Classes)":
    st.title("🗺️ Four-Class Land Surface Maps")
    st.markdown(
        """
        **How to read this page in two steps:**  
        1. The maps show **where** each surface type is located.  
        2. The chart below shows **how hot** each surface type is, on average.
        """
    )

    if os.path.exists("figures/fig4_landcover_classification.png"):
        st.image(
            Image.open("figures/fig4_landcover_classification.png"),
            caption="4-class surface maps · threshold rules on NDVI, NDBI, MNDWI",
            use_container_width=True,
        )
    else:
        st.warning("`figures/fig4_landcover_classification.png` not found.")

    st.markdown("### Class rules used in this framework")
    st.code(
        """
Water / Wetland : MNDWI > 0
Vegetation      : NDVI > 0.35  (and not water)
Built-up        : NDBI > 0     (and not water/vegetation)
Bare ground     : remaining valid land pixels (low NDVI, low NDBI)
Cloud / Mask    : QA_PIXEL cloud and shadow bits
        """.strip()
    )

    if df_lulc is not None:
        st.subheader("Class area share (%) and mean LST by class")
        st.dataframe(df_lulc, use_container_width=True)

        temp_cols = [c for c in df_lulc.columns if "Mean_Temp" in c]
        if temp_cols:
            st.markdown("#### 🔥 Linking land cover to heat")
            st.caption(
                "Built-up and bare ground typically run hotter than vegetation. "
                "That contrast is the surface urban heat mechanism."
            )
            plot_df = df_lulc.melt(
                id_vars=["Year"] if "Year" in df_lulc.columns else df_lulc.columns[:1],
                value_vars=temp_cols,
                var_name="Class",
                value_name="Mean_LST_C",
            )
            plot_df["Class"] = (
                plot_df["Class"]
                .str.replace("Mean_Temp_", "", regex=False)
                .str.replace("_C", "", regex=False)
            )
            color_map = {
                "Veg": "#2ca02c",
                "Vegetation": "#2ca02c",
                "Built": "#d95f02",
                "BuiltUp": "#d95f02",
                "Bare": "#8c564b",
                "BareGround": "#8c564b",
                "Water": "#1f77b4",
            }
            x_col = "Year" if "Year" in plot_df.columns else plot_df.columns[0]
            fig = px.bar(
                plot_df,
                x=x_col,
                y="Mean_LST_C",
                color="Class",
                barmode="group",
                color_discrete_map=color_map,
                title="Mean Land Surface Temperature by Land-Cover Class",
                labels={"Mean_LST_C": "Mean LST (°C)", "Class": "Land category"},
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown(
                """
                **Colour key for the bars**  
                - 🟩 **Green = Vegetation** (usually coolest)  
                - 🟧 **Orange = Built-up** (usually hot)  
                - 🟫 **Brown = Bare ground** (often very hot when dry)  
                - 🟦 **Blue = Water / wetland** (when detected)
                """
            )

    st.warning(
        """
        **About the 2019 bare-ground surge**  
        A single dry-season scene can show more bare soil after harvest or under drier Harmattan
        conditions. Threshold classification is indicative, not a fully supervised land-cover product.
        The multi-year story that remains robust is: **NDBI up, NDVI down** across the decade.
        """
    )

    with st.expander("❓ Why is open water limited in Uyo maps?"):
        st.markdown("""
        Uyo is an inland LGA. Many drainage channels are narrow and tree-covered. At Landsat's 30 m
        resolution those features often become mixed pixels, so open-water percentage stays modest.
        That is a sensor-resolution reality, not a claim that Uyo has no hydrology.
        """)

# ─────────────────────────────────────────────
# PAGE 5
# ─────────────────────────────────────────────
elif view_mode == "5. Decadal Time-Series Trends" and data_loaded:
    st.title("📈 Decadal Time-Series Trends (2016 - 2025)")
    st.markdown("Four-point trajectories for vegetation, built-up signal, and mean surface temperature.")

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_summary["Epoch"], y=df_summary["Mean_NDBI"],
        name="Built-Up Index (NDBI)", mode="lines+markers",
        line=dict(color="#d95f02", width=3),
        marker=dict(size=10),
    ))
    fig_trend.add_trace(go.Scatter(
        x=df_summary["Epoch"], y=df_summary["Mean_NDVI"],
        name="Vegetation Index (NDVI)", mode="lines+markers",
        line=dict(color="#2ca02c", width=3),
        marker=dict(size=10),
    ))
    fig_trend.update_layout(
        title="Structural shift across Uyo LGA (2016-2025): Built-up vs Vegetation",
        xaxis_title="Epoch",
        yaxis_title="Index value (dimensionless)",
        legend_title="Indicator",
        hovermode="x unified",
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown(
        """
        **How to read the first chart**  
        - 🟧 **Orange line = NDBI (built-up signal)**  
        - 🟩 **Green line = NDVI (vegetation signal)**  
        If orange rises while green falls, the landscape is shifting toward more built / less canopy cover.
        """
    )

    fig_temp = px.line(
        df_summary, x="Epoch", y="Mean_LST_C", markers=True,
        title="Mean Land Surface Temperature (°C) by epoch (2016-2025)",
        labels={"Mean_LST_C": "Mean LST (°C)", "Epoch": "Epoch"},
    )
    fig_temp.update_traces(line_color="#c51b8a", line_width=3, marker=dict(size=10))
    st.plotly_chart(fig_temp, use_container_width=True)

    st.info(
        """
        **Interpretation guide**  
        • **NDBI rising** = stronger built-up / bare-impervious spectral signal  
        • **NDVI falling** = reduced green canopy  
        • **Mean LST** alone is weather-sensitive. Use it together with NDVI, NDBI, and the maps.
        """
    )

    with st.expander("💬 Defence sentence for this page"):
        st.markdown("""
        *"Across 2016 to 2025 the spectral evidence points to structural urban change in Uyo:
        the built-up index trends upward while vegetation declines. Temperature maps and class-wise
        means then show why that matters: built and bare surfaces carry higher heat loads."*
        """)

# ─────────────────────────────────────────────
# PAGE 6 — OLS with clear colours
# ─────────────────────────────────────────────
elif view_mode == "6. Statistical Relationships (OLS)":
    st.title("🔬 Statistical Relationships (Ordinary Least Squares)")

    st.markdown("""
    ## What question are we answering?

    > **When vegetation is higher, is the ground cooler?**  
    > **When built-up index is higher, is the ground hotter?**

    We answer with scatter plots of thousands of satellite pixels and a straight trend line
    (Ordinary Least Squares regression).
    """)

    st.markdown("""
    | Relationship | Colour used here | Expected UHI pattern | Meaning of the trend line |
    |---|---|---|---|
    | **LST vs NDVI** | 🟩 Green points | Negative | More green → lower surface temperature |
    | **LST vs NDBI** | 🟧 Orange points | Positive | More built-up → higher surface temperature |
    """)

    if df_sampled is not None:
        df_plot = df_sampled.copy()
        if "Year" in df_plot.columns:
            df_plot["Year"] = df_plot["Year"].astype(str)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🌿 Vegetation cools the surface")
            st.caption("Green points = vegetation relationship (NDVI). Not blue.")
            fig1 = px.scatter(
                df_plot,
                x="NDVI",
                y="LST",
                color_discrete_sequence=["#2ca02c"],
                trendline="ols",
                trendline_color_override="#006400",
                opacity=0.30,
                title="LST vs NDVI (cooling relationship)",
                labels={"NDVI": "NDVI (greenness)", "LST": "Land Surface Temp (°C)"},
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.success(
                "**Takeaway:** The cloud of points slopes **downward**. "
                "Greener pixels are generally cooler. That is the cooling association."
            )

        with c2:
            st.subheader("🏙️ Built-up heats the surface")
            st.caption("Orange points = built-up relationship (NDBI). Not blue.")
            fig2 = px.scatter(
                df_plot,
                x="NDBI",
                y="LST",
                color_discrete_sequence=["#d95f02"],
                trendline="ols",
                trendline_color_override="#8b0000",
                opacity=0.30,
                title="LST vs NDBI (heating relationship)",
                labels={"NDBI": "NDBI (built-up signal)", "LST": "Land Surface Temp (°C)"},
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.error(
                "**Takeaway:** The cloud of points slopes **upward**. "
                "More built-up pixels are generally hotter. That is the heating association."
            )

        st.markdown("### Optional: same relationships by epoch")
        show_by_year = st.checkbox("Show points coloured by year (for multi-epoch comparison)", value=False)
        if show_by_year and "Year" in df_plot.columns:
            y1, y2 = st.columns(2)
            with y1:
                fig1b = px.scatter(
                    df_plot, x="NDVI", y="LST", color="Year",
                    trendline="ols", opacity=0.25,
                    title="LST vs NDVI by epoch",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                )
                st.plotly_chart(fig1b, use_container_width=True)
            with y2:
                fig2b = px.scatter(
                    df_plot, x="NDBI", y="LST", color="Year",
                    trendline="ols", opacity=0.25,
                    title="LST vs NDBI by epoch",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                )
                st.plotly_chart(fig2b, use_container_width=True)
    else:
        st.warning("Sampled pixel CSV not found, so regression charts are unavailable in this build.")

    with st.expander("🧠 How to read OLS in one minute (interactive study note)"):
        st.markdown("""
        1. Each dot is one 30 m satellite pixel inside Uyo LGA.  
        2. The line is the best straight-line fit through the cloud of dots.  
        3. **Downward green line (NDVI)** = negative association = cooling linked to vegetation.  
        4. **Upward orange line (NDBI)** = positive association = heating linked to built-up surfaces.  
        5. Say **“associated with”**, not “causes”, because moisture, slope, and time of day also matter.  
        6. Neighbouring pixels are spatially correlated. Pixel OLS is a clear first-level evidence tool;
           advanced spatial models can be added later.
        """)

    with st.expander("❓ Mini quiz (tap to reveal answers)"):
        st.markdown("""
        **Q1.** If NDVI increases and LST falls, what urban design action does that support?  
        **A1.** Protect and expand tree canopy / green cover.

        **Q2.** If NDBI increases and LST rises, what does that imply for new estates and roads?  
        **A2.** New impermeable surfaces intensify local heat unless cooling measures are included.

        **Q3.** Why avoid saying “NDVI causes cool temperatures” in the defence?  
        **A3.** The analysis shows association. Causation needs stronger experimental or quasi-experimental design.
        """)

    if df_reg is not None:
        st.subheader("Numeric model summary")
        st.dataframe(df_reg, use_container_width=True)

# ─────────────────────────────────────────────
# PAGE 7
# ─────────────────────────────────────────────
elif view_mode == "7. Full Methodology & Documentation":
    st.title("📖 Full Project Methodology & Documentation")

    st.markdown("""
    ## 1. Project identity

    **Title:** End-to-End Geospatial Data Analysis of Urban Heat Island Dynamics in Uyo LGA:
    A Reproducible Python Framework and Interactive Dashboard for Satellite-Derived Surface
    Temperature Monitoring (2016-2025)

    **Type:** Industrial Training (IT) defence project · Data Analysis track  
    **Host organisation:** Advanced Space Technology And Applications Laboratories, Uyo, Akwa Ibom State  

    ---

    ## 2. Aim

    To develop a reproducible Python-based geospatial analytics **framework** that quantifies
    multi-temporal Surface Urban Heat Island patterns in Uyo LGA using Landsat 8/9 Collection 2
    Level-2 data, and to deliver results through an interactive dashboard usable by non-GIS specialists.

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
    - **Climate note:** Humid tropical; dry season (about November to February) is the practical clear-sky window  

    ---

    ## 4. Data

    | Dataset | Source | Role |
    |---|---|---|
    | Landsat 8/9 C2 L2 | Microsoft Planetary Computer / USGS | SR bands + ST_B10 + QA_PIXEL |
    | Uyo LGA polygon | geoBoundaries | Clip and study extent |
    | Epochs | Dry-season scenes around **2016, 2019, 2022, 2025** | Multi-temporal change |

    ### Level-2 scale factors
    $$
    \\text{Reflectance} = DN \\times 0.0000275 - 0.2
    $$
    $$
    \\text{LST (°C)} = (DN \\times 0.00341802 + 149.0) - 273.15
    $$

    **Important:** Collection 2 Level-2 `ST_B10` is already a surface temperature product.
    Planck / single-channel Level-1 formulas are not re-applied.

    ### QA masking
    Pixels flagged as fill, dilated cloud, cloud, or cloud shadow in `QA_PIXEL` are removed before
    index computation.

    ---

    ## 5. Spectral indices

    $$
    \\mathrm{NDVI} = \\frac{NIR - Red}{NIR + Red}
    $$
    $$
    \\mathrm{NDBI} = \\frac{SWIR1 - NIR}{SWIR1 + NIR}
    $$
    $$
    \\mathrm{MNDWI} = \\frac{Green - SWIR1}{Green + SWIR1}
    $$
    $$
    \\mathrm{UTFVI} = \\frac{LST - \\overline{LST}}{LST}
    $$

    ### Four-class surface rules
    - **Water/Wetland:** MNDWI > 0  
    - **Vegetation:** NDVI > 0.35  
    - **Built-up:** NDBI > 0  
    - **Bare ground:** remaining valid land (low NDVI and low NDBI)

    ---

    ## 6. Analytical methods

    1. Exploratory distribution analysis of LST, NDVI, and NDBI per epoch  
    2. Pearson correlation and OLS trend lines for LST versus NDVI and LST versus NDBI  
    3. Multi-temporal comparison across four epochs  
    4. Class-wise mean LST to link land cover to heat  
    5. Interactive dashboard communication in Streamlit and Plotly  

    ---

    ## 7. Key findings

    - Built-up spectral signal (NDBI) increased across the decade.  
    - Vegetation signal (NDVI) declined.  
    - LST is negatively associated with NDVI (cooling) and positively associated with NDBI (heating).  
    - Built-up and bare classes show higher mean LST than dense vegetation.  
    - Narrow streams in Uyo are partly sub-pixel at 30 m, so mapped open-water share is modest for an inland LGA.

    ---

    ## 8. Scientific limitations

    1. **LST is not air temperature.** The satellite measures surface skin temperature near the morning overpass.  
    2. **Snapshot bias.** Each map is one clear-sky morning, not a full seasonal average.  
    3. **Weather between dates.** City-mean LST can differ because the atmosphere differed that morning.  
    4. **30 m resolution.** Fine courtyards and narrow streams become mixed pixels.  
    5. **Threshold classification** is transparent but not a field-validated supervised land-cover product.  
    6. **Spatial autocorrelation.** Neighbouring pixels are not independent; pixel OLS is associative evidence.

    ---

    ## 9. Recommendations

    1. Protect and expand tree canopy along major corridors and new estates.  
    2. Prioritise greening in persistent high-LST built-up cores visible on the thermal maps.  
    3. Avoid leaving large bare cleared sites exposed for long periods.  
    4. Institutionalise this open framework at Advanced Space Technology And Applications Laboratories
       as a low-cost monitoring product for additional Nigerian cities.

    ---

    ## 10. Reproducibility and software stack

    - **Language:** Python 3  
    - **Cloud processing environment:** Google Colab  
    - **Local development environment:** Visual Studio Code (VS Code)  
    - **Version control and hosting:** Git, GitHub, Streamlit Community Cloud  
    - **Core libraries:** rasterio, rioxarray, geopandas, numpy, pandas, matplotlib, plotly, streamlit, planetary-computer  
    - **Code repository:** GitHub `uyo_uhi`  
    - **Live application:** Streamlit Community Cloud  

    ---

    ## 11. Organisational relevance (IT defence)

    This project shows how **Advanced Space Technology And Applications Laboratories** can:
    - replace slow manual GIS repetition with a reproducible scripted framework  
    - deliver client-facing interactive intelligence without requiring every viewer to hold a proprietary GIS licence  
    - scale the same workflow from Uyo to other cities by changing the area-of-interest boundary and re-running the process  

    ---

    ## 12. References

    1. United States Geological Survey (USGS). (2021). *Landsat 8-9 Collection 2 Level-2 Science Products*. USGS Earth Resources Observation and Science Center.  
    2. Tucker, C. J. (1979). Red and photographic infrared linear combinations for monitoring vegetation. *Remote Sensing of Environment, 8*(2), 127-150.  
    3. Zha, Y., Gao, J., & Ni, S. (2003). Use of normalized difference built-up index in automatically mapping urban areas from TM imagery. *International Journal of Remote Sensing, 24*(3), 583-594.  
    4. Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. *International Journal of Remote Sensing, 27*(14), 3025-3033.  
    5. Voogt, J. A., & Oke, T. R. (2003). Thermal remote sensing of urban climates. *Remote Sensing of Environment, 86*(3), 370-384.  
    6. Microsoft Planetary Computer. (n.d.). *STAC API for Landsat Collection 2 Level-2*. https://planetarycomputer.microsoft.com/  
    """)

else:
    if not data_loaded and view_mode not in ["1. Project Introduction", "7. Full Methodology & Documentation"]:
        st.warning("Data files are not fully loaded. Introduction and Methodology pages still work.")