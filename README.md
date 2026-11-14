# Kaziranga Monsoon Water Observatory 🛰️🌊

**Exploring seasonal surface-water dynamics and L-band vegetation backscatter shifts across the Brahmaputra–Kaziranga floodplain using NASA-ISRO NISAR radar.**

Built for the **NASA Space Apps Challenge 2026 — Dancing with the SARs** by **Team The Larpers**.

![Kaziranga Monsoon Water Observatory Dashboard](The_Larpers/docs/screenshot.png)

---

## 🎯 The Problem & Ecological Context

Kaziranga National Park on the south bank of the Brahmaputra River in Assam undergoes dramatic seasonal inundation every monsoon. While seasonal flooding is ecologically vital—replenishing wetlands (*beels*), sustaining alluvial grasslands, and clearing invasive species—extreme inundation forces wildlife southward across National Highway 37 toward the Karbi (Mikir) Hills.

Optical satellites are routinely blocked by dense monsoon cloud cover during peak wet months. **NASA-ISRO NISAR's L-band Synthetic Aperture Radar (SAR)** (~24 cm wavelength) images through clouds and darkness on a 12-day repeat cycle. This observatory transforms 10 multi-temporal dual-polarization (`HHHH` + `HVHV`) NISAR acquisitions into a plain-language, interactive scientific explorer.

> **2026 Ground-Truth Context:** On **21 July 2026**—one day before our highest-water NISAR acquisition—Kaziranga Divisional Forest Officer (DFO) Arun Vignesh reported normal seasonal wetting with only four forest camps inundated and no flood emergency. Accordingly, this tool tracks *surface-water dynamics* across the combined Brahmaputra river and floodplain corridor rather than claiming a park-wide flood disaster.

---

## 💡 Core Questions & Interactive Features

1. **Question 1 — Where is the water? (`Where water is` & `Raw radar view`)**
   - 10-date timeline slider (`Jun 16` – `Oct 14, 2026`, UTC & IST) with a split-screen **Before / After swipe** comparing the October 14 low-water baseline against any selected monsoon date.
   - Plain-language daily headlines paired with a full **Observation Metadata** panel (UTC/IST timestamps, cycle number, polarization, CRID maturity status, and classification cutoff).
2. **Question 2 — How frequently is an area wet? (`How often wet`)**
   - Full-width 10-date inundation frequency map distinguishing **occasionally water-observed (10–30%)**, **frequently water-observed (40–70%)**, and **persistent water signatures (80–100%, 8–10 of 10 passes)**.
3. **Question 3 — How does vegetation radar response change? (`Vegetation radar change`)**
   - Exploratory L-band `HHHH` and `HVHV` change map relative to the October 14 baseline over non-water vegetated land, separating **Increased HH response** (Amber: possible surface-water/vegetation double-bounce interaction) from **Changed HV response** (Violet: possible canopy structure or moisture shift).
4. **Evidence, Sensitivity & Export**
   - Every water-like area measurement includes a **$\pm 2\text{ dB}$ threshold sensitivity range** (`−17.5 dB` to `−13.5 dB`), plus one-click CSV exports for both the selected date and the full 10-date time series.

---

## 📊 Key Findings (Cropped Track 040 / Frame 015 Window: 2,176.13 km²)

| Cycle | Date (UTC) | Local Date (IST) | Total Water-Like Area ($\text{km}^2$) | Extra vs. Oct 14 ($\text{km}^2$) | $\pm 2\text{ dB}$ Sensitivity ($\text{km}^2$) | Mean HHHH ($\text{dB}$) | Mean HVHV ($\text{dB}$) | Vegetation Radar Change ($\text{km}^2$) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **023** | 2026-06-16 | 2026-06-17 | 297.5 | +61.6 (+26%) | 99.1 – 385.8 | −9.20 | −15.37 | 78.6 |
| **024** | 2026-06-28 | 2026-06-29 | 360.5 | +124.6 (+53%) | 191.5 – 443.6 | −9.38 | −15.49 | 109.4 |
| **025** | 2026-07-10 | 2026-07-11 | 347.0 | +111.1 (+47%) | 141.1 – 447.0 | −9.43 | −15.58 | 112.9 |
| **026** | **2026-07-22** | **2026-07-23** | **455.5** | **+219.6 (+93%)** | **299.0 – 544.4** | **−9.62** | **−15.65** | **174.8** |
| **028** | 2026-08-15 | 2026-08-16 | 330.4 | +94.5 (+40%) | 143.6 – 422.2 | −8.97 | −15.16 | 56.9 |
| **029** | 2026-08-27 | 2026-08-28 | 309.3 | +73.4 (+31%) | 81.7 – 388.5 | −8.87 | −15.22 | 55.3 |
| **030** | 2026-09-08 | 2026-09-09 | 325.2 | +89.3 (+38%) | 81.1 – 395.2 | −8.74 | −15.19 | 54.6 |
| **031** | 2026-09-20 | 2026-09-21 | 309.3 | +73.4 (+31%) | 43.0 – 387.8 | −8.47 | −14.93 | 31.8 |
| **032** | 2026-10-02 | 2026-10-03 | 277.5 | +41.6 (+18%) | 138.1 – 348.7 | −8.48 | −14.94 | 25.0 |
| **033** | **2026-10-14** | **2026-10-15** | **235.9** | **Baseline** | **136.6 – 315.4** | **−8.36** | **−14.76** | **0.0** |

