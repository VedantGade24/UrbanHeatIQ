"""
Data Preparation Pipeline for Power BI Star Schema
Author: Vedant (B.Tech CSE - 3rd Year)
Project: UrbanHeatIQ - Climate Resilience & Urban Heat Island Analytics
"""

import os
import pandas as pd
import numpy as np

def build_star_schema():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_data_dir = os.path.join(os.path.dirname(base_dir), 'data')
    out_data_dir = os.path.join(base_dir, 'data')
    os.makedirs(out_data_dir, exist_ok=True)

    # 1. Load Raw Sources
    zones_raw_path = os.path.join(raw_data_dir, 'uhi_complete_powerbi_ready.csv')
    grid_raw_path = os.path.join(raw_data_dir, 'uhi_timeseries_energy_grid.csv')

    df_zones = pd.read_csv(zones_raw_path)
    df_grid = pd.read_csv(grid_raw_path)

    print(f"Loaded {len(df_zones)} zones and {len(df_grid)} time series records.")

    # 2. Derive Geographic Sectors for Spatial Filtering
    def get_sector(row):
        lat, lon = row['latitude'], row['longitude']
        if lat >= 40.0:
            return 'Northeast / Upper City' if lon >= -75.1 else 'Northwest / Wissahickon'
        elif lat <= 39.93:
            return 'South / Port Industrial'
        elif lon <= -75.18:
            return 'West Urban / Cobbs Basin'
        else:
            return 'Central / Downtown Core'

    df_zones['geographic_sector'] = df_zones.apply(get_sector, axis=1)

    # 3. Create Dim_Zone
    dim_zone = df_zones[[
        'zone_id', 'zone_name', 'zone_type', 'geographic_sector', 'latitude', 'longitude'
    ]].copy()
    dim_zone_path = os.path.join(out_data_dir, 'Dim_Zone.csv')
    dim_zone.to_csv(dim_zone_path, index=False)
    print(f"-> Created {dim_zone_path} ({len(dim_zone)} rows)")

    # 4. Create Dim_Vulnerability_Tier
    tier_metadata = [
        {
            'vulnerability_tier': 'Severe / Critical',
            'priority_level': 1,
            'risk_rating': 'Critical Priority',
            'action_protocol': 'Emergency Cool Roof Subsidies, Mobile Mist Stations & Tree Planting',
            'target_canopy_pct': 40.0,
            'color_hex': '#DC2626'
        },
        {
            'vulnerability_tier': 'High Vulnerability',
            'priority_level': 2,
            'risk_rating': 'High Priority',
            'action_protocol': 'Public Cooling Centers, Transit Shade Shelters & Pavement Retrofits',
            'target_canopy_pct': 40.0,
            'color_hex': '#EA580C'
        },
        {
            'vulnerability_tier': 'Moderate Vulnerability',
            'priority_level': 3,
            'risk_rating': 'Moderate Priority',
            'action_protocol': 'Residential Canopy Grants & Urban Green Buffer Maintenance',
            'target_canopy_pct': 40.0,
            'color_hex': '#CA8A04'
        },
        {
            'vulnerability_tier': 'Low Vulnerability',
            'priority_level': 4,
            'risk_rating': 'Low / Resilient',
            'action_protocol': 'Forest Conservation Easements & Riparian Buffer Preservation',
            'target_canopy_pct': 40.0,
            'color_hex': '#16A34A'
        }
    ]
    dim_tier = pd.DataFrame(tier_metadata)
    dim_tier_path = os.path.join(out_data_dir, 'Dim_Vulnerability_Tier.csv')
    dim_tier.to_csv(dim_tier_path, index=False)
    print(f"-> Created {dim_tier_path} ({len(dim_tier)} rows)")

    # 5. Create Dim_Date_Year
    years = sorted(df_grid['year'].unique())
    year_records = []
    for y in years:
        if y <= 2018:
            era = 'Historical Baseline (2015-2018)'
        elif y <= 2021:
            era = 'Accelerating Warming (2019-2021)'
        else:
            era = 'Extreme Heat Surge (2022-2024)'
        year_records.append({
            'year': y,
            'decade': f"{(y // 10) * 10}s",
            'climate_era': era
        })
    dim_year = pd.DataFrame(year_records)
    dim_year_path = os.path.join(out_data_dir, 'Dim_Date_Year.csv')
    dim_year.to_csv(dim_year_path, index=False)
    print(f"-> Created {dim_year_path} ({len(dim_year)} rows)")

    # 6. Create Fact_Zone_Metrics
    fact_zone = df_zones[[
        'zone_id', 'vulnerability_tier', 'surface_temp_c', 'ndvi_index',
        'tree_canopy_pct', 'impervious_surface_pct', 'albedo_coefficient',
        'median_income_usd', 'poverty_rate_pct', 'elderly_pop_pct',
        'ac_penetration_pct', 'heat_hospitalizations_per_10k', 'uhi_intensity_c',
        'heat_vulnerability_score'
    ]].copy()
    fact_zone_path = os.path.join(out_data_dir, 'Fact_Zone_Metrics.csv')
    fact_zone.to_csv(fact_zone_path, index=False)
    print(f"-> Created {fact_zone_path} ({len(fact_zone)} rows)")

    # 7. Create Fact_Grid_Stress
    fact_grid = df_grid.copy()
    fact_grid_path = os.path.join(out_data_dir, 'Fact_Grid_Stress.csv')
    fact_grid.to_csv(fact_grid_path, index=False)
    print(f"-> Created {fact_grid_path} ({len(fact_grid)} rows)")

    # 8. Create Consolidated Master Table
    master = df_zones.copy()
    master_path = os.path.join(out_data_dir, 'UHI_Master_Consolidated.csv')
    master.to_csv(master_path, index=False)
    print(f"-> Created {master_path} ({len(master)} rows)")

    print("\n[SUCCESS] Power BI Star Schema datasets successfully prepared in powerbi/data/!")

if __name__ == '__main__':
    build_star_schema()
