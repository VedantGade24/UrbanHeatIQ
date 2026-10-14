/**
 * UrbanHeatIQ - Interactive Application Logic & Data Visualization Engine
 */

let mapInstance = null;
let mapMarkersGroup = null;
let currentLayer = 'temp'; // 'temp', 'ndvi', 'hvi'

let regressionChart = null;
let dualAxisChart = null;
let justiceChart = null;

let filteredZones = [...ZONES_DATA];

// --------------------------------------------------------------------------
// Initialization
// --------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    initRegressionChart();
    initDualAxisChart();
    initJusticeChart();
    populateTable(filteredZones);
    updateKPIs(filteredZones);
});

// --------------------------------------------------------------------------
// 1. Leaflet Interactive Map
// --------------------------------------------------------------------------
function initMap() {
    const defaultLat = 39.98;
    const defaultLng = -75.16;

    mapInstance = L.map('leaflet-map').setView([defaultLat, defaultLng], 12);

    // 1. ESRI Clean Street Map (Default - 100% Free, No API key, No watermark, No 403 blocks)
    const esriStreet = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; Street Map',
        maxZoom: 18
    }).addTo(mapInstance);

    // 2. ESRI High-Resolution Satellite Imagery (NASA / USGS)
    const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; NASA, USGS, Earthstar Geographics',
        maxZoom: 18
    });

    // 3. ESRI Minimalist Gray Canvas (Base + Labels)
    const esriGray = L.layerGroup([
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Light Canvas',
            maxZoom: 16
        }),
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 16
        })
    ]);

    const baseMaps = {
        "🏙️ Clean City Streets": esriStreet,
        "🛰️ NASA / ESRI Satellite": esriSatellite,
        "🗺️ Minimalist Canvas": esriGray
    };

    L.control.layers(baseMaps, null, { position: 'topright' }).addTo(mapInstance);

    mapMarkersGroup = L.layerGroup().addTo(mapInstance);
    renderMapMarkers();
}

function renderMapMarkers() {
    mapMarkersGroup.clearLayers();

    filteredZones.forEach(zone => {
        let color = '#2ca02c';
        let radius = 10;
        let metricDisplay = '';

        if (currentLayer === 'temp') {
            if (zone.surface_temp_c < 30.0) color = '#10b981';
            else if (zone.surface_temp_c < 34.0) color = '#3b82f6';
            else if (zone.surface_temp_c < 38.0) color = '#f97316';
            else color = '#ef4444';
            radius = 8 + (zone.surface_temp_c - 24) * 0.7;
            metricDisplay = `<b>Surface Temp (LST):</b> <span style="color:${color}; font-weight:800; font-size:14px;">${zone.surface_temp_c}°C</span> (+${zone.uhi_intensity_c}°C UHI)`;
        } else if (currentLayer === 'ndvi') {
            if (zone.ndvi_index > 0.6) color = '#047857';
            else if (zone.ndvi_index > 0.4) color = '#10b981';
            else if (zone.ndvi_index > 0.2) color = '#a7f3d0';
            else color = '#fed7aa';
            radius = 7 + zone.ndvi_index * 15;
            metricDisplay = `<b>Satellite NDVI:</b> <span style="color:${color}; font-weight:800; font-size:14px;">${zone.ndvi_index}</span> | Canopy: ${zone.tree_canopy_pct}%`;
        } else if (currentLayer === 'hvi') {
            if (zone.heat_vulnerability_score >= 4.0) color = '#dc2626';
            else if (zone.heat_vulnerability_score >= 3.0) color = '#ea580c';
            else if (zone.heat_vulnerability_score >= 2.0) color = '#2563eb';
            else color = '#16a34a';
            radius = 6 + zone.heat_vulnerability_score * 3.5;
            metricDisplay = `<b>HVI Risk Score:</b> <span style="color:${color}; font-weight:800; font-size:14px;">${zone.heat_vulnerability_score} / 5.0</span> (${zone.vulnerability_tier})`;
        }

        const popupHtml = `
            <div style="font-family: Plus Jakarta Sans, Arial; font-size: 12.5px; width: 230px; line-height: 1.5;">
                <div style="font-weight: 800; font-size: 14px; margin-bottom: 4px; border-bottom: 2px solid ${color}; padding-bottom: 3px;">
                    ${zone.zone_name}
                </div>
                <div><b>Typology:</b> ${zone.zone_type}</div>
                <div style="margin: 4px 0;">${metricDisplay}</div>
                <div><b>Tree Canopy:</b> ${zone.tree_canopy_pct}% | <b>Impervious:</b> ${zone.impervious_surface_pct}%</div>
                <hr style="margin: 6px 0; border: 0; border-top: 1px solid #e2e8f0;">
                <div><b>Median Income:</b> $${zone.median_income_usd.toLocaleString()}</div>
                <div><b>Poverty Rate:</b> ${zone.poverty_rate_pct}% | <b>Elderly:</b> ${zone.elderly_pop_pct}%</div>
                <div><b>Heat Hospitalizations:</b> <b>${zone.heat_hospitalizations_per_10k}</b> per 10k</div>
            </div>
        `;

        const marker = L.circleMarker([zone.latitude, zone.longitude], {
            radius: radius,
            color: color,
            fillColor: color,
            fillOpacity: 0.8,
            weight: 1.5
        }).bindPopup(popupHtml);

        marker.bindTooltip(`${zone.zone_name}: ${zone.surface_temp_c}°C`, { direction: 'top' });
        mapMarkersGroup.addLayer(marker);
    });
}

