"""
Power BI Solution Builder: UrbanHeatIQ
Generates:
1. Microsoft Power BI Project (.pbip)
2. Semantic Model TMSL definition (model.bim + definition.pbism)
3. Report Layout Definition (report.json + definition.pbir)
4. Power BI Template package (.pbit)
Author: Vedant (B.Tech CSE - 3rd Year)
"""

import os
import json
import zipfile
import shutil

def create_powerbi_solution():
    workspace_root = r"c:\Users\Vedant\OneDrive\Desktop\DV"
    pbi_dir = os.path.join(workspace_root, "powerbi")
    data_dir = os.path.join(pbi_dir, "data").replace("\\", "/")

    # Directory layout
    pbip_file = os.path.join(pbi_dir, "UrbanHeatIQ_Climate_Resilience.pbip")
    semantic_model_dir = os.path.join(pbi_dir, "UrbanHeatIQ_Climate_Resilience.SemanticModel")
    report_dir = os.path.join(pbi_dir, "UrbanHeatIQ_Climate_Resilience.Report")
    pbit_file = os.path.join(pbi_dir, "UrbanHeatIQ_Climate_Resilience.pbit")

    os.makedirs(semantic_model_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)

    # 1. UrbanHeatIQ_Climate_Resilience.pbip
    pbip_payload = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": "UrbanHeatIQ_Climate_Resilience.Report"
                }
            }
        ],
        "settings": {
            "enableAutoAuth": True
        }
    }
    with open(pbip_file, "w", encoding="utf-8") as f:
        json.dump(pbip_payload, f, indent=2)
    print(f"Created: {pbip_file}")

    # 2. SemanticModel definition.pbism
    pbism_payload = {
        "version": "1.0"
    }
    with open(os.path.join(semantic_model_dir, "definition.pbism"), "w", encoding="utf-8") as f:
        json.dump(pbism_payload, f, indent=2)

    # 3. model.bim (TMSL)
    model_bim = {
        "name": "UrbanHeatIQ_SemanticModel",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "tables": [
                {
                    "name": "_Measures",
                    "lineageTag": "tbl-measures-001",
                    "columns": [
                        {
                            "name": "MeasurePlaceholder",
                            "dataType": "string",
                            "isHidden": True,
                            "sourceColumn": "MeasurePlaceholder"
                        }
                    ],
                    "partitions": [
                        {
                            "name": "_Measures-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText(\"i44FAA==\", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [MeasurePlaceholder = _t])",
                                    "in",
                                    "    Source"
                                ]
                            }
                        }
                    ],
                    "measures": [
                        {
                            "name": "Avg_Surface_Temp",
                            "expression": "AVERAGE('Fact_Zone_Metrics'[surface_temp_c])",
                            "formatString": "0.0 °C",
                            "description": "Average Land Surface Temperature across filtered zones"
                        },
                        {
                            "name": "Max_UHI_Delta",
                            "expression": "MAX('Fact_Zone_Metrics'[uhi_intensity_c])",
                            "formatString": "+0.0 °C",
                            "description": "Peak Urban Heat Island temperature anomaly above rural baseline"
                        },
                        {
                            "name": "Min_Surface_Temp",
                            "expression": "MIN('Fact_Zone_Metrics'[surface_temp_c])",
                            "formatString": "0.0 °C"
                        },
                        {
                            "name": "Avg_Canopy_Pct",
                            "expression": "AVERAGE('Fact_Zone_Metrics'[tree_canopy_pct])",
                            "formatString": "0.0\\%",
                            "description": "Mean vegetative tree canopy coverage percentage"
                        },
                        {
                            "name": "Canopy_Deficit_Pct",
                            "expression": "VAR TargetCanopy = 40.0 VAR ActualAvg = [Avg_Canopy_Pct] RETURN IF(ActualAvg < TargetCanopy, TargetCanopy - ActualAvg, 0)",
                            "formatString": "0.0\\%",
                            "description": "Tree canopy deficit relative to municipal 40% climate resilience target"
                        },
                        {
                            "name": "Critical_Zone_Count",
                            "expression": "CALCULATE(COUNTROWS('Fact_Zone_Metrics'), 'Fact_Zone_Metrics'[vulnerability_tier] IN {\"Severe / Critical\", \"High Vulnerability\"})",
                            "formatString": "#,##0",
                            "description": "Count of zones categorized as Severe or High Heat Vulnerability"
                        },
                        {
                            "name": "Critical_Zone_Share_Pct",
                            "expression": "DIVIDE([Critical_Zone_Count], COUNTROWS(ALL('Fact_Zone_Metrics')), 0)",
                            "formatString": "0.0\\%"
                        },
                        {
                            "name": "Estimated_Cooling_Benefit_C",
                            "expression": "VAR CanopyInc = 10.0 RETURN CanopyInc * 0.26",
                            "formatString": "-0.00 °C",
                            "description": "Projected temperature drop from a +10% tree canopy addition based on empirical OLS slope (-0.26 °C per 1% canopy)"
                        },
                        {
                            "name": "Avg_Heat_Hospitalizations",
                            "expression": "AVERAGE('Fact_Zone_Metrics'[heat_hospitalizations_per_10k])",
                            "formatString": "0.0",
                            "description": "Emergency heat illness hospitalizations per 10,000 residents"
                        },
                        {
                            "name": "Avg_Median_Income",
                            "expression": "AVERAGE('Fact_Zone_Metrics'[median_income_usd])",
                            "formatString": "$#,##0",
                            "description": "Median household income across selected zones"
                        },
                        {
                            "name": "Total_Peak_Load_MW",
                            "expression": "SUM('Fact_Grid_Stress'[summer_peak_grid_load_mw])",
                            "formatString": "#,##0 MW"
                        },
                        {
                            "name": "Total_Extreme_Heat_Days",
                            "expression": "SUM('Fact_Grid_Stress'[extreme_heat_days_count])",
                            "formatString": "#,##0 Days"
                        },
                        {
                            "name": "Grid_Load_Growth_Pct",
                            "expression": "VAR Y2015 = CALCULATE(SUM('Fact_Grid_Stress'[summer_peak_grid_load_mw]), 'Dim_Date_Year'[year] = 2015) VAR Y2024 = CALCULATE(SUM('Fact_Grid_Stress'[summer_peak_grid_load_mw]), 'Dim_Date_Year'[year] = 2024) RETURN DIVIDE(Y2024 - Y2015, Y2015, 0)",
                            "formatString": "+0.0\\%",
                            "description": "10-Year growth in summer peak electrical demand (2015 to 2024)"
                        },
                        {
                            "name": "Hospitalization_Disparity_Ratio",
                            "expression": "DIVIDE(CALCULATE(AVERAGE('Fact_Zone_Metrics'[heat_hospitalizations_per_10k]), 'Fact_Zone_Metrics'[vulnerability_tier] = \"Severe / Critical\"), CALCULATE(AVERAGE('Fact_Zone_Metrics'[heat_hospitalizations_per_10k]), 'Fact_Zone_Metrics'[vulnerability_tier] = \"Low Vulnerability\"), 1)",
                            "formatString": "0.0 \"x\"",
                            "description": "Disparity multiplier in emergency heat hospital admissions between Severe and Low vulnerability zones"
                        }
                    ]
                },
                {
                    "name": "Dim_Zone",
                    "lineageTag": "tbl-dim-zone-001",
                    "columns": [
                        { "name": "zone_id", "dataType": "string", "sourceColumn": "zone_id", "isKey": True },
                        { "name": "zone_name", "dataType": "string", "sourceColumn": "zone_name" },
                        { "name": "zone_type", "dataType": "string", "sourceColumn": "zone_type" },
                        { "name": "geographic_sector", "dataType": "string", "sourceColumn": "geographic_sector" },
                        { "name": "latitude", "dataType": "double", "sourceColumn": "latitude", "dataCategory": "Latitude" },
                        { "name": "longitude", "dataType": "double", "sourceColumn": "longitude", "dataCategory": "Longitude" }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Zone-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Csv.Document(File.Contents("{data_dir}/Dim_Zone.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"zone_id", type text}, {"zone_name", type text}, {"zone_type", type text}, {"geographic_sector", type text}, {"latitude", type number}, {"longitude", type number}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Vulnerability_Tier",
                    "lineageTag": "tbl-dim-tier-001",
                    "columns": [
                        { "name": "vulnerability_tier", "dataType": "string", "sourceColumn": "vulnerability_tier", "isKey": True },
                        { "name": "priority_level", "dataType": "int64", "sourceColumn": "priority_level" },
                        { "name": "risk_rating", "dataType": "string", "sourceColumn": "risk_rating" },
                        { "name": "action_protocol", "dataType": "string", "sourceColumn": "action_protocol" },
                        { "name": "target_canopy_pct", "dataType": "double", "sourceColumn": "target_canopy_pct" },
                        { "name": "color_hex", "dataType": "string", "sourceColumn": "color_hex" }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Vulnerability_Tier-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Csv.Document(File.Contents("{data_dir}/Dim_Vulnerability_Tier.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"vulnerability_tier", type text}, {"priority_level", Int64.Type}, {"risk_rating", type text}, {"action_protocol", type text}, {"target_canopy_pct", type number}, {"color_hex", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Dim_Date_Year",
                    "lineageTag": "tbl-dim-year-001",
                    "columns": [
                        { "name": "year", "dataType": "int64", "sourceColumn": "year", "isKey": True },
                        { "name": "decade", "dataType": "string", "sourceColumn": "decade" },
                        { "name": "climate_era", "dataType": "string", "sourceColumn": "climate_era" }
                    ],
                    "partitions": [
                        {
                            "name": "Dim_Date_Year-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Csv.Document(File.Contents("{data_dir}/Dim_Date_Year.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"year", Int64.Type}, {"decade", type text}, {"climate_era", type text}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Zone_Metrics",
                    "lineageTag": "tbl-fact-zone-001",
                    "columns": [
                        { "name": "zone_id", "dataType": "string", "sourceColumn": "zone_id" },
                        { "name": "vulnerability_tier", "dataType": "string", "sourceColumn": "vulnerability_tier" },
                        { "name": "surface_temp_c", "dataType": "double", "sourceColumn": "surface_temp_c" },
                        { "name": "ndvi_index", "dataType": "double", "sourceColumn": "ndvi_index" },
                        { "name": "tree_canopy_pct", "dataType": "double", "sourceColumn": "tree_canopy_pct" },
                        { "name": "impervious_surface_pct", "dataType": "double", "sourceColumn": "impervious_surface_pct" },
                        { "name": "albedo_coefficient", "dataType": "double", "sourceColumn": "albedo_coefficient" },
                        { "name": "median_income_usd", "dataType": "double", "sourceColumn": "median_income_usd" },
                        { "name": "poverty_rate_pct", "dataType": "double", "sourceColumn": "poverty_rate_pct" },
                        { "name": "elderly_pop_pct", "dataType": "double", "sourceColumn": "elderly_pop_pct" },
                        { "name": "ac_penetration_pct", "dataType": "double", "sourceColumn": "ac_penetration_pct" },
                        { "name": "heat_hospitalizations_per_10k", "dataType": "double", "sourceColumn": "heat_hospitalizations_per_10k" },
                        { "name": "uhi_intensity_c", "dataType": "double", "sourceColumn": "uhi_intensity_c" },
                        { "name": "heat_vulnerability_score", "dataType": "double", "sourceColumn": "heat_vulnerability_score" }
                    ],
                    "partitions": [
                        {
                            "name": "Fact_Zone_Metrics-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Csv.Document(File.Contents("{data_dir}/Fact_Zone_Metrics.csv"), [Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"zone_id", type text}, {"vulnerability_tier", type text}, {"surface_temp_c", type number}, {"ndvi_index", type number}, {"tree_canopy_pct", type number}, {"impervious_surface_pct", type number}, {"albedo_coefficient", type number}, {"median_income_usd", type number}, {"poverty_rate_pct", type number}, {"elderly_pop_pct", type number}, {"ac_penetration_pct", type number}, {"heat_hospitalizations_per_10k", type number}, {"uhi_intensity_c", type number}, {"heat_vulnerability_score", type number}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Fact_Grid_Stress",
                    "lineageTag": "tbl-fact-grid-001",
                    "columns": [
                        { "name": "year", "dataType": "int64", "sourceColumn": "year" },
                        { "name": "extreme_heat_days_count", "dataType": "int64", "sourceColumn": "extreme_heat_days_count" },
                        { "name": "summer_peak_grid_load_mw", "dataType": "int64", "sourceColumn": "summer_peak_grid_load_mw" },
                        { "name": "cooling_degree_days_cdd", "dataType": "int64", "sourceColumn": "cooling_degree_days_cdd" },
                        { "name": "heatwave_events_count", "dataType": "int64", "sourceColumn": "heatwave_events_count" },
                        { "name": "grid_stress_alert_events", "dataType": "int64", "sourceColumn": "grid_stress_alert_events" },
                        { "name": "total_heat_emergency_admissions", "dataType": "int64", "sourceColumn": "total_heat_emergency_admissions" }
                    ],
                    "partitions": [
                        {
                            "name": "Fact_Grid_Stress-Partition",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    f'    Source = Csv.Document(File.Contents("{data_dir}/Fact_Grid_Stress.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
                                    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"year", Int64.Type}, {"extreme_heat_days_count", Int64.Type}, {"summer_peak_grid_load_mw", Int64.Type}, {"cooling_degree_days_cdd", Int64.Type}, {"heatwave_events_count", Int64.Type}, {"grid_stress_alert_events", Int64.Type}, {"total_heat_emergency_admissions", Int64.Type}})',
                                    "in",
                                    '    #"Changed Type"'
                                ]
                            }
                        }
                    ]
                }
            ],
            "relationships": [
                {
                    "name": "rel_zone_to_metrics",
                    "fromTable": "Fact_Zone_Metrics",
                    "fromColumn": "zone_id",
                    "toTable": "Dim_Zone",
                    "toColumn": "zone_id",
                    "crossFilteringBehavior": "bothDirections"
                },
                {
                    "name": "rel_tier_to_metrics",
                    "fromTable": "Fact_Zone_Metrics",
                    "fromColumn": "vulnerability_tier",
                    "toTable": "Dim_Vulnerability_Tier",
                    "toColumn": "vulnerability_tier",
                    "crossFilteringBehavior": "bothDirections"
                },
                {
                    "name": "rel_year_to_grid",
                    "fromTable": "Fact_Grid_Stress",
                    "fromColumn": "year",
                    "toTable": "Dim_Date_Year",
                    "toColumn": "year",
                    "crossFilteringBehavior": "bothDirections"
                }
            ]
        }
    }

    with open(os.path.join(semantic_model_dir, "model.bim"), "w", encoding="utf-8") as f:
        json.dump(model_bim, f, indent=2)
    print(f"Created: {os.path.join(semantic_model_dir, 'model.bim')}")

    # 4. Report definition.pbir
    pbir_payload = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": "../UrbanHeatIQ_Climate_Resilience.SemanticModel"
            },
            "byConnection": None
        }
    }
    with open(os.path.join(report_dir, "definition.pbir"), "w", encoding="utf-8") as f:
        json.dump(pbir_payload, f, indent=2)

    # 5. Report report.json (Pages, Visuals, Layouts)
    report_json = {
        "config": json.dumps({
            "version": "5.52",
            "themeCollection": {
                "baseTheme": {
                    "name": "CY24SU02",
                    "version": "5.52",
                    "type": 2
                }
            },
            "activeSectionIndex": 0,
            "defaultDrillFilterOtherVisuals": True
        }),
        "layoutOptimization": 0,
        "sections": [
            {
                "id": "Section_Overview",
                "name": "Executive Climate Overview",
                "displayName": "Executive Climate Overview & Geospatial Heat",
                "width": 1280.0,
                "height": 720.0,
                "ordinal": 0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 1000, "width": 1240.0, "height": 65.0,
                        "config": json.dumps({
                            "name": "header_textbox",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [
                                        {"properties": {"paragraphs": [{"textRuns": [{"value": "UrbanHeatIQ | Urban Heat Island Vulnerability & Climate Resilience Decision System", "textStyle": {"fontFamily": "Segoe UI Semibold", "fontSize": "18pt", "color": "#0F172A"}}, {"value": "\nSatellite Earth Observation (Landsat 8/9 & Sentinel-2) | Star Schema Data Warehouse | B.Tech CSE Capstone", "textStyle": {"fontFamily": "Segoe UI", "fontSize": "9pt", "color": "#64748B"}}]}]}}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 90.0, "z": 1001, "width": 230.0, "height": 100.0,
                        "config": json.dumps({
                            "name": "card_avg_temp",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "_Measures.Avg_Surface_Temp"}]}
                            }
                        })
                    },
                    {
                        "x": 265.0, "y": 90.0, "z": 1002, "width": 230.0, "height": 100.0,
                        "config": json.dumps({
                            "name": "card_max_uhi",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "_Measures.Max_UHI_Delta"}]}
                            }
                        })
                    },
                    {
                        "x": 510.0, "y": 90.0, "z": 1003, "width": 230.0, "height": 100.0,
                        "config": json.dumps({
                            "name": "card_critical_zones",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "_Measures.Critical_Zone_Count"}]}
                            }
                        })
                    },
                    {
                        "x": 755.0, "y": 90.0, "z": 1004, "width": 240.0, "height": 100.0,
                        "config": json.dumps({
                            "name": "card_canopy_deficit",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "_Measures.Canopy_Deficit_Pct"}]}
                            }
                        })
                    },
                    {
                        "x": 1010.0, "y": 90.0, "z": 1005, "width": 250.0, "height": 100.0,
                        "config": json.dumps({
                            "name": "card_cooling_benefit",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "_Measures.Estimated_Cooling_Benefit_C"}]}
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 205.0, "z": 1006, "width": 730.0, "height": 495.0,
                        "config": json.dumps({
                            "name": "map_geospatial_zones",
                            "singleVisual": {
                                "visualType": "map",
                                "projections": {
                                    "Latitude": [{"queryRef": "Dim_Zone.latitude"}],
                                    "Longitude": [{"queryRef": "Dim_Zone.longitude"}],
                                    "Size": [{"queryRef": "Fact_Zone_Metrics.surface_temp_c"}],
                                    "Legend": [{"queryRef": "Dim_Vulnerability_Tier.vulnerability_tier"}],
                                    "Tooltips": [
                                        {"queryRef": "Dim_Zone.zone_name"},
                                        {"queryRef": "Dim_Zone.zone_type"},
                                        {"queryRef": "Fact_Zone_Metrics.tree_canopy_pct"},
                                        {"queryRef": "Fact_Zone_Metrics.heat_hospitalizations_per_10k"}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 765.0, "y": 205.0, "z": 1007, "width": 495.0, "height": 240.0,
                        "config": json.dumps({
                            "name": "bar_typology_temperatures",
                            "singleVisual": {
                                "visualType": "barChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Zone.zone_type"}],
                                    "Y": [{"queryRef": "_Measures.Avg_Surface_Temp"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 765.0, "y": 460.0, "z": 1008, "width": 495.0, "height": 240.0,
                        "config": json.dumps({
                            "name": "donut_vulnerability_breakdown",
                            "singleVisual": {
                                "visualType": "pieChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Vulnerability_Tier.vulnerability_tier"}],
                                    "Y": [{"queryRef": "Fact_Zone_Metrics.zone_id"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": "Section_Regression_EJ",
                "name": "Biophysical & Environmental Justice",
                "displayName": "Biophysical OLS Cooling & Environmental Justice",
                "width": 1280.0,
                "height": 720.0,
                "ordinal": 1,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 2000, "width": 1240.0, "height": 65.0,
                        "config": json.dumps({
                            "name": "header_ej",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [
                                        {"properties": {"paragraphs": [{"textRuns": [{"value": "Pillar 2 & 4: Tree Canopy Cooling Physics (OLS R²=0.71) & Socioeconomic Vulnerability", "textStyle": {"fontFamily": "Segoe UI Semibold", "fontSize": "17pt", "color": "#0F172A"}}, {"value": "\nEmpirical OLS Cooling Rate: -2.6°C per +10% Canopy | Disproportionate Low-Income Burden", "textStyle": {"fontFamily": "Segoe UI", "fontSize": "9pt", "color": "#64748B"}}]}]}}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 90.0, "z": 2001, "width": 610.0, "height": 610.0,
                        "config": json.dumps({
                            "name": "scatter_canopy_temp",
                            "singleVisual": {
                                "visualType": "scatterChart",
                                "projections": {
                                    "X": [{"queryRef": "Fact_Zone_Metrics.tree_canopy_pct"}],
                                    "Y": [{"queryRef": "Fact_Zone_Metrics.surface_temp_c"}],
                                    "Details": [{"queryRef": "Dim_Zone.zone_name"}],
                                    "Legend": [{"queryRef": "Dim_Vulnerability_Tier.vulnerability_tier"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 645.0, "y": 90.0, "z": 2002, "width": 615.0, "height": 610.0,
                        "config": json.dumps({
                            "name": "scatter_income_temp",
                            "singleVisual": {
                                "visualType": "scatterChart",
                                "projections": {
                                    "X": [{"queryRef": "Fact_Zone_Metrics.median_income_usd"}],
                                    "Y": [{"queryRef": "Fact_Zone_Metrics.surface_temp_c"}],
                                    "Size": [{"queryRef": "Fact_Zone_Metrics.heat_hospitalizations_per_10k"}],
                                    "Details": [{"queryRef": "Dim_Zone.zone_name"}],
                                    "Legend": [{"queryRef": "Dim_Vulnerability_Tier.vulnerability_tier"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": "Section_Grid_Stress",
                "name": "Energy Grid Infrastructure",
                "displayName": "Municipal Power Grid Strain & Heatwave Trends",
                "width": 1280.0,
                "height": 720.0,
                "ordinal": 2,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 3000, "width": 1240.0, "height": 65.0,
                        "config": json.dumps({
                            "name": "header_grid",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [
                                        {"properties": {"paragraphs": [{"textRuns": [{"value": "Pillar 3: 10-Year Municipal Grid Strain (2015–2024) vs Extreme Heat Surge", "textStyle": {"fontFamily": "Segoe UI Semibold", "fontSize": "17pt", "color": "#0F172A"}}, {"value": "\nDecade Trend: Summer Peak Electrical Load +37% (6,850 MW to 9,380 MW) as Days ≥35°C Surged from 14 to 42", "textStyle": {"fontFamily": "Segoe UI", "fontSize": "9pt", "color": "#64748B"}}]}]}}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 90.0, "z": 3001, "width": 1240.0, "height": 400.0,
                        "config": json.dumps({
                            "name": "dual_axis_grid_load",
                            "singleVisual": {
                                "visualType": "lineClusteredColumnComboChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Date_Year.year"}],
                                    "Y": [{"queryRef": "Fact_Grid_Stress.summer_peak_grid_load_mw"}],
                                    "Y2": [{"queryRef": "Fact_Grid_Stress.extreme_heat_days_count"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 505.0, "z": 3002, "width": 610.0, "height": 195.0,
                        "config": json.dumps({
                            "name": "table_grid_metrics",
                            "singleVisual": {
                                "visualType": "tableEx",
                                "projections": {
                                    "Values": [
                                        {"queryRef": "Dim_Date_Year.year"},
                                        {"queryRef": "Dim_Date_Year.climate_era"},
                                        {"queryRef": "Fact_Grid_Stress.summer_peak_grid_load_mw"},
                                        {"queryRef": "Fact_Grid_Stress.extreme_heat_days_count"},
                                        {"queryRef": "Fact_Grid_Stress.cooling_degree_days_cdd"},
                                        {"queryRef": "Fact_Grid_Stress.grid_stress_alert_events"}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 645.0, "y": 505.0, "z": 3003, "width": 615.0, "height": 195.0,
                        "config": json.dumps({
                            "name": "line_admissions_trend",
                            "singleVisual": {
                                "visualType": "lineChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Date_Year.year"}],
                                    "Y": [{"queryRef": "Fact_Grid_Stress.total_heat_emergency_admissions"}]
                                }
                            }
                        })
                    }
                ]
            }
        ]
    }
    with open(os.path.join(report_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)
    print(f"Created: {os.path.join(report_dir, 'report.json')}")

    # 6. Generate Power BI Template (.pbit) Package
    # A .pbit is a ZIP package containing:
    # - [Content_Types].xml
    # - Version
    # - DataModelSchema (UTF-16LE TMSL)
    # - Report/Layout (UTF-16LE report layout)
    # - Settings (UTF-16LE)
    content_types_xml = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/Version" ContentType="application/vnd.microsoft.powerbi.version" />
  <Override PartName="/DataModelSchema" ContentType="application/vnd.microsoft.powerbi.datamodelschema+json" />
  <Override PartName="/Report/Layout" ContentType="application/vnd.microsoft.powerbi.reportlayout+json" />
  <Override PartName="/Settings" ContentType="application/vnd.microsoft.powerbi.settings+json" />
</Types>"""

    version_str = "2.128.0.0"
    settings_json = {"version": "1.0", "customVisualAllowlist": []}

    with zipfile.ZipFile(pbit_file, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml.encode('utf-8'))
        zf.writestr("Version", version_str.encode('utf-16le'))
        zf.writestr("Settings", json.dumps(settings_json).encode('utf-16le'))
        zf.writestr("DataModelSchema", json.dumps(model_bim).encode('utf-16le'))
        zf.writestr("Report/Layout", json.dumps(report_json).encode('utf-16le'))

    print(f"Created standalone Power BI Template: {pbit_file} ({os.path.getsize(pbit_file)} bytes)")
    print("\n[SUCCESS] Power BI project (.pbip) and template (.pbit) generated successfully!")

if __name__ == '__main__':
    create_powerbi_solution()