- **Highest Water Seen in Record:** July 22 UTC (**455.5 km²**, or **+219.6 km² / +93%** above the October 14 baseline of **235.9 km²**). This ranking holds across all three tested thresholds (`−17.5 dB`, `−15.5 dB`, and `−13.5 dB`).
- **Frequently Water-Observed Area:** **280.04 km²** exhibited a water-like signature in 8–10 of the 10 acquisitions (corresponding to the main Brahmaputra braided channel and perennial *beels*), while **197.37 km²** was water-observed in 1–7 acquisitions.
- **Why HHHH for Open Water:** Across all 10 dates, `HHHH` separates smooth water from land by **10.5 dB** on average vs. **8.5 dB** for `HVHV`, because cross-polarized `HV` scatters strongly within Kaziranga's dense tall grasslands.

![NISAR HHHH Backscatter Histogram](The_Larpers/docs/hh_histogram.png)

---

## 🔬 Methodology & Dataset Notes

- **Dataset:** NASA-ISRO NISAR Level-2 Geocoded Covariance (`L2 GCOV`), L-band, ascending **Track 040, Frame 015** (cropped to `92.95°E–93.65°E, 26.50°N–26.78°N`), **10.0 m × 10.0 m** pixel spacing in `EPSG:32646` (UTM Zone 46N), **PROVISIONAL** maturity (`CRID P05023`), accessed via NASA Earthdata / ASF DAAC.
- **Missing Track Interval:** No matching Track 040 / Frame 015 observation is available between **27 July and 10 August 2026** (NISAR instrument gap; Cycle 027 missing), so higher water levels may have occurred during that window.
- **Processing (`backend/processing/02_process_nisar.py`):**
  1. Applies a $5 \times 5$ (50 m) normalized spatial boxcar speckle filter in linear backscatter power ($\gamma^0$) before converting to decibels ($\gamma^0_{\text{dB}} = 10 \cdot \log_{10}(\gamma^0)$).
  2. Classifies smooth water-like surfaces using a consistent physical cutoff (`HHHH < −15.5 dB`), removes isolated patches $< 25\text{ pixels}$ ($2,500\text{ m}^2$), and evaluates cutoff sensitivity at `−17.5 dB` and `−13.5 dB`.
  3. Maps exploratory vegetation radar change over non-water vegetated land (`HVHV > −20 dB` on Oct 14) as the disjoint union of patches $\ge 2,500\text{ m}^2$ with either **Increased HH** ($\Delta\text{HH} > +2.5\text{ dB}$ and $\Delta\text{HH} > \Delta\text{HV} + 1.0\text{ dB}$) or **Changed HV** ($|\Delta\text{HV}| > 2.5\text{ dB}$).

---

## ⚠️ Scientific Limitations

- **Water-Like Surfaces vs. Confirmed Floodwater:** Low L-band backscatter (`< −15.5 dB`) identifies smooth, specular surfaces (river channels, *beels*, flooded paddies, and saturated smooth mudflats) rather than exclusively overbank flooding.
- **Exploratory Vegetation Changes:** Changes in `HH` and `HV` backscatter reflect shifts in vegetation structure, moisture, and surface-water interactions; they indicate areas worth investigating rather than confirmed vegetation damage.
- **12-Day Revisit & Track Gap:** Short-lived flood pulses between 12-day passes or during the July 27 – August 10 gap are not captured.

---

## ▶️ How to Run Locally

```bash
# 1. Inspect raw NISAR GeoTIFFs (place 20 .tif files in The_Larpers/data/raw_tifs/)
python The_Larpers/backend/processing/01_inspect_tifs.py

# 2. Generate PNG overlays, histogram, and nisar_metrics.json
python The_Larpers/backend/processing/02_process_nisar.py

# 3. Serve the web observatory
cd The_Larpers/frontend
python -m http.server 8000
# Open http://localhost:8000 in your browser