function toggleMapLayer(layerType) {
    currentLayer = layerType;
    document.querySelectorAll('.btn-toggle').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-layer-${layerType}`).classList.add('active');
    renderMapMarkers();
}

// --------------------------------------------------------------------------
// 2. Chart.js: Canopy vs. Temperature Regression
// --------------------------------------------------------------------------
function initRegressionChart() {
    const ctx = document.getElementById('regressionChart').getContext('2d');

    // Prepare scatter data
    const scatterData = ZONES_DATA.map(z => ({
        x: z.tree_canopy_pct,
        y: z.surface_temp_c,
        name: z.zone_name,
        type: z.zone_type
    }));

    // Generate OLS Regression Line (T = 38.4 - 0.26 * Canopy)
    const lineData = [
        { x: 2, y: 38.4 - 0.26 * 2 },
        { x: 70, y: 38.4 - 0.26 * 70 }
    ];

    regressionChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Urban Neighborhood Zones',
                    data: scatterData,
                    backgroundColor: 'rgba(37, 99, 235, 0.75)',
                    borderColor: '#1d4ed8',
                    borderWidth: 1,
                    pointRadius: 6,
                    pointHoverRadius: 9
                },
                {
                    label: 'OLS Linear Regression Fit (R² = 0.71)',
                    data: lineData,
                    type: 'line',
                    borderColor: '#ef4444',
                    borderWidth: 2.5,
                    borderDash: [6, 4],
                    pointRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const raw = ctx.raw;
                            if (raw.name) {
                                return `${raw.name} (${raw.type}): ${raw.x}% Canopy, ${raw.y}°C Temp`;
                            }
                            return `Regression: ${raw.y.toFixed(1)}°C`;
                        }
                    }
                },
                legend: {
                    position: 'top',
                    labels: { font: { family: 'Plus Jakarta Sans', size: 12, weight: 600 } }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Tree Canopy Coverage (% of Total Land Area)', font: { weight: 'bold', size: 12 } },
                    min: 0,
                    max: 75
                },
                y: {
                    title: { display: true, text: 'Average Land Surface Temperature (°C)', font: { weight: 'bold', size: 12 } },
                    min: 22,
                    max: 44
                }
            }
        }
    });
}

// --------------------------------------------------------------------------
// 3. Chart.js: Dual-Axis Grid Load vs. Extreme Heat Days
// --------------------------------------------------------------------------
function initDualAxisChart() {
    const ctx = document.getElementById('dualAxisChart').getContext('2d');

    const years = TIMESERIES_DATA.map(d => d.year);
    const gridLoad = TIMESERIES_DATA.map(d => d.summer_peak_grid_load_mw);
    const heatDays = TIMESERIES_DATA.map(d => d.extreme_heat_days_count);

    dualAxisChart = new Chart(ctx, {
        data: {
            labels: years,
            datasets: [
                {
                    type: 'bar',
                    label: 'Summer Peak Grid Load (MW)',
                    data: gridLoad,
                    backgroundColor: 'rgba(59, 130, 246, 0.75)',
                    borderColor: '#2563eb',
                    borderWidth: 1,
                    borderRadius: 4,
                    yAxisID: 'yGrid',
                    order: 2
                },
                {
                    type: 'line',
                    label: 'Extreme Heat Days (T ≥ 35°C)',
                    data: heatDays,
                    borderColor: '#ef4444',
                    backgroundColor: '#ef4444',
                    borderWidth: 3,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    yAxisID: 'yDays',
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { font: { family: 'Plus Jakarta Sans', size: 12, weight: 600 } }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Observation Year', font: { weight: 'bold' } }
                },
                yGrid: {
                    type: 'linear',
                    position: 'left',
                    title: { display: true, text: 'Peak Electricity Grid Load (Megawatts - MW)', font: { weight: 'bold' }, color: '#2563eb' },
                    min: 6000,
                    max: 10500,
                    ticks: { color: '#2563eb' }
                },
                yDays: {
                    type: 'linear',
                    position: 'right',
                    title: { display: true, text: 'Annual Extreme Heat Days (Days ≥ 35°C)', font: { weight: 'bold' }, color: '#ef4444' },
                    min: 0,
                    max: 50,
                    grid: { drawOnChartArea: false },
                    ticks: { color: '#ef4444' }
                }
            }
        }
    });
}

// --------------------------------------------------------------------------
// 4. Chart.js: Environmental Justice (Income vs. Heat)
// --------------------------------------------------------------------------
function initJusticeChart() {
    const ctx = document.getElementById('justiceChart').getContext('2d');

    const bubbleData = ZONES_DATA.map(z => ({
        x: z.median_income_usd,
        y: z.surface_temp_c,
        r: Math.max(4, z.heat_hospitalizations_per_10k * 0.7),
        name: z.zone_name,
        hosp: z.heat_hospitalizations_per_10k
    }));

    justiceChart = new Chart(ctx, {
        type: 'bubble',
        data: {
            datasets: [{
                label: 'Urban Neighborhoods (Bubble Size = Heat Hospitalizations per 10k)',
                data: bubbleData,
                backgroundColor: 'rgba(239, 68, 68, 0.65)',
                borderColor: '#dc2626',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const raw = ctx.raw;
                            return `${raw.name}: $${raw.x.toLocaleString()} Income | ${raw.y}°C Temp | ${raw.hosp} Hosp/10k`;
                        }
                    }
                },
                legend: { position: 'top', labels: { font: { family: 'Plus Jakarta Sans', weight: 600 } } }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Median Household Income (USD $)', font: { weight: 'bold' } },
                    ticks: { callback: (val) => '$' + val.toLocaleString() }
                },
                y: {
                    title: { display: true, text: 'Land Surface Temperature (°C)', font: { weight: 'bold' } },
                    min: 22,
                    max: 44
                }
            }
        }
    });
}

// --------------------------------------------------------------------------
// 5. Filtering and Interactivity
// --------------------------------------------------------------------------
function applyFilters() {
    const selectedType = document.getElementById('filter-zone-type').value;
    const selectedVuln = document.getElementById('filter-vulnerability').value;
    const maxCanopy = parseFloat(document.getElementById('filter-canopy-slider').value);
    const minTemp = parseFloat(document.getElementById('filter-temp-slider').value);

    filteredZones = ZONES_DATA.filter(z => {
        const matchesType = (selectedType === 'ALL') || (z.zone_type === selectedType);
        const matchesVuln = (selectedVuln === 'ALL') || (z.vulnerability_tier === selectedVuln);
        const matchesCanopy = z.tree_canopy_pct <= maxCanopy;
        const matchesTemp = z.surface_temp_c >= minTemp;
        return matchesType && matchesVuln && matchesCanopy && matchesTemp;
    });

    renderMapMarkers();
    populateTable(filteredZones);
    updateKPIs(filteredZones);
}

function updateCanopySlider(val) {
    document.getElementById('canopy-slider-val').innerText = val + '%';
    applyFilters();
}

function updateTempSlider(val) {
    document.getElementById('temp-slider-val').innerText = val + '°C';
    applyFilters();
}

function resetFilters() {
    document.getElementById('filter-zone-type').value = 'ALL';
    document.getElementById('filter-vulnerability').value = 'ALL';
    document.getElementById('filter-canopy-slider').value = 75;
    document.getElementById('canopy-slider-val').innerText = '75%';
    document.getElementById('filter-temp-slider').value = 24;
    document.getElementById('temp-slider-val').innerText = '24°C';
    applyFilters();
}

function updateKPIs(zones) {
    if (zones.length === 0) {
        document.getElementById('kpi-peak-temp').innerText = 'N/A';
        document.getElementById('kpi-uhi-delta').innerText = 'N/A';
        document.getElementById('kpi-avg-canopy').innerText = 'N/A';
        document.getElementById('kpi-high-risk-count').innerText = '0 Zones';
        return;
    }

    const maxTempZone = zones.reduce((prev, curr) => (prev.surface_temp_c > curr.surface_temp_c) ? prev : curr);
    document.getElementById('kpi-peak-temp').innerText = maxTempZone.surface_temp_c + '°C';
    document.getElementById('kpi-peak-zone').innerText = maxTempZone.zone_name;

    const maxUhi = Math.max(...zones.map(z => z.uhi_intensity_c));
    document.getElementById('kpi-uhi-delta').innerText = '+' + maxUhi.toFixed(1) + '°C';

    const avgCanopy = zones.reduce((acc, z) => acc + z.tree_canopy_pct, 0) / zones.length;
    document.getElementById('kpi-avg-canopy').innerText = avgCanopy.toFixed(1) + '%';

    const severeCount = zones.filter(z => z.vulnerability_tier === 'Severe / Critical' || z.vulnerability_tier === 'High Vulnerability').length;
    document.getElementById('kpi-high-risk-count').innerText = `${severeCount} Zones`;
}

// --------------------------------------------------------------------------
// 6. Table Population & Search
// --------------------------------------------------------------------------
function populateTable(zones) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';
    document.getElementById('table-filtered-count').innerText = zones.length;

    zones.forEach(z => {
        let badgeClass = 'risk-low';
        if (z.vulnerability_tier === 'Severe / Critical') badgeClass = 'risk-severe';
        else if (z.vulnerability_tier === 'High Vulnerability') badgeClass = 'risk-high';
        else if (z.vulnerability_tier === 'Moderate Vulnerability') badgeClass = 'risk-moderate';

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><b>${z.zone_id}</b></td>
            <td><b>${z.zone_name}</b></td>
            <td>${z.zone_type}</td>
            <td style="font-weight:700; color: #ef4444;">${z.surface_temp_c}°C</td>
            <td>+${z.uhi_intensity_c}°C</td>
            <td>${z.tree_canopy_pct}%</td>
            <td>${z.ndvi_index}</td>
            <td>$${z.median_income_usd.toLocaleString()}</td>
            <td>${z.heat_hospitalizations_per_10k}</td>
            <td><span class="badge-risk ${badgeClass}">${z.vulnerability_tier}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function searchTable(query) {
    const q = query.toLowerCase().trim();
    const rows = filteredZones.filter(z => 
        z.zone_name.toLowerCase().includes(q) || 
        z.zone_type.toLowerCase().includes(q) ||
        z.zone_id.toLowerCase().includes(q)
    );
    populateTable(rows);
}

// --------------------------------------------------------------------------
// 7. Navigation Tabs
// --------------------------------------------------------------------------
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

    event.currentTarget.classList.add('active');
    document.getElementById(tabId).classList.add('active');

    // Trigger map invalidation on tab show so Leaflet tiles align properly
    if (tabId === 'tab-map' && mapInstance) {
        setTimeout(() => mapInstance.invalidateSize(), 150);
    }
}

// --------------------------------------------------------------------------
// 8. CSV Export
// --------------------------------------------------------------------------
function exportFilteredData() {
    if (filteredZones.length === 0) {
        alert('No data to export under current filters.');
        return;
    }
    const headers = Object.keys(filteredZones[0]);
    const csvRows = [headers.join(',')];

    filteredZones.forEach(z => {
        const values = headers.map(h => `"${z[h]}"`);
        csvRows.push(values.join(','));
    });

    const csvBlob = new Blob([csvRows.join('\n')], { type: 'text/csv' });
    const url = window.URL.createObjectURL(csvBlob);
    const a = document.createElement('a');
    a.setAttribute('href', url);
    a.setAttribute('download', 'uhi_filtered_neighborhoods.csv');
    a.click();
}
