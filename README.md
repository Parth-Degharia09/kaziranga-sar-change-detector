# Kaziranga Monsoon Water Observatory 🛰️🌊

**Exploring seasonal surface-water dynamics and L-band vegetation backscatter shifts across the Brahmaputra–Kaziranga floodplain using NASA-ISRO NISAR radar.**

Built for the **NASA Space Apps Challenge 2026 — Dancing with the SARs** by **Team The Larpers**. (Repository: `kaziranga-sar-change-detector`.)

---

## 🎯 The Problem & Ecological Context

Kaziranga National Park on the south bank of the Brahmaputra River in Assam undergoes dramatic seasonal inundation every monsoon. While seasonal flooding is ecologically vital—replenishing wetlands (*beels*), sustaining alluvial grasslands, and clearing invasive species—extreme inundation forces wildlife southward across National Highway 37 toward the Karbi (Mikir) Hills.

Optical satellites are routinely blocked by dense monsoon cloud cover during peak wet months. **NASA-ISRO NISAR's L-band Synthetic Aperture Radar (SAR)** (~24 cm wavelength) images through clouds and darkness on a 12-day repeat cycle. This observatory turns 10 multi-temporal dual-polarization (`HHHH` + `HVHV`) NISAR acquisitions into a plain-language, interactive explorer.

> **2026 context:** On **21 July 2026**—one day before our highest-water-like NISAR acquisition—Kaziranga Divisional Forest Officer (DFO) Arun Vignesh reported normal seasonal wetting with only four forest camps inundated and no flood emergency. Accordingly, this tool tracks *surface-water dynamics* across the combined Brahmaputra river and floodplain corridor rather than claiming a park-wide flood disaster. <!-- TODO: add a link to the published DFO statement here and in frontend/index.html (DFO_SOURCE_URL). -->

---

## 💡 Core Questions & Interactive Features

1. **Where is the water? (`Where water is` & `Raw radar view`)**
   - 10-date timeline slider (`Jun 16` – `Oct 14, 2026`, UTC & IST) with a split-screen **Before / After swipe** comparing the Oct 14 reference against any selected date.
   - Plain-language headlines and an **Observation Metadata** panel (UTC/IST timestamps, cycle number, polarization, CRID maturity status, cutoff).
2. **How often is an area wet? (`How often wet`)**
   - Full-width 10-date frequency map: **occasional (10–30%)**, **frequent (40–70%)**, **persistent (80–100%, 8–10 of 10 passes)**.
3. **How does vegetation radar response change? (`Vegetation radar change`)**
   - Exploratory `HHHH`/`HVHV` change relative to Oct 14 over non-water vegetated land: **Increased HH** (amber: possible double-bounce) vs. **Changed HV** (violet: possible canopy structure or moisture shift).
4. **Evidence, sensitivity & export**
   - Every area comes with a **±2 dB cutoff-sensitivity range** (−17.5 to −13.5 dB; *a sensitivity check, not a confidence interval*) and a **per-date adaptive-cutoff cross-check**.
   - CSV export (selected date or all dates) and a **GeoJSON** of the wetness-frequency polygons.
   - Optional: in-park statistics (needs a park boundary file) and a river-gauge/rainfall overlay on the chart. See [`The_Larpers/docs/DATA.md`](The_Larpers/docs/DATA.md).

---

## 📊 Key Findings (Cropped Track 040 / Frame 015 window: 2,176.13 km²)

