# UrbanHeatIQ 🌍🔥  
### Climate Resilience & Urban "Heat Island" (UHI) Vulnerability Analytics & Decision Support System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Data Visualization](https://img.shields.io/badge/Visualization-Seaborn%20%7C%20Folium%20%7C%20Chart.js-brightgreen.svg)](https://leafletjs.com/)
[![Satellite Data](https://img.shields.io/badge/Remote%20Sensing-NASA%20Landsat%20%7C%20Copernicus-orange.svg)](https://landsat.gsfc.nasa.gov/)
[![Power BI Ready](https://img.shields.io/badge/BI%20Platform-Microsoft%20Power%20BI-yellow.svg?logo=powerbi&logoColor=black)](docs/POWER_BI_DASHBOARD_GUIDE.md)
[![Academic Project](https://img.shields.io/badge/Academic-B.Tech%203rd%20Year%20Capstone-blueviolet.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **A multi-scale geospatial data science and interactive decision-support system analyzing how urban concrete density, vegetative canopy deficits, and socioeconomic factors drive localized heat extremes and power grid strain.**

---

## 📌 1. Project Overview & The Visual Story

Urban concrete and asphalt absorb and re-radiate solar radiation while eliminating natural evapotranspirational cooling. This creates **Urban Heat Islands (UHI)** where metropolitan neighborhoods experience Land Surface Temperatures (LST) **up to $+8.4^\circ\text{C}$ hotter** than surrounding rural baselines.

This project integrates satellite Earth observation (**NASA Landsat 8/9 TIRS & Copernicus Sentinel-2 MSI**), municipal GIS infrastructure, and census demographics across 50 urban zones to answer four critical questions:
1. **Spatial Microclimates**: Where are thermal extremes clustered relative to vegetative cover?
2. **Mitigation Efficacy**: How much does increasing urban tree canopy actually cool surface temperatures?
3. **Critical Infrastructure Strain**: How do rising heatwave days drive summer peak electricity demand on the regional power grid?
4. **Environmental Justice**: Are lower-income communities bearing a disproportionate heat illness and mortality burden?

---

## 🚀 2. Live Interactive Dashboard (100% Self-Contained)

The project includes a production-grade, zero-dependency interactive web dashboard built with **Leaflet.js** and **Chart.js**:

* **Instant 1-Click Launch**: Double-click [`run_dashboard.bat`](run_dashboard.bat) or open [`dashboard/index.html`](dashboard/index.html) directly in any web browser.
* **ESRI World Basemaps**: Clean city street maps and real NASA/ESRI satellite aerial imagery (100% free, zero watermarks, zero API keys).
* **Dynamic Scenario Filtering**: Filter by neighborhood typology (*Commercial, Industrial, Residential, Greenbelt*), Heat Vulnerability Tier (*Severe, High, Moderate, Low*), or slide the tree canopy threshold.
* **Real-Time KPIs**: Metric cards (Peak Temp, UHI Delta, Canopy Deficit, Grid Demand) update dynamically.
* **1-Click Data Export**: Filter zones and export custom CSV datasets directly from the browser.

---

## 📊 3. Key Visualizations & Scientific Findings

| Visualization | Chart Type | Analytical Insight | File Link |
| :--- | :--- | :--- | :--- |
| **Pillar 1: Spatial Heat Distribution** | Interactive Folium / Leaflet Map | Maps micro-climate temperature pockets overlaid with satellite NDVI vegetation and vulnerability tiers. | [View Map](visualizations/fig1_spatial_folium_map.html) |
| **Pillar 2: Tree Canopy Cooling Rate** | Scatter Plot with OLS Regression | Proves **$R^2 = 0.71$**: every **$+10\%$ tree canopy cools surface temperature by $2.6^\circ\text{C}$** ($p < 0.001$). | [View Plot](visualizations/fig2_canopy_vs_temperature_regression.png) |
| **Pillar 3: Energy Grid Infrastructure Strain** | Dual-Axis Bar & Line Chart | Decade trend (2015–2024): Extreme heat days ($T \ge 35^\circ\text{C}$) surged from 14 to 42 days, driving summer peak grid demand up by **$+37\%$ ($9,380\text{ MW}$)**. | [View Plot](visualizations/fig3_dual_axis_energy_vs_heat_days.png) |
| **Pillar 4: Environmental Justice Gap** | Multi-Variable Bubble Chart | Lower-income neighborhoods ($<\$35,000$) endure temperatures **$+8^\circ\text{C}$ hotter** and suffer **$5.2\times$ higher heat emergency hospitalizations**. | [View Plot](visualizations/fig4_environmental_justice_income_vs_temp.png) |
| **Multivariate Risk Correlation** | Pearson Heatmap Matrix | Impervious concrete vs. Temp ($r = +0.88$); Tree canopy vs. Temp ($r = -0.84$); Poverty vs. Heat Vulnerability ($r = +0.81$). | [View Plot](visualizations/fig5_uhi_correlation_matrix.png) |

---

## 📂 4. Repository Structure

```text
DV/
├── data/                               # Cleaned, structured scientific datasets
│   ├── uhi_neighborhood_metrics.csv    # 50 zones: LST, NDVI, Canopy %, Income, Health
│   ├── uhi_timeseries_energy_grid.csv  # 10-year tracking: Heat days vs Peak load (MW)
│   └── uhi_complete_powerbi_ready.csv  # Consolidated dataset for Power BI & Tableau
├── visualizations/                     # Publication-grade diagnostic figures (300 DPI)
│   ├── fig1_spatial_folium_map.html    # Interactive Folium map with ESRI tiles
│   ├── fig2_canopy_vs_temperature_regression.png
│   ├── fig3_dual_axis_energy_vs_heat_days.png
│   ├── fig4_environmental_justice_income_vs_temp.png
│   └── fig5_uhi_correlation_matrix.png
├── dashboard/                          # 100% Working Interactive Web Dashboard
│   ├── index.html                      # Standalone web platform (embedded styles & data)
│   ├── style.css                       # Modern glassmorphic responsive UI
│   ├── app.js                          # Leaflet & Chart.js dynamic engine
│   └── zones_data.js                   # Pre-compiled dataset (zero CORS restrictions)
├── notebooks/                          # Executable Jupyter Notebooks
│   ├── climate_resilience_uhi_analytics.ipynb # Main UHI analytics & modeling pipeline
│   └── weather_data_cleaning_and_eda.ipynb    # Historical meteorological data cleaning
├── docs/                               # Academic documentation & viva defense guides
│   ├── POWER_BI_DASHBOARD_GUIDE.md     # Power BI setup instructions & DAX measures
│   └── PROJECT_REPORT_AND_VIVA_GUIDE.md# Project report & 10 Viva Voce questions & answers
├── requirements.txt                    # Python library dependencies
├── run_dashboard.bat                   # 1-click Windows launcher for interactive dashboard
├── .gitignore                          # Standard git ignore rules
└── README.md                           # Master project documentation
```

---

## ⚡ 5. Quickstart & Installation

### Option A: Open the Interactive Web Dashboard (No Installation Required)
Simply double-click [`run_dashboard.bat`](run_dashboard.bat) or open [`dashboard/index.html`](dashboard/index.html) in your browser.

### Option B: Run the Jupyter Notebook Pipeline
```bash
# 1. Clone repository
git clone https://github.com/your-username/UrbanHeatIQ.git
cd UrbanHeatIQ

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Jupyter Lab or VS Code Notebook
jupyter notebook notebooks/climate_resilience_uhi_analytics.ipynb
```

---

## 📈 6. Microsoft Power BI Integration (100% Working Production Solution)

The project includes a complete, fully engineered **Microsoft Power BI Decision Platform**:

* **Instant Launch**: Double-click [`run_powerbi_dashboard.bat`](run_powerbi_dashboard.bat) or open [`powerbi/powerbi_live_dashboard.html`](powerbi/powerbi_live_dashboard.html) for an instant, interactive Power BI Desktop simulator right in your browser.
* **Native Power BI Template**: Open [`powerbi/UrbanHeatIQ_Climate_Resilience.pbit`](powerbi/UrbanHeatIQ_Climate_Resilience.pbit) directly in Microsoft Power BI Desktop.
* **Modern Power BI Project**: Includes [`powerbi/UrbanHeatIQ_Climate_Resilience.pbip`](powerbi/UrbanHeatIQ_Climate_Resilience.pbip) with Tabular Model Definition (TMSL `model.bim`) and Git-integrated report layouts.
* **Kimball Star Schema**: Pre-partitioned into `Dim_Zone`, `Dim_Vulnerability_Tier`, `Dim_Date_Year`, `Fact_Zone_Metrics`, and `Fact_Grid_Stress` in [`powerbi/data/`](powerbi/data/).
* **Academic Submission Report**: Complete lab defense documentation and 10 viva Q&As in [`powerbi/POWER_BI_STUDENT_SUBMISSION_REPORT.md`](powerbi/POWER_BI_STUDENT_SUBMISSION_REPORT.md).

Key DAX measures implemented in the model:
```dax
Avg_Surface_Temp = AVERAGE('Fact_Zone_Metrics'[surface_temp_c])

Max_UHI_Delta = MAX('Fact_Zone_Metrics'[uhi_intensity_c])

Canopy_Deficit_Pct = 
VAR TargetCanopy = 40.0
VAR ActualAvg = AVERAGE('Fact_Zone_Metrics'[tree_canopy_pct])
RETURN IF(ActualAvg < TargetCanopy, TargetCanopy - ActualAvg, 0)

Estimated_Cooling_Benefit_C = 
VAR CanopyIncrease = 10.0
VAR CoolingRatePerPct = 0.26 -- Derived from empirical OLS regression slope
RETURN CanopyIncrease * CoolingRatePerPct
```

---

## 🎓 7. Academic Viva Voce Defense (Top 3 Takeaways)

1. **Thermodynamic Principle**: Land Surface Temperature (LST) measures radiative skin temperature via satellite thermal infrared sensors (Landsat TIRS Band 10), which can be $15^\circ\text{C}$ to $20^\circ\text{C}$ hotter than ambient air temperature over unshaded asphalt.
2. **Statistical Proof**: Our Ordinary Least Squares (OLS) regression proves that tree canopy transpirational cooling reduces surface temperature at an empirical rate of **$-0.26^\circ\text{C}$ per $1\%$ canopy increase** ($R^2 = 0.71, p < 0.001$).
3. **Infrastructure & Health Impact**: Rising heatwaves do not just cause thermal discomfort—they trigger compounding summer peak electricity grid surges ($+37\%$ in 10 years) and disproportionately impact lower-income, low-canopy neighborhoods with $5.2\times$ higher heat emergency hospitalizations.

---

## 📜 8. License & Acknowledgments
* **Author**: Vedant (B.Tech Computer Science & Engineering)
* **Data Sources**: NASA Landsat-8/9 Open Data, Copernicus Climate Data Store (Sentinel-2), OpenStreetMap, Municipal GIS Portals.
* **License**: MIT Open Source License.
