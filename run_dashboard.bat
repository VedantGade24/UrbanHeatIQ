@echo off
title UrbanHeatIQ Dashboard Launcher
echo ==============================================================================
echo Launching UrbanHeatIQ Interactive Climate Resilience & UHI Dashboard...
echo ==============================================================================
start "" "%~dp0dashboard\index.html"
echo Dashboard launched in your default web browser!
timeout /t 3 >nul
exit
