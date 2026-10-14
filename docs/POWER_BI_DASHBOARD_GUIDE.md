# Power BI Implementation Guide: Climate Resilience & Urban Heat Island Vulnerability Dashboard

This guide provides step-by-step instructions and production-grade DAX measures to build an interactive **Urban Heat Island & Climate Resilience Decision Support Dashboard** in **Microsoft Power BI Desktop**.

---

## 1. Data Source Files
All Power BI-ready datasets are located in:
* **Primary Table**: [`uhi_project/data/uhi_neighborhood_metrics.csv`](file:///c:/Users/Vedant/OneDrive/Desktop/DV/uhi_project/data/uhi_neighborhood_metrics.csv)
* **Time-Series Table**: [`uhi_project/data/uhi_timeseries_energy_grid.csv`](file:///c:/Users/Vedant/OneDrive/Desktop/DV/uhi_project/data/uhi_timeseries_energy_grid.csv)
* **Consolidated File**: [`uhi_project/data/uhi_complete_powerbi_ready.csv`](file:///c:/Users/Vedant/OneDrive/Desktop/DV/uhi_project/data/uhi_complete_powerbi_ready.csv)

---

## 2. Power BI Data Loading & Data Types

1. Open **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **Text/CSV** $\rightarrow$ Select `uhi_complete_powerbi_ready.csv`.
3. Click **Transform Data** to inspect Power Query Editor:
   * Set `latitude` to Data Category: **Latitude** (Decimal Number).
   * Set `longitude` to Data Category: **Longitude** (Decimal Number).
   * Set `surface_temp_c`, `uhi_intensity_c`, `tree_canopy_pct`, `ndvi_index`, `impervious_surface_pct` to **Decimal Number**.
   * Set `median_income_usd` to **Fixed Decimal Number / Currency ($)**.
   * Set `zone_id`, `zone_name`, `zone_type`, `vulnerability_tier` to **Text**.
4. Click **Close & Apply**.

---

## 3. Essential DAX Measures (Copy & Paste Ready)

In Power BI, click **New Measure** in the Modeling tab and create these key analytical metrics:

### Measure 1: Average Land Surface Temperature (LST)
```dax
Avg_Surface_Temp = 
AVERAGE('uhi_complete_powerbi_ready'[surface_temp_c])
```

### Measure 2: Maximum Urban Heat Island Delta (°C above Rural Baseline)
```dax
Max_UHI_Delta = 
MAX('uhi_complete_powerbi_ready'[uhi_intensity_c])
```

### Measure 3: Average Tree Canopy Deficit (Distance from 40% Target)
```dax
Canopy_Deficit_Pct = 
VAR TargetCanopy = 40.0
VAR ActualAvgCanopy = AVERAGE('uhi_complete_powerbi_ready'[tree_canopy_pct])
RETURN
IF(ActualAvgCanopy < TargetCanopy, TargetCanopy - ActualAvgCanopy, 0)
```

### Measure 4: High & Severe Vulnerability Zone Count
```dax
Critical_Vulnerability_Zones_Count = 
CALCULATE(
    COUNTROWS('uhi_complete_powerbi_ready'),
    'uhi_complete_powerbi_ready'[vulnerability_tier] IN {"Severe / Critical", "High Vulnerability"}
)
```

### Measure 5: Estimated Cooling Benefit from 10% Additional Canopy
```dax
Estimated_Cooling_Benefit_C = 
VAR CanopyIncrease = 10.0
VAR CoolingRatePerPct = 0.26 -- Derived from empirical OLS regression slope
RETURN
CanopyIncrease * CoolingRatePerPct
```

### Measure 6: Total Heat Hospitalization Rate per Metropolitan Cohort
```dax
Avg_Heat_Hospitalizations = 
AVERAGE('uhi_complete_powerbi_ready'[heat_hospitalizations_per_10k])
```

---

## 4. Recommended Power BI Visualizations Layout

### Page 1: Executive Climate Resilience Overview (Canvas 16:9)

| Visual Title | Visual Type in Power BI | Data Fields Assigned | Formatting & Visual Cues |
| :--- | :--- | :--- | :--- |
| **Card 1** | Card (New) | `[Avg_Surface_Temp]` | Label: "Avg Surface Temp (°C)" |
| **Card 2** | Card (New) | `[Max_UHI_Delta]` | Callout color: Red (`#EF4444`) |
| **Card 3** | Card (New) | `[Critical_Vulnerability_Zones_Count]` | Callout color: Orange (`#F97316`) |
| **Card 4** | Card (New) | `[Canopy_Deficit_Pct]` | Callout color: Emerald (`#10B981`) |
| **Visual 1** | **Map / Azure Map** | Location: `latitude`, `longitude`<br>Bubble Size: `surface_temp_c`<br>Color Saturation / Tooltips: `vulnerability_tier`, `zone_name`, `ndvi_index` | Base map: Dark / Gray Canvas.<br>Gradient: Green $\to$ Amber $\to$ Red. |
| **Visual 2** | **Scatter Chart** | X-Axis: `tree_canopy_pct`<br>Y-Axis: `surface_temp_c`<br>Legend: `vulnerability_tier`<br>Size: `heat_hospitalizations_per_10k` | Enable **Trend Line** in Analytics pane ($R^2 \approx 0.71$). |
| **Visual 3** | **Line and Clustered Column Chart** (from `uhi_timeseries_energy_grid.csv`) | X-Axis: `year`<br>Column Y-Axis: `summer_peak_grid_load_mw`<br>Line Y-Axis: `extreme_heat_days_count` | Columns: Deep Blue.<br>Line: Crimson Red with data markers. |
| **Visual 4** | **Scatter / Bubble Chart (Environmental Justice)** | X-Axis: `median_income_usd`<br>Y-Axis: `surface_temp_c`<br>Bubble Size: `poverty_rate_pct` | Add constant line at Income median ($55,000). |
| **Slicers** | Slicer Visuals | Top Left: `zone_type`<br>Top Right: `vulnerability_tier` | Dropdown or Tile style. |

---

## 5. Viva Voce Demo Script for Power BI

When presenting this dashboard to examiners:
1. **Interactive Cross-Filtering**: Click on **"Industrial"** in the `zone_type` slicer. Show how the map instantly filters to the logistics and chemical sectors, with temperatures spiking above $41^\circ\text{C}$ and tree canopy dropping below $5\%$.
2. **Environmental Justice Insight**: Point to the Scatter plot showing low-income rowhouse neighborhoods (median income $<\$35,000$) enduring temperatures $6^\circ\text{C}$ hotter than affluent green enclaves.
3. **Infrastructure Resilience**: Highlight the dual-axis chart demonstrating how extreme heat days directly drive summer peak electricity demand ($9,380\text{ MW}$ in 2024), threatening grid reliability and brownout risks.
