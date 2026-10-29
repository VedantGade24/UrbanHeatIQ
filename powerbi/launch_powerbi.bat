@echo off
title Launch Power BI Decision System
start "" "%~dp0powerbi_live_dashboard.html"
start "" "%~dp0UrbanHeatIQ_Climate_Resilience.pbit" 2>nul
