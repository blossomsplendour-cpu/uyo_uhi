import os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Pt, Inches

print("📄 Generating Full-Length 30-Page SIWES Word Document Report. Please wait...")

doc = Document()

# Set global styles
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)

def add_heading(doc, text, level, align=WD_ALIGN_PARAGRAPH.LEFT):
    h = doc.add_heading(text, level=level)
    h.alignment = align
    for run in h.runs:
        run.font.name = 'Arial'
        run.font.color.rgb = None
        run.bold = True

def add_para(doc, text, bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(12)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_after = space_after
    run = p.add_run(text)
    run.bold = bold
    return p

# ==========================================
# COVER PAGE
# ==========================================
for _ in range(3): doc.add_paragraph()
add_para(doc, "TECHNICAL REPORT ON THE STUDENTS INDUSTRIAL\nWORK EXPERIENCE SCHEME (SIWES)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(2): doc.add_paragraph()
add_para(doc, "UNDERTAKEN AT", align=WD_ALIGN_PARAGRAPH.CENTER)
add_para(doc, "ADVANCED SPACE TECHNOLOGY AND APPLICATIONS LABORATORIES (ASTAL)\nUYO, AKWA IBOM STATE", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(2): doc.add_paragraph()
add_para(doc, "BY", align=WD_ALIGN_PARAGRAPH.CENTER)
add_para(doc, "[STUDENT FULL NAME]\n[MATRICULATION NUMBER]", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(2): doc.add_paragraph()
add_para(doc, "DEPARTMENT OF COMPUTER SCIENCE,\nFACULTY OF COMPUTING,\nUNIVERSITY OF UYO, UYO.", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(2): doc.add_paragraph()
add_para(doc, "SUBMITTED TO\nDEPARTMENT OF COMPUTER SCIENCE,\nFACULTY OF COMPUTING,\nUNIVERSITY OF UYO, UYO.", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
for _ in range(2): doc.add_paragraph()
add_para(doc, "IN PARTIAL FULFILLMENT OF THE REQUIREMENT FOR THE AWARD OF\nBACHELOR OF SCIENCE (B.Sc.) DEGREE IN COMPUTER SCIENCE", align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ==========================================
# PROJECT TITLE PAGE
# ==========================================
for _ in range(5): doc.add_paragraph()
add_para(doc, "IT PROJECT ON", align=WD_ALIGN_PARAGRAPH.CENTER)
add_para(doc, "END-TO-END GEOSPATIAL DATA ANALYSIS OF URBAN HEAT ISLAND DYNAMICS IN UYO LGA: A REPRODUCIBLE PYTHON FRAMEWORK AND INTERACTIVE DASHBOARD FOR SATELLITE-DERIVED SURFACE TEMPERATURE MONITORING (2016–2025)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ==========================================
# PRELIMINARIES
# ==========================================
add_heading(doc, 'ABSTRACT', level=1, align=WD_ALIGN_PARAGRAPH.CENTER)
abstract_text = (
    "Rapid urbanisation across Uyo Local Government Area (LGA) has accelerated the conversion of natural forest canopy and agricultural land into impermeable built-up infrastructure. This spatial transformation significantly alters local surface energy balances, creating a Surface Urban Heat Island (SUHI) effect. This report details the 24-week Students Industrial Work Experience Scheme (SIWES) attachment completed at the Advanced Space Technology And Applications Laboratories (ASTAL), Uyo, Akwa Ibom State, alongside an applied Computer Science IT project.\n\n"
    "The report covers the complete technical progression across the 24-week period—starting from foundational space technology, satellite orbits, Nigerian satellites (NigeriaSat-1, NigeriaSat-2, NigeriaSat-X, NigComSat-1R), spatial coordinate systems, feature digitization, georeferencing, remote sensing physics, multispectral classification (ENVI and ArcGIS), and Principal Component Analysis (PCA), to modern open-source programmatic geospatial engineering using Python (GeoPandas, Rasterio, Shapely, SciPy), data analysis (NumPy, Pandas, Seaborn), and cloud-based web application deployment (Streamlit).\n\n"
    "The applied IT project engineered an automated, end-to-end Python geospatial framework to quantify decadal SUHI dynamics across Uyo LGA using USGS Landsat 8 and 9 Collection 2 Level-2 multispectral and thermal imagery across four dry-season epochs (2016, 2019, 2022, and 2025). The computational framework ingests data via SpatioTemporal Asset Catalog (STAC) APIs, applies bitmask quality filtering on the QA_PIXEL band, and derives scaled land surface temperature (LST °C) alongside spectral indices including NDVI (vegetation), NDBI (built-up), MNDWI (water), and UTFVI (thermal variance).\n\n"
    "A four-class surface classification scheme (Vegetation, Built-Up, Bare Soil, Water) was executed to monitor urban land cover transitions. Quantitative results reveal a decadal expansion in built-up density (mean NDBI increased from -0.031 in 2016 to -0.005 in 2025) accompanied by vegetation canopy loss (mean NDVI declined from 0.418 in 2016 to 0.382 in 2025). Ordinary Least Squares (OLS) regression models demonstrate a statistically significant negative relationship between LST and NDVI (surface cooling) and a positive relationship between LST and NDBI (microclimate heating). The entire workflow was deployed to the cloud as a live, interactive web application using Streamlit and Plotly, providing an accessible decision-support platform for urban planners."
)
add_para(doc, abstract_text)
doc.add_page_break()

add_heading(doc, 'DEDICATION', level=1, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para(doc, "This work is dedicated to Almighty God for the gift of life, wisdom, health, and perseverance throughout the duration of my academic journey and industrial training.\n\nIt is also dedicated to my beloved family for their unyielding moral, financial, and emotional support, and to every aspiring computer scientist committed to leveraging open-source software and Earth Observation data toward solving pressing environmental and spatial challenges in Nigeria.")
doc.add_page_break()

add_heading(doc, 'ACKNOWLEDGEMENTS', level=1, align=WD_ALIGN_PARAGRAPH.CENTER)
add_para(doc, "I extend my sincere gratitude to the Department of Computer Science, Faculty of Computing, University of Uyo, for establishing a rigorous academic foundation that prepared me for industry experience. I am deeply grateful to my academic supervisors and the SIWES coordinator for their continuous guidance, structural oversight, and constructive evaluation throughout this programme.\n\nSpecial appreciation goes to the Board of Management, Director, and technical staff of the Advanced Space Technology And Applications Laboratories (ASTAL), Uyo, Akwa Ibom State, for granting me the privilege to complete my 24-week industrial attachment within their facility. I express my profound gratitude to my industry supervisors—including Mr. Brain Okafor, Mr. Magnus, Dr. Dapo, Dr. Adamson Oloyede, and senior research scientists in the GIS, Remote Sensing, and IT Applications Division—for their hands-on instruction, exposure to operational space technologies, and continuous encouragement during the execution of this work.")
doc.add_page_break()

# ==========================================
# CHAPTER 1: INTRODUCTION
# ==========================================
add_heading(doc, 'CHAPTER 1: INTRODUCTION TO SIWES PLACEMENT', level=1)

add_heading(doc, '1.1 BACKGROUND OF THE SIWES PROGRAM', level=2)
add_para(doc, "The Students Industrial Work Experience Scheme (SIWES) was established by the Industrial Training Fund (ITF) in 1973 to address the challenge of inadequate practical exposure among university graduates in engineering, science, technology, and applied disciplines across Nigeria. The scheme is a mandatory, credit-bearing component of the Bachelor of Science (B.Sc.) Computer Science curriculum.")
add_para(doc, "SIWES serves as a practical bridge connecting theoretical classroom instructions with real-world industry applications. For a Computer Science student, the scheme provides vital exposure to industrial software suites, specialized computational data stacks, satellite data pipelines, cloud computing architectures, and hardware infrastructure that are not typically available in academic laboratories. Furthermore, it integrates students into professional work ethics, interdisciplinary collaboration, and technical project management.")

add_heading(doc, '1.2 ABOUT ADVANCED SPACE TECHNOLOGY AND APPLICATIONS LABORATORIES (ASTAL), UYO', level=2)
add_para(doc, "The Advanced Space Technology And Applications Laboratories (ASTAL), Uyo, is an advanced research institute under the National Space Research and Development Agency (NASRDA), operating under the Federal Ministry of Innovation, Science and Technology, Nigeria.")
add_para(doc, "ASTAL Uyo was established to drive research, development, and capacity building in satellite remote sensing, Geographic Information Systems (GIS), spatial computing, global navigation satellite systems (GNSS), and environmental monitoring. The laboratory serves as a regional space application center covering the Niger Delta and South-South geopolitical zone of Nigeria, focusing on coastal management, urban heat monitoring, forestry mapping, flood modeling, and geospatial software automation.")

add_heading(doc, '1.3 HISTORY, VISION, MISSION, AND CORE VALUES OF ASTAL', level=2)
add_para(doc, "ASTAL Uyo was created as part of NASRDA's strategic decentralization policy to establish specialized space application laboratories across Nigeria's geopolitical zones. Located in Uyo, Akwa Ibom State, ASTAL was positioned to address environmental challenges unique to the humid tropical belt and oil-producing coastal ecosystems, including rapid urban expansion, deforestation, oil spill tracking, coastal erosion, and urban microclimate shifts.")
add_para(doc, "Vision Statement: To be a premier center of excellence in satellite technology applications, driving sustainable socio-economic development through innovative spatial computing, environmental intelligence, and space-derived solutions.")
add_para(doc, "Mission Statement: To harness space science and satellite remote sensing technology through applied research, capacity development, and user-friendly geospatial software solutions to address environmental, agricultural, urban, and ecological challenges in Nigeria.")
add_para(doc, "Core Values:\n• Innovation: Developing modern programmatic workflows and open-source software tools for spatial data processing.\n• Accuracy: Maintaining rigorous scientific standards in satellite data calibration, cloud masking, and spatial statistics.\n• Integrity: Ensuring scientific transparency, data reproducibility, and compliance with open-data principles.\n• Capacity Building: Mentoring students and researchers to build national competency in space technology and computer science.")

add_heading(doc, '1.4 ORGANIZATIONAL STRUCTURE AND UNIT ATTACHMENT', level=2)
add_para(doc, "ASTAL Uyo is structured into specialized technical and administrative units to execute its mandates, including the Directorate, Remote Sensing and Earth Observation Unit, Geographic Information Systems (GIS) and Spatial Computing Unit, Software Engineering and IT Infrastructure Unit, and the Administration and Finance Division.")
add_para(doc, "During the 24-week SIWES attachment, the author was attached to the GIS, Remote Sensing, and IT Applications Division. This placement provided direct exposure to spatial software environments (ArcGIS, ENVI, QGIS), Python spatial programming, satellite data APIs, database management, and web dashboard engineering.")

add_heading(doc, '1.5 DURATION AND SCOPE OF INTERNSHIP', level=2)
add_para(doc, "The industrial attachment spanned a period of six months (24 weeks, covering April 2026 to September 2026). The practical scope of work assigned during this period included Space Science Foundations, Desktop GIS & Cartography, Multispectral Image Classification, Band Math and PCA, Open-Source Geospatial Engineering in Python, Scientific Computing/Machine Learning, and Full-Stack Cloud Web Application Deployment.")
doc.add_page_break()

# ==========================================
# CHAPTER 2: PRACTICAL SKILLS
# ==========================================
add_heading(doc, 'CHAPTER 2: PRACTICAL SKILLS ACQUIRED DURING SIWES', level=1)

add_heading(doc, '2.1 ORIENTATION, SPACE TECHNOLOGY FOUNDATIONS, AND NIGERIAN SATELLITE SYSTEMS (WEEKS 1–2)', level=2)
add_para(doc, "The initial weeks of the attachment were dedicated to formal orientation, introduction to space science principles, and understanding the operational framework of Nigerian satellite assets under the guidance of Mr. Brain Okafor.")
add_para(doc, "Students studied orbital mechanics, satellite trajectories, and orbital classifications, including Low Earth Orbit (LEO) for Earth observation, Medium Earth Orbit (MEO) for navigation, and Geostationary Earth Orbit (GEO) for telecommunications. Detailed analysis was conducted on satellites launched by Nigeria through NASRDA, including NigeriaSat-1, NigComSat-1/1R, NigeriaSat-2, and NigeriaSat-X.")

add_heading(doc, '2.2 CARTOGRAPHY, SPATIAL DATA MODELS, AND COORDINATE REFERENCE SYSTEMS (WEEKS 3–5)', level=2)
add_para(doc, "Under the instruction of Mr. Magnus, practical sessions focused on establishing core competencies in desktop Geographic Information Systems (GIS) software, spatial database structures, and cartographic standards using ArcMap 10.5.")
add_para(doc, "Practical knowledge was acquired in differentiating between Geographic Coordinate Systems (GCS), which use spherical coordinates based on angular degrees (WGS84), and Projected Coordinate Systems (PCS), which utilize flat metric grids necessary for accurate distance, area, and buffer calculations (UTM Zone 32N).")

add_heading(doc, '2.3 GEOREFERENCING, GEOPROCESSING, AND IMAGE CLASSIFICATION BASICS (WEEKS 6–8)', level=2)
add_para(doc, "Weeks 6 through 8 introduced spatial image alignment, vector geoprocessing tools, and fundamental remote sensing physics. Practical skills included assigning real-world spatial coordinates to unreferenced rasters using Ground Control Points (GCPs) and executing geoprocessing tools such as Buffer, Clip, Intersect, and Union.")
add_para(doc, "Fundamental remote sensing physics was explored, detailing how solar radiation interacts with Earth's surface matter (Absorption, Transmission, and Reflection) to create distinct spectral signatures for vegetation, water, and built-up concrete.")

add_heading(doc, '2.4 DIGITAL IMAGE PROCESSING AND MULTISPECTRAL CLASSIFICATION (WEEKS 9–12)', level=2)
add_para(doc, "Under the instruction of Dr. Dapo, practical exercises advanced into digital image processing and land cover classification using ENVI and ArcGIS. Skills acquired included handling Landsat 7 ETM+, Landsat 8 OLI/TIRS, and Sentinel-2 MSI satellite scenes, executing image subsetting, and constructing False Color Composites (FCC).")
add_para(doc, "Advanced supervised classification algorithms, such as Mahalanobis Distance Classification, were executed to categorize pixels based on directional covariance between spectral bands, followed by raster-to-polygon vectorization and statistical area quantification in hectares.")

add_heading(doc, '2.5 LULC CHANGE DETECTION AND ADVANCED SYMBOLOGY (WEEKS 13–15)', level=2)
add_para(doc, "Weeks 13 through 15 focused on applied geospatial project execution, synthesizing Sentinel-2 and Landsat data to analyze multi-decade Land Use / Land Cover (LULC) shifts. An applied case study compared land surface shifts in Ini LGA between 2003 and 2025, quantifying agricultural expansion and deforestation.")
add_para(doc, "Advanced map cartography techniques were mastered, applying Choropleth maps and graduated symbology alongside complete cartographic layouts (Title, Legend, North Arrow, Scale Bar).")

add_heading(doc, '2.6 BAND MATH, PCA, AND TRANSITION TO PYTHON FOR GIS (WEEK 16)', level=2)
add_para(doc, "Week 16 marked a major milestone: transitioning from manual graphical software menus to algorithmic processing and open-source Python spatial programming. Principal Component Analysis (PCA) was conducted to reduce spectral redundancy by analyzing Eigenvalues and Eigenvectors derived from the image covariance matrix.")
add_para(doc, "Python environments were configured using Anaconda, installing core geospatial libraries (GeoPandas, Rasterio, Shapely, PyProj) to transition workflows into programmatic environments.")

add_heading(doc, '2.7 PROGRAMMATIC VECTOR AND RASTER DATA ENGINEERING (WEEKS 17–20)', level=2)
add_para(doc, "Weeks 17 through 20 converted desktop GIS workflows into reproducible, automated Python code. Using GeoPandas and Shapely, programmatic vector operations were executed, including buffering metric proximity zones, dissolving polygon boundaries, clipping vector layers, and performing spatial joins (sjoin).")
add_para(doc, "Raster arrays were ingested and clipped using Rasterio and RioXarray. Zonal statistics were programmatically computed using the 'rasterstats' library to extract mean, min, max, and standard deviation metrics from raster grids within vector administrative boundaries.")

add_heading(doc, '2.8 SCIENTIFIC COMPUTING, MACHINE LEARNING LIBRARIES, AND EDA (WEEKS 21–23)', level=2)
add_para(doc, "To strengthen computer science competencies, Weeks 21 through 23 focused on data science, scientific computing, machine learning tools, and Exploratory Data Analysis (EDA). Practical applications utilized Python's NumPy library for multi-dimensional array creation, slicing, boolean masking, and vectorized arithmetic operations.")
add_para(doc, "Pandas DataFrames were used for tabular data cleaning, missing value handling, and data reshaping. Data visualization was mastered using Matplotlib and Seaborn to construct publication-style statistical figures, including KDE distributions, bar charts, regression scatter plots, and correlation heatmaps.")

add_heading(doc, '2.9 CAPSTONE RESEARCH AND TECHNICAL PRESENTATION (WEEK 24)', level=2)
add_para(doc, "The final week focused on research design, supervisory evaluation, and project presentation. A capstone IT project topic was selected: End-to-End Geospatial Data Analysis of Urban Heat Island Dynamics in Uyo LGA. Technical slides and web deployment architectures were presented to ASTAL technical supervisors for final assessment and grading.")
doc.add_page_break()

# ==========================================
# CHAPTER 3: IT PROJECT
# ==========================================
add_heading(doc, 'CHAPTER 3: IT PROJECT ON GEOSPATIAL ANALYSIS OF URBAN HEAT ISLAND DYNAMICS', level=1)

add_heading(doc, '3.1 PROJECT OVERVIEW', level=2)
add_para(doc, "This chapter presents the primary IT project executed during the industrial attachment at ASTAL, Uyo. The project engineered an end-to-end, open-source Python computational framework designed to process multispectral and thermal satellite imagery from Landsat 8 and Landsat 9 Collection 2 Level-2 products. The system quantifies multi-temporal Surface Urban Heat Island (SUHI) patterns across Uyo Local Government Area across a 9-year decadal window (2016, 2019, 2022, and 2025).")

add_heading(doc, '3.2 BACKGROUND OF THE STUDY', level=2)
add_para(doc, "Uyo, the capital city of Akwa Ibom State, Nigeria, has experienced rapid urban growth, population influx, and infrastructure development since its creation in 1987. The expansion of administrative buildings, commercial centers, residential estates, and transportation networks has led to extensive land clearing and canopy loss.")
add_para(doc, "When natural vegetated surfaces are replaced with dark, impermeable construction materials (concrete, asphalt, corrugated roofing sheets), the localized surface energy balance changes dramatically. Natural vegetation provides microclimate cooling through evapotranspiration and canopy shading. In contrast, urban construction materials possess high thermal heat capacities and low albedos, causing them to absorb, store, and re-radiate intense solar radiation, creating Surface Urban Heat Islands (SUHI).")

add_heading(doc, '3.3 PROBLEM STATEMENT', level=2)
add_para(doc, "The rapid urban expansion of Uyo LGA presents several challenges: Urban planning authorities lack automated, high-resolution spatial tools to pinpoint microclimatic thermal hotspots; forest clearing is eroding natural cooling buffers without quantitative tracking; traditional GIS implementations rely on expensive, proprietary software licenses; and static paper maps fail to provide interactive decision tools accessible via web browsers.")

add_heading(doc, '3.4 AIM AND OBJECTIVES', level=2)
add_para(doc, "Aim: To develop a reproducible Python geospatial software framework and interactive web dashboard that ingests multi-temporal Landsat Level-2 satellite imagery, derives spectral indicators and land surface temperature (°C), models land-cover microclimate relationships, and tracks SUHI dynamics across Uyo LGA from 2016 to 2025.")
add_para(doc, "Objectives:\n1. Programmatically acquire and preprocess Landsat 8/9 Collection 2 Level-2 imagery across four dry-season epochs.\n2. Execute QA_PIXEL filtering to mask cloud artifacts.\n3. Derive spectral indices (NDVI, NDBI, MNDWI, UTFVI) and scaled Land Surface Temperature (LST °C).\n4. Implement a 4-class land surface classification scheme to track decadal transitions.\n5. Compute Ordinary Least Squares (OLS) regression models to prove statistical microclimate relationships.\n6. Deploy a live, interactive full-stack web dashboard using Streamlit, Plotly, and GitHub.")

add_heading(doc, '3.5 DATA SOURCES AND ACQUISITION', level=2)
add_para(doc, "The project utilized USGS Landsat Collection 2 Level-2 Science Products sourced programmatically via the Microsoft Planetary Computer STAC API. Four dry-season scenes (Jan 2016, Jan 2019, Jan 2022, Jan 2025) covering Path 188 / Row 056 were selected to minimize cloud cover (all scenes <3.0% cloud cover). The spatial boundary was derived from the geoBoundaries ADM2 Administrative dataset for Uyo LGA (EPSG:32632).")

add_heading(doc, '3.6 METHODOLOGY AND TECHNICAL FORMULATIONS', level=2)
add_para(doc, "USGS Landsat Collection 2 Level-2 products store pixel values as unsigned integers. The official scaling equations were programmatically applied:")
add_para(doc, "Surface Reflectance (SR) = (DN * 0.0000275) - 0.2")
add_para(doc, "Land Surface Temperature (LST °C) = (DN * 0.00341802 + 149.0) - 273.15")
add_para(doc, "Spectral indices were calculated via raster array math:\n• NDVI = (NIR - Red) / (NIR + Red)\n• NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)\n• MNDWI = (Green - SWIR1) / (Green + SWIR1)")
add_para(doc, "A four-class decision-tree threshold rule was applied across valid pixels: Water Bodies (MNDWI > 0.0), Vegetation Canopy (NDVI > 0.35), Built-Up Infrastructure (NDBI > 0.0), and Bare Soil (remaining valid pixels).")

add_heading(doc, '3.7 DATA ANALYSIS, RESULTS, AND FINDINGS', level=2)
add_para(doc, "Quantitative analysis revealed a severe decadal structural landscape shift. Built-Up Expansion (NDBI) increased continuously from a mean of -0.031 in 2016 to -0.005 in 2025. Conversely, Vegetation Canopy Loss (NDVI) dropped continuously from 0.418 in 2016 to 0.382 in 2025. Maximum surface temperatures across all dry-season epochs consistently reached 41.12°C to 43.48°C in densely built urban cores.")

add_heading(doc, '3.8 ANALYSIS OF KEY FACTORS AND MICROCLIMATE DRIVERS', level=2)
add_para(doc, "To mathematically evaluate microclimate dynamics, samples of 10,000 pixels per epoch were evaluated using Ordinary Least Squares (OLS) linear regression models. LST versus NDVI showed a statistically significant negative Pearson correlation (r = -0.58 to -0.64), proving that higher vegetation canopy actively cools the land surface. LST versus NDBI showed a statistically significant positive Pearson correlation (r = +0.62 to +0.71), proving that built-up density directly increases surface heating.")

add_heading(doc, '3.9 SYSTEM ARCHITECTURE AND CLOUD DEPLOYMENT', level=2)
add_para(doc, "The system architecture separated heavy cloud computation from lightweight web application rendering. Data was processed in Google Colab utilizing Python geospatial libraries. Code logic and modular scripting were managed locally in VS Code, with source control managed via GitHub. The final interactive application was deployed 24/7 on Streamlit Community Cloud.")

add_heading(doc, '3.10 SCIENTIFIC LIMITATIONS OF THE STUDY', level=2)
add_para(doc, "Limitations include: Satellite thermal sensors measure radiometric surface skin temperature (LST), which is not identical to 2-meter ambient air temperature. Landsat overpasses occur at 10:30 AM local time, representing mid-morning snapshot conditions rather than afternoon thermal peaks. Fine-scale urban features are subject to sub-pixel spatial mixing at 30-meter resolution.")

add_heading(doc, '3.11 CONCLUSION AND RECOMMENDATIONS', level=2)
add_para(doc, "This project successfully developed an automated, open-source Python software framework to analyze SUHI dynamics across Uyo LGA. Results proved that rapid urban development drove significant built-up expansion and canopy loss from 2016 to 2025, which mathematically intensified local surface temperatures. It is highly recommended that municipal planning authorities mandate green buffer zones along expanding transport arteries. Furthermore, ASTAL Uyo should institutionalize this open-source Python framework to replace proprietary GIS workflows, drastically reducing software licensing costs.")
doc.add_page_break()

# ==========================================
# REFERENCES
# ==========================================
add_heading(doc, 'REFERENCES', level=1)
refs = [
    "Microsoft Planetary Computer. (2025). STAC API Catalog for Landsat Collection 2 Level-2 Products. https://planetarycomputer.microsoft.com/",
    "Tucker, C. J. (1979). Red and photographic infrared linear combinations for monitoring vegetation. Remote Sensing of Environment, 8(2), 127–150.",
    "United States Geological Survey (USGS). (2021). Landsat 8-9 Collection 2 Level-2 Science Products Guide (Version 2.0). Earth Resources Observation and Science (EROS) Center.",
    "Voogt, J. A., & Oke, T. R. (2003). Thermal remote sensing of urban climates. Remote Sensing of Environment, 86(3), 370–384.",
    "Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. International Journal of Remote Sensing, 27(14), 3025–3033.",
    "Zha, Y., Gao, J., & Ni, S. (2003). Use of normalized difference built-up index in automatically mapping urban areas from TM imagery. International Journal of Remote Sensing, 24(3), 583–594."
]
for r in refs:
    add_para(doc, "• " + r)
doc.add_page_break()

# ==========================================
# APPENDICES
# ==========================================
add_heading(doc, 'APPENDICES', level=1)

add_heading(doc, 'APPENDIX A: COMPLETE CHRONOLOGICAL SIWES LOGBOOK (WEEKS 1–24)', level=2)
add_para(doc, "The following table represents the complete, verbatim transcription of the official SIWES logbook recorded during the 24-week industrial attachment at ASTAL Uyo.")

# Create the giant 24-week logbook table
table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Week No.'
hdr_cells[1].text = 'Dates / Week Ending'
hdr_cells[2].text = 'Daily Activities Recorded'

logbook_data = [
    ("Week 1", "1st April – 3rd April 2026", "MON: Intro to Space Technology, GIS components.\nTUE: Satellites Types and Examples.\nWED: Space and its elements.\nTHUR: Satellites Launched in Nigeria.\nFRI: Good Friday (Public Holiday)."),
    ("Week 2", "6th April – 10th April 2026", "MON: Easter Monday.\nTUE: Uses and Examples of Satellites.\nWED: GIS and its Components.\nTHUR: Longitude and Latitude.\nFRI: Nigerian Shapefile and Boundaries."),
    ("Week 3", "13th April – 17th April 2026", "MON: Layering and Mapping out a Map.\nTUE: Spatial Data and Types.\nWED: Coordinate Systems (CRS).\nTHUR: Continuation of Coordinate Systems.\nFRI: Introduction to Arc GIS -> Mapping out Road, Settlements, legend."),
    ("Week 4", "20th April – 24th April 2026", "MON: Arc GIS Interface and Components.\nTUE: Orientation with the Managing Board -> Civil Service.\nWED: Layers in GIS and Operations.\nTHUR: Four Major Satellites Launch by Nigeria.\nFRI: International Space Station (ISS), History, Components & Structures."),
    ("Week 5", "27th April – 1st May 2026", "MON: Space Orbit & Movement, Functions and Characteristics.\nTUE: Rain Check on GIS, its components and functions.\nWED: GIS Data Models and Data Types.\nTHUR: Data Types and Functions.\nFRI: Spatial data / Attributes Data -> Assignment on Field Report."),
    ("Week 6", "4th May – 8th May 2026", "MON: Introduction to Georeferencing.\nTUE: Classification, Assigning Features and Coordinates on ArcMap 10.5.\nWED: Geoprocessing Framework and Set of Tools for Processing Maps and Images.\nTHUR: Assignment Presentation and Defense on Field Report.\nFRI: Supervised and Non-Supervised Classification, Assigning Coordinates and Feature."),
    ("Week 7", "11th May – 15th May 2026", "MON: Defining the environment in ArcGIS.\nTUE: Projected and Geographic Coordinate Systems.\nWED: Digitization of Maps, Creation of Features, Roads etc.\nTHUR: Creation of Area of Interest on Maps and Images.\nFRI: Continuation of Creation of Area of Interests on Maps and Images."),
    ("Week 8", "18th May – 22nd May 2026", "MON: Remote Sensing and Types.\nTUE: Platforms in Remote Sensing and How satellites Communicate with them.\nWED: Electromagnetic Radiation / Normalized Difference Vegetation Index (NDVI).\nTHUR: Electromagnetic Interaction with Matter / Reflection.\nFRI: Spectral Responses / Spectral Signatures -> Assignment: Spectral Signatures."),
    ("Week 9", "25th May – 29th May 2026", "MON: Image Classification using ENVI Software.\nTUE: Quantification of Images and Map Composition -> Assignment on Land Use Land Cover.\nWED: Public Holiday (Children's Day).\nTHUR: Public Holiday (Eid el Kabir).\nFRI: Map Composition."),
    ("Week 10", "1st June – 5th June 2026", "MON: Map Composition ENVI Software (Region of Interest) Using Landsat 7 & 8.\nTUE: Map Composition ENVI (Land Use Land Cover Classification).\nWED: Map Composition ENVI (Mahalanobis Classification).\nTHUR: Map Composition ENVI (Subset to Equilibrium).\nFRI: Map Composition ArcGIS (Raster to Polygon)."),
    ("Week 11", "8th June – 12th June 2026", "MON: Map Composition ArcGIS (Query, Merge and Edit Classification).\nTUE: Map Composition ArcGIS (Symbology and Colour Composites).\nWED: Map Composition ArcGIS (Area and Hectares of LULC).\nTHUR: Tailoring on Tables and Creating Barcharts on Excel.\nFRI: Public Holiday (Democracy Day)."),
    ("Week 12", "15th June – 19th June 2026", "MON: Map Composition using Sentinel Data (Layers Composition) on ArcGIS.\nTUE: Map Composition using Sentinel Data (Abstraction of Region of Interest).\nWED: General Presentation by ASTAL Staff.\nTHUR: Map Composition using Sentinel Data on ENVI (Region of Interest and Classification).\nFRI: Map Composition using Sentinel Data (LULC Classification) on ENVI."),
    ("Week 13", "22nd June – 26th June 2026", "MON: Map Composition using Sentinel Data (Subset to Equilibrium) in ENVI.\nTUE: Map Composition using Sentinel Data (Raster to Polygon) using ArcGIS.\nWED: Map Composition using Sentinel Data (Query, Merge and Edit Classification).\nTHUR: Map Composition using Sentinel Data (Area of LULC) using ArcGIS.\nFRI: Map Composition using Sentinel Data (Export to Excel, Create Barcharts)."),
    ("Week 14", "29th June – 3rd July 2026", "MON: Project to determine LULC changes using Landsat and Sentinel (2003 - 2025) in Ini LGA.\nTUE: Continuation of Project.\nWED: Continuation of Project.\nTHUR: Report on the Project to determine the changes in LULC.\nFRI: Map layering and export with Design including Title, Legend, Scale Bar, North Arrow and Coordinate Grid."),
    ("Week 15", "6th July – 10th July 2026", "MON: Symbolization of Spatial Drawing of data to collect Coordinate point in field.\nTUE: Symbolization of spatial drawing using Choropleth map and Graduated Colours.\nWED: Spatial Join and Relate / Graduated Symbology.\nTHUR: Indices in ArcGIS -> Variants in NDVI.\nFRI: Digitization and Creation of Boundaries -> Longitude, Latitude and Correction of Hemisphere."),
    ("Week 16", "13th July – 17th July 2026", "MON: Spectral Indices Calculation using Band Math.\nTUE: Analysed Eigen Values and Eigen Vectors leading to Identify useful PCs.\nWED: Introduction to Google Earth Engine -> Functions and Interface.\nTHUR: Introduction to Python for GIS -> Variables and Lists etc.\nFRI: Python Environment in GIS -> Activating Conda Installation and Set up."),
    ("Week 17", "20th July – 24th July 2026", "MON: Using Python on Jupyter Lab -> Using Python on Google Colab.\nTUE: Buffering in Python.\nWED: Introduction to QGIS, Settings and Features -> Installation.\nTHUR: GeoPandas -> Working with Shapefiles.\nFRI: Rasterio -> Working with Raster Data -> Did Hands-on Exercise."),
    ("Week 18", "27th July – 31st July 2026", "MON: Spatial Analysis with Python -> Coordinate Reference Systems (CRS): GCS and PCS.\nTUE: Vector Operations with GeoPandas -> Buffer, Dissolve, Clip and Spatial Join.\nWED: Zonal Statistics with raster stats.\nTHUR: Making Maps with Matplotlib.\nFRI: Hands-on Exercise."),
    ("Week 19", "3rd August – 7th August 2026", "MON: Continuation of Google Earth Engine -> Code Editor.\nTUE: Installed ML Packages on Anaconda: NumPy, Pandas, Matplotlib, Jupyter, Rasterio.\nWED: General Presentation By ASTAL STAFF.\nTHUR: Introduction to QGIS, Settings and Features.\nFRI: Adding Base Maps To QGIS: Google Satellite, Google Hybrid, Google Streets, OSM, Esri World Imagery."),
    ("Week 20", "10th August – 14th August 2026", "MON: Mapping out features like road, buildings, settlements etc.\nTUE: Creation of Boundaries and Clipping.\nWED: General Presentation by ASTAL Staff.\nTHUR: Digitization.\nFRI: Hands-on Exercise and Field Work."),
    ("Week 21", "17th August – 21st August 2026", "MON: Worked on Python for Machine Learning and its Overview.\nTUE: Installation of Python for Machine Learning.\nWED: NumPy - Numerical Computing for Machine Learning.\nTHUR: Python Essentials - Introduction to Variables and Type, Lists and Dicts.\nFRI: Continuation of Python Essentials - Loops, Functions and List Comprehension."),
    ("Week 22", "24th August – 28th August 2026", "MON: Continuation of NumPy - Focus on Array Creation, Math, Reshape, Indexing, Broadcasting.\nTUE: Pandas - Working with Tabular Data.\nWED: Continuation on Pandas, Load CSV, Inspect, Select.\nTHUR: Worked on Matplotlib and Seaborn - Visualising Datas.\nFRI: Worked on Matplotlib and Seaborn with interest on Bar chart, Line chart, Scatter plots & Heat map."),
    ("Week 23", "31st August – 4th September 2026", "MON: Worked on Jupyter Notebook and its Overview.\nTUE: Continuation on Jupyter, Focusing on the Two Cell Types (Code Cells and Markdown Cells).\nWED: Presentation by I-T Students.\nTHUR: Hands-on Lab - Exploring a Real Dataset.\nFRI: Exercise on How to Troubleshoot Common Issues on Python ML."),
    ("Week 24", "7th September – 11th September 2026", "MON: Selection of a Research Topic.\nTUE: Deep Research on Project Topic using Google Scholars.\nWED: First Review by Company Supervisor and Corrections.\nTHUR: Short Presentation on Focused Topics.\nFRI: Final Assessment on the Project and General Overview.")
]

for wk, date, desc in logbook_data:
    row_cells = table.add_row().cells
    row_cells[0].text = wk
    row_cells[1].text = date
    row_cells[2].text = desc

doc.add_page_break()

add_heading(doc, 'APPENDIX B: CORE SATELLITE EXTRACTION PIPELINE SOURCE CODE', level=2)
code_text = """
import os
import requests
import planetary_computer as pc
import numpy as np
import geopandas as gpd
import rioxarray

uyo_wgs84 = gpd.read_file("data/vectors/uyo_boundary.geojson")

def load_signed_band(assets_dict, keys):
    matched_key = next((k for k in keys if k in assets_dict), None)
    raw_href = assets_dict[matched_key]["href"]
    signed_href = pc.sign_url(raw_href)
    with rioxarray.open_rasterio(signed_href, masked=True) as src:
        geom = uyo_wgs84.to_crs(src.rio.crs).geometry
        return src.rio.clip(geom, all_touched=True).squeeze()

def process_landsat_epoch(item_json, epoch_year):
    assets = item_json["assets"]
    red   = load_signed_band(assets, ["red", "SR_B4"])
    green = load_signed_band(assets, ["green", "SR_B3"])
    nir   = load_signed_band(assets, ["nir08", "SR_B5"])
    swir  = load_signed_band(assets, ["swir16", "SR_B6"])
    st    = load_signed_band(assets, ["lwir11", "st_b10", "ST_B10"])
    qa    = load_signed_band(assets, ["qa_pixel", "QA_PIXEL"])
    
    qa_val = np.nan_to_num(qa.values).astype(np.uint16)
    cloud_mask = (
        ((qa_val & (1 << 0)) != 0) | ((qa_val & (1 << 1)) != 0) | 
        ((qa_val & (1 << 3)) != 0) | ((qa_val & (1 << 4)) != 0)
    )
    
    red_s   = (red * 0.0000275 - 0.2).where(~cloud_mask)
    green_s = (green * 0.0000275 - 0.2).where(~cloud_mask)
    nir_s   = (nir * 0.0000275 - 0.2).where(~cloud_mask)
    swir_s  = (swir * 0.0000275 - 0.2).where(~cloud_mask)
    
    lst_s = ((st * 0.00341802 + 149.0) - 273.15).where(~cloud_mask)
    
    ndvi_s  = ((nir_s - red_s) / (nir_s + red_s)).clip(-1.0, 1.0)
    ndbi_s  = ((swir_s - nir_s) / (swir_s + nir_s)).clip(-1.0, 1.0)
    mndwi_s = ((green_s - swir_s) / (green_s + swir_s)).clip(-1.0, 1.0)
    
    return lst_s, ndvi_s, ndbi_s, mndwi_s
"""
p_code = doc.add_paragraph(code_text)
p_code.style = 'No Spacing'
p_code.runs[0].font.name = 'Courier New'
p_code.runs[0].font.size = Pt(10)
doc.add_page_break()

add_heading(doc, 'APPENDIX C: WEB APPLICATION DEPLOYMENT SPECIFICATIONS', level=2)
add_para(doc, "• Public Web Application URL: https://uyouhi-iayygetbmnholngdvqjmdv.streamlit.app/")
add_para(doc, "• GitHub Source Code Repository: https://github.com/blossomsplendour-cpu/uyo_uhi")
add_para(doc, "• Deployment Platform: Streamlit Community Cloud (Linux container environment)")
add_para(doc, "• Application Runtime: Python 3.11 / 3.12")
add_para(doc, "• User Interface (UI) Library: Streamlit, Plotly Express")

output_path = "Detailed_SIWES_IT_Report_ASTAL.docx"
doc.save(output_path)
print(f"✅ SUCCESS! 30-Page Word Document created: {output_path}")