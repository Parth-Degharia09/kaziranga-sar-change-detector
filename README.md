# Kaziranga SAR Change Detector 🛰️🌊

**All-weather flood inundation and ecosystem change detection for Kaziranga National Park, Assam, using Synthetic Aperture Radar (SAR).**

Built for the **NASA Space Apps Challenge: Dancing with the SARs**.

---

## 🎯 The Problem
Every monsoon, severe flooding across the Brahmaputra floodplain submerges large portions of **Kaziranga National Park**, threatening critical wildlife habitats, highland shelters, and surrounding communities. Traditional optical satellites are rendered blind by dense monsoon cloud cover right when real-time situational awareness is needed most.

## 💡 The Solution
**Kaziranga SAR Change Detector** leverages microwave Synthetic Aperture Radar (SAR) data to pierce through storm clouds and darkness. By comparing pre-monsoon baseline backscatter against peak-monsoon radar imagery, the application isolates open floodwater, highlights submerged zones, and visualizes terrain shifts interactively.

---

## 🛠️ Tech Stack & Architecture

* **Data Processing (`Python`):**
  * `earthaccess` / `asf_search` — Automated querying and retrieval of SAR granules over Assam.
  * `rasterio` & `numpy` — Radiometric calibration ($\text{dB}$ backscatter conversion), speckle filtering, and pre/post-event change detection math.
  * `geopandas` & `rio-cogeo` — Exporting web-optimized GeoJSON flood masks and Cloud Optimized GeoTIFFs (COGs).
* **Interactive Frontend (`React`):**
  * `react-leaflet` — Geospatial visualization of flood extents and park boundaries.
  * `react-compare-slider` — Interactive before-and-after swipe comparison between dry and flooded radar states.

---

## 📂 Repository Structure

```text
kaziranga-sar-change-detector/
├── processing/              # Python SAR preprocessing & change detection pipeline
│   ├── requirements.txt
│   ├── download_sar.py
│   └── process_flood.py
├── frontend/                # React interactive web dashboard
│   ├── public/              # Processed GeoJSON masks & raster overlays
│   └── src/
└── README.md