<!-- RESULTS_START -->
| Cycle | Date (UTC) | Local date (IST) | Water-like area (km²) | Extra vs. Oct 14 (km²) | Cutoff check −17.5 → −13.5 dB (km²) | Mean HHHH (dB) | Mean HVHV (dB) | Vegetation radar change (km²) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 023 | 2026-06-16 | 2026-06-17 | 297.5 | +61.6 (+26%) | 99.1 – 385.8 | -9.20 | -15.37 | 126.3 |
| 024 | 2026-06-28 | 2026-06-29 | 360.4 | +124.5 (+53%) | 191.4 – 443.6 | -9.38 | -15.49 | 138.0 |
| 025 | 2026-07-10 | 2026-07-11 | 347.0 | +111.1 (+47%) | 141.1 – 447.0 | -9.43 | -15.58 | 146.2 |
| **026** | **2026-07-22** | **2026-07-23** | **455.5** | **+219.6 (+93%)** | **299.0 – 544.4** | **-9.62** | **-15.65** | **174.8** |
| 028 | 2026-08-15 | 2026-08-16 | 330.4 | +94.5 (+40%) | 143.6 – 422.2 | -8.97 | -15.16 | 141.8 |
| 029 | 2026-08-27 | 2026-08-28 | 309.3 | +73.3 (+31%) | 81.7 – 388.5 | -8.87 | -15.22 | 111.9 |
| 030 | 2026-09-08 | 2026-09-09 | 325.2 | +89.3 (+38%) | 81.0 – 395.1 | -8.74 | -15.19 | 129.3 |
| 031 | 2026-09-20 | 2026-09-21 | 309.3 | +73.4 (+31%) | 43.0 – 387.8 | -8.47 | -14.93 | 85.7 |
| 032 | 2026-10-02 | 2026-10-03 | 277.5 | +41.6 (+18%) | 138.1 – 348.7 | -8.48 | -14.94 | 23.4 |
| **033** | **2026-10-14** | **2026-10-15** | **235.9** | **Baseline** | **136.6 – 315.4** | **-8.36** | **-14.76** | **0.0** |

- **Highest water-like area in this 10-pass series:** Jul 22 UTC (**455.5 km²**, **+219.6 km² / +93%** over the Oct 14 reference of 235.9 km²). Jul 22 stays the highest at all three tested cutoffs (−17.5, −15.5, −13.5 dB).
- **Often-wet area:** 280.04 km² was water-like in 8–10 of the 10 acquisitions (main braided channel and perennial *beels*); 197.37 km² in 1–7 acquisitions.
- **Consistency check:** the often-wet area is larger than the Oct 14 water area, so at least 44.1 km² of often-wet pixels are not water-like on Oct 14.
- **Cutoff sensitivity caveat:** at the strict −17.5 dB cutoff, Jun 16, Aug 27, Sep 08, Sep 20 fall *below* the Oct 14 reference, so the size of each date's margin over Oct 14 depends on the cutoff (the ±2 dB band is a sensitivity check, not a confidence interval).
<!-- RESULTS_END -->

![NISAR HHHH backscatter histogram](The_Larpers/docs/hh_histogram.png)

*The fixed −15.5 dB cutoff sits near the valley between the water peak (≈ −18 dB) and the land peak. The strict −17.5 dB cutoff cuts through the water peak, which is why the sensitivity band is wide. Re-running `02_process_nisar.py` redraws this figure with the adaptive cutoffs.*

**How to read the time series.** Apart from the Jul 22 peak, water-like area stays between about 300 and 360 km² from mid-June to late September, then falls to 278 and 236 km² in October. The data do not by themselves show a steady recession; pairing it with river-gauge or rainfall data (see `DATA.md`) would be needed to say more.

---

## 🔬 Methodology & Dataset Notes

- **Dataset:** NASA-ISRO NISAR Level-2 Geocoded Covariance (`L2 GCOV`), L-band, ascending **Track 040, Frame 015** (cropped to `92.95°E–93.65°E, 26.50°N–26.78°N`), **10 m** pixels in `EPSG:32646` (UTM 46N), **PROVISIONAL** maturity (`CRID P05023`), from NASA Earthdata / ASF DAAC.
- **Missing interval:** No Track 040 / Frame 015 observation exists between **27 July and 10 August 2026** (Cycle 027 missing), so higher water may have occurred then.
- **Processing** (`backend/processing/02_process_nisar.py`, helpers in `sar_utils.py`):
  1. A 5 × 5 (50 m) NaN-aware boxcar speckle filter in linear power, then conversion to dB.
  2. **Water-like surface:** `HHHH < −15.5 dB`, patches smaller than 25 pixels (2,500 m²) removed. The same rule at −17.5 and −13.5 dB gives the sensitivity band. A **per-date adaptive cutoff** (minimum of the smoothed histogram between the water and land modes, with Otsu as a labelled fallback) is reported as a cross-check.
  3. **Vegetation radar change** over non-water land with `HVHV > −20 dB` on Oct 14: *Increased HH* (ΔHH > +2.5 dB and ΔHH > ΔHV + 1 dB) or *Changed HV* (|ΔHV| > 2.5 dB), patches ≥ 2,500 m².
  4. **Frequency map:** fraction of the 10 dates on which each pixel is water-like. Persistent water = ≥ 8 of 10.
- **Outputs:** water masks and vegetation maps as lossless PNG; false-colour radar views as WebP (about 9× smaller than PNG); metrics JSON; GeoJSON of frequency classes (needs `shapely`).

---

## ✅ Validation

`backend/processing/03_validate_gsw.py` compares a NISAR water mask with the **JRC Global Surface Water** occurrence layer (recall of permanent water, precision against "ever water", IoU) for the fixed, strict, loose and adaptive cutoffs, and writes `docs/validation_gsw.json` and `docs/validation_gsw.png`.

**Status:** the script is included; no validation results have been published yet. GSW ends in 2021 and the Brahmaputra is braided, so expect imperfect agreement and treat it as a sanity check rather than ground truth.

---

## ⚠️ Scientific Limitations

- **Water-like surfaces vs. confirmed floodwater:** low L-band backscatter identifies smooth, specular surfaces (river channels, *beels*, flooded paddies, smooth wet mudflats), not only overbank flooding.
- **Cutoff sensitivity is not an uncertainty interval:** at the strict cutoff several dates fall below the Oct 14 reference, so the *size* of each date's margin over Oct 14 depends on the cutoff. Jul 22 being highest does not.
- **Flooded vegetation is under-counted:** water under tall grass or forest *raises* HH through double-bounce, so a low-backscatter cutoff misses it. The amber class is only a partial proxy.
- **Baseline and season:** Oct 14 is post-monsoon but not necessarily the seasonal minimum; vegetation-response differences mix real change with phenology and soil moisture. They indicate areas worth investigating, not confirmed vegetation damage.
- **Frequency map vs. reference date:** often-wet area can exceed the Oct 14 water area, so some often-wet pixels are not water-like on the reference date.
- **12-day revisit & track gap:** short flood pulses between passes, or in the 27 Jul – 10 Aug gap, are not captured.
- **Provisional product:** NISAR data are PROVISIONAL (`CRID P05023`) and may be reprocessed.
- **Not modelled:** wind roughening of water surfaces, incidence-angle effects and calibration differences between dates can all affect date-to-date comparisons.

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt

# 0. Get the inputs (see The_Larpers/docs/DATA.md) into The_Larpers/data/raw_tifs/

# 1. Inspect raw NISAR GeoTIFFs
python The_Larpers/backend/processing/01_inspect_tifs.py

# 2. Generate overlays, GeoJSON, histogram and nisar_metrics.json
python The_Larpers/backend/processing/02_process_nisar.py

# 3. Refresh the results table in this README from the new JSON
python The_Larpers/backend/processing/04_update_readme_table.py

# 4. (Optional) validate against JRC Global Surface Water
python The_Larpers/backend/processing/03_validate_gsw.py --gsw The_Larpers/data/gsw/<occurrence_tile>.tif

# 5. Serve the web observatory
cd The_Larpers/frontend
python -m http.server 8000      # open http://localhost:8000
```

Run the unit tests (no raster data needed): `python The_Larpers/backend/tests/test_sar_utils.py`

The web app loads Leaflet, Chart.js, Tailwind and Esri basemap tiles from the internet; keep a connection (or a screen recording) handy when demoing.

## 🗂️ Repository layout

```
The_Larpers/
  backend/processing/   01 inspect · 02 process · 03 validate (GSW) · 04 README table · sar_utils.py
  backend/tests/        unit tests for the helpers
  frontend/             index.html + data/ (overlays, metrics JSON, GeoJSON)
  docs/                 histogram, DATA.md, validation outputs
```
