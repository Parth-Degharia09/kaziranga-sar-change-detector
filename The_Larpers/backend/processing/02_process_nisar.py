import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, transform_bounds
from scipy.ndimage import uniform_filter
from skimage.morphology import remove_small_objects
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

BASE_DIR = Path(__file__).resolve().parents[2]
TIF_DIR = BASE_DIR / "data" / "raw_tifs"
IMERG_CSV = BASE_DIR / "data" / "imerg_kaziranga_2026.csv"
OUT_DIR = BASE_DIR / "frontend" / "data"
DOCS_DIR = BASE_DIR / "docs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Neutral, factual cycle descriptions (no contradictory hand-typed trend labels)
DATES = [
    ("20260616", "Jun 16", "Jun 17 IST", "Cycle 023 observation (Track 040 / Frame 015)"),
    ("20260628", "Jun 28", "Jun 29 IST", "Cycle 024 observation (Track 040 / Frame 015)"),
    ("20260710", "Jul 10", "Jul 11 IST", "Cycle 025 observation (Track 040 / Frame 015)"),
    ("20260722", "Jul 22", "Jul 23 IST", "Cycle 026 observation — highest water-like extent seen in series"),
    ("20260815", "Aug 15", "Aug 16 IST", "Cycle 028 observation — first pass after Jul 27–Aug 10 track gap"),
    ("20260827", "Aug 27", "Aug 28 IST", "Cycle 029 observation (Track 040 / Frame 015)"),
    ("20260908", "Sep 08", "Sep 09 IST", "Cycle 030 observation (Track 040 / Frame 015)"),
    ("20260920", "Sep 20", "Sep 21 IST", "Cycle 031 observation (Track 040 / Frame 015)"),
    ("20261002", "Oct 02", "Oct 03 IST", "Cycle 032 observation (Track 040 / Frame 015)"),
    ("20261014", "Oct 14", "Oct 15 IST", "Cycle 033 observation — lowest water-like extent (reference baseline)"),
]

PIXEL_AREA_KM2 = (10.0 * 10.0) / 1e6
MIN_PATCH_PIXELS = 25
EXPORT_WIDTH = 1600
FIXED_THRESH_DB = -15.5


def load_imerg_12day_rainfall():
    """Reads NASA Giovanni IMERG daily CSV (mm/day) and requires all 12 days to be valid."""
    if not IMERG_CSV.exists():
        return None
    daily = {}
    with open(IMERG_CSV, "r", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if len(row) < 2:
                continue
            dt_str = row[0].strip()[:10]
            try:
                dt = datetime.strptime(dt_str, "%Y-%m-%d").date()
                val = float(row[1])
                if np.isfinite(val) and val >= 0:
                    daily[dt] = val
            except ValueError:
                continue
    if not daily:
        return None

    rain_by_date = {}
    for date_str, *_ in DATES:
        target = datetime.strptime(date_str, "%Y%m%d").date()
        window_days = [target - timedelta(days=k) for k in range(12)]
        if all(d in daily for d in window_days):
            rain_by_date[date_str] = round(sum(daily[d] for d in window_days), 1)
        else:
            rain_by_date[date_str] = None
    return rain_by_date
def to_db(linear_arr, nodata=None):
    arr = linear_arr.astype("float32").copy()
    if nodata is not None:
        arr[arr == nodata] = np.nan
    arr[~np.isfinite(arr) | (arr <= 0)] = np.nan

    valid_mask = np.isfinite(arr)
    filled = np.where(valid_mask, arr, 0.0)
    weights = valid_mask.astype("float32")
    smooth_sum = uniform_filter(filled, size=5)
    smooth_w = uniform_filter(weights, size=5)

    with np.errstate(divide="ignore", invalid="ignore"):
        smooth = np.where(smooth_w > 0.2, smooth_sum / smooth_w, np.nan)
        db = 10.0 * np.log10(np.clip(smooth, 1e-6, None))
        db[~np.isfinite(smooth)] = np.nan
    return db


def clean_small(mask):
    try:
        return remove_small_objects(mask, max_size=MIN_PATCH_PIXELS - 1)
    except TypeError:
        return remove_small_objects(mask, min_size=MIN_PATCH_PIXELS)


def classify_water(hh_db, thresh_db):
    return clean_small(np.isfinite(hh_db) & (hh_db < thresh_db))


def reproject_to_3857(arr, src_transform, src_crs, dst_width, resampling=Resampling.nearest):
    dst_crs = "EPSG:3857"
    left, bottom, right, top = transform_bounds(
        src_crs, dst_crs, *rasterio.transform.array_bounds(arr.shape[-2], arr.shape[-1], src_transform)
    )
    aspect = (top - bottom) / (right - left)
    dst_height = int(round(dst_width * aspect))
    dst_transform = rasterio.transform.from_bounds(left, bottom, right, top, dst_width, dst_height)

    if arr.ndim == 2:
        dst = np.zeros((dst_height, dst_width), dtype=arr.dtype)
        reproject(arr, dst, src_transform=src_transform, src_crs=src_crs,
                  dst_transform=dst_transform, dst_crs=dst_crs, resampling=resampling)
    else:
        dst = np.zeros((arr.shape[0], dst_height, dst_width), dtype=arr.dtype)
        for b in range(arr.shape[0]):
            reproject(arr[b], dst[b], src_transform=src_transform, src_crs=src_crs,
                      dst_transform=dst_transform, dst_crs=dst_crs, resampling=resampling)
    return dst


def save_rgba_png(rgba_uint8, out_path):
    Image.fromarray(rgba_uint8, mode="RGBA").save(out_path, optimize=True)


def main():
    water_stack = []
    hh_stack = []
    hv_stack = []
    records = []
    src_transform = None
    src_crs = None
    wgs84_bounds = None
    hist_samples = {}
    imerg_rain = load_imerg_12day_rainfall()

    with rasterio.open(TIF_DIR / "kaziranga_20261014_HHHH.tif") as s_hh, \
         rasterio.open(TIF_DIR / "kaziranga_20261014_HVHV.tif") as s_hv:
        base_hh_db = to_db(s_hh.read(1), s_hh.nodata)
        base_hv_db = to_db(s_hv.read(1), s_hv.nodata)

    for date_str, label, ist_label, desc in DATES:
        hh_path = TIF_DIR / f"kaziranga_{date_str}_HHHH.tif"
        hv_path = TIF_DIR / f"kaziranga_{date_str}_HVHV.tif"

        with rasterio.open(hh_path) as src_hh, rasterio.open(hv_path) as src_hv:
            if src_transform is None:
                src_transform = src_hh.transform
                src_crs = src_hh.crs
                w, s, e, n = transform_bounds(src_crs, "EPSG:4326", *src_hh.bounds)
                wgs84_bounds = [[round(s, 6), round(w, 6)], [round(n, 6), round(e, 6)]]

            hh_db = to_db(src_hh.read(1), src_hh.nodata)
            hv_db = to_db(src_hv.read(1), src_hv.nodata)

        if date_str in ("20260722", "20261014"):
            hist_samples[label] = hh_db[np.isfinite(hh_db)][::10]

        water_mid = classify_water(hh_db, FIXED_THRESH_DB)
        water_low = classify_water(hh_db, FIXED_THRESH_DB - 2.0)
        water_high = classify_water(hh_db, FIXED_THRESH_DB + 2.0)

        water_stack.append(water_mid.astype(np.uint8))
        hh_stack.append(hh_db)
        hv_stack.append(hv_db)

        area_mid = float(water_mid.sum() * PIXEL_AREA_KM2)
        area_low = float(water_low.sum() * PIXEL_AREA_KM2)
        area_high = float(water_high.sum() * PIXEL_AREA_KM2)

        # Water Mask PNG
        w_3857 = reproject_to_3857(water_mid.astype(np.uint8), src_transform, src_crs, EXPORT_WIDTH, Resampling.nearest)
        rgba_water = np.zeros((w_3857.shape[0], w_3857.shape[1], 4), dtype=np.uint8)
        rgba_water[w_3857 == 1] = [29, 78, 216, 195]
        save_rgba_png(rgba_water, OUT_DIR / f"water_{date_str}.png")

        # Dual-Pol False-Color RGB (R=HH, G=HV, B=HH-HV)
        hh_clean = np.nan_to_num(hh_db, nan=-22.0)
        hv_clean = np.nan_to_num(hv_db, nan=-28.0)
        r_norm = np.clip((hh_clean - (-22.0)) / (-4.0 - (-22.0)), 0, 1)
        g_norm = np.clip((hv_clean - (-28.0)) / (-10.0 - (-28.0)), 0, 1)
        b_norm = np.clip(((hh_clean - hv_clean) - 2.0) / (12.0 - 2.0), 0, 1)

        rgb_stack = np.stack([(r_norm * 255).astype(np.uint8), (g_norm * 255).astype(np.uint8), (b_norm * 255).astype(np.uint8)], axis=0)
        rgb_3857 = reproject_to_3857(rgb_stack, src_transform, src_crs, EXPORT_WIDTH, Resampling.bilinear)
        alpha = np.full((rgb_3857.shape[1], rgb_3857.shape[2], 1), 235, dtype=np.uint8)
        rgba_rgb = np.concatenate([np.transpose(rgb_3857, (1, 2, 0)), alpha], axis=2)
        save_rgba_png(rgba_rgb, OUT_DIR / f"rgb_{date_str}.png")

        # Experimental Vegetation Radar Change vs Oct 14
        land_mask = np.isfinite(hh_db) & (~water_mid)
        d_hh = hh_db - base_hh_db
        d_hv = hv_db - base_hv_db
        veg_domain = land_mask & (base_hv_db > -20.0)
        double_bounce_cand = clean_small(veg_domain & (d_hh > 2.5) & (d_hh > d_hv + 1.0))
        hv_shift_cand = clean_small(veg_domain & (~double_bounce_cand) & (np.abs(d_hv) > 2.5))

        veg_code = np.zeros(hh_db.shape, dtype=np.uint8)
        veg_code[hv_shift_cand] = 2
        veg_code[double_bounce_cand] = 1

        v_3857 = reproject_to_3857(veg_code, src_transform, src_crs, EXPORT_WIDTH, Resampling.nearest)
        rgba_veg = np.zeros((v_3857.shape[0], v_3857.shape[1], 4), dtype=np.uint8)
        rgba_veg[v_3857 == 1] = [217, 119, 6, 200]
        rgba_veg[v_3857 == 2] = [124, 58, 237, 175]
        save_rgba_png(rgba_veg, OUT_DIR / f"veg_{date_str}.png")

        rec = {
            "date": date_str,
            "label": label,
            "ist_label": ist_label,
            "description": desc,
            "threshold_db": FIXED_THRESH_DB,
            "water_km2": round(area_mid, 2),
            "water_low_km2": round(area_low, 2),
            "water_high_km2": round(area_high, 2),
            "water_pct_box": round(100.0 * area_mid / (hh_db.size * PIXEL_AREA_KM2), 1),
            "mean_hh_db": round(float(np.nanmean(hh_db)), 2),
            "mean_hv_db": round(float(np.nanmean(hv_db)), 2),
            "veg_double_bounce_km2": round(float(double_bounce_cand.sum() * PIXEL_AREA_KM2), 2),
            "veg_hv_shift_km2": round(float(hv_shift_cand.sum() * PIXEL_AREA_KM2), 2),
            "water_png": f"data/water_{date_str}.png",
            "rgb_png": f"data/rgb_{date_str}.png",
            "veg_png": f"data/veg_{date_str}.png",
        }
        if imerg_rain is not None:
            rec["rain_12d_mm"] = imerg_rain.get(date_str, None)
        records.append(rec)

    max_mid = max(records, key=lambda r: r["water_km2"])["date"]
    max_low = max(records, key=lambda r: r["water_low_km2"])["date"]
    max_high = max(records, key=lambda r: r["water_high_km2"])["date"]
    jul22_stays_highest = (max_mid == max_low == max_high == "20260722")

    stack_arr = np.stack(water_stack, axis=0)
    freq = stack_arr.sum(axis=0).astype(np.float32) / len(DATES)
    core_channel_mask = (freq >= 0.80)
    dry_land_mask = (freq == 0.0)

    # Non-circular polarization comparison using the 10-date multi-temporal river channel core vs dry land
    hh_core_contrast = float(np.nanmean([np.nanmedian(h[dry_land_mask]) - np.nanmedian(h[core_channel_mask]) for h in hh_stack]))
    hv_core_contrast = float(np.nanmean([np.nanmedian(h[dry_land_mask]) - np.nanmedian(h[core_channel_mask]) for h in hv_stack]))

    perm_km2 = round(float(core_channel_mask.sum() * PIXEL_AREA_KM2), 2)
    seasonal_km2 = round(float(((freq > 0.0) & (freq < 0.80)).sum() * PIXEL_AREA_KM2), 2)
    total_box_km2 = round(float(freq.size * PIXEL_AREA_KM2), 2)

    freq_3857 = reproject_to_3857(freq, src_transform, src_crs, EXPORT_WIDTH, Resampling.bilinear)
    cmap = matplotlib.colormaps["YlGnBu"]
    rgba_freq = (cmap(freq_3857) * 255).astype(np.uint8)
    rgba_freq[..., 3] = np.where(freq_3857 > 0.05, 215, 0)
    save_rgba_png(rgba_freq, OUT_DIR / "inundation_frequency.png")

    plt.figure(figsize=(8, 4), dpi=150)
    plt.hist(hist_samples["Oct 14"], bins=120, range=(-26, -2), density=True, alpha=0.55, color="#0F2942", label="Oct 14 (Low-water baseline)")
    plt.hist(hist_samples["Jul 22"], bins=120, range=(-26, -2), density=True, alpha=0.55, color="#1D4ED8", label="Jul 22 (Highest water seen)")
    plt.axvline(FIXED_THRESH_DB, color="#C2410C", linestyle="--", linewidth=2, label="Water cutoff (−15.5 dB)")
    plt.axvspan(FIXED_THRESH_DB - 2, FIXED_THRESH_DB + 2, color="#C2410C", alpha=0.12, label="±2 dB sensitivity band (−17.5 to −13.5 dB)")
    plt.title("NISAR L-Band HHHH Backscatter Distribution (Kaziranga Study Box)")
    plt.xlabel("Backscatter gamma-nought (dB) — Smooth water (< −15.5 dB) vs. Land/Vegetation (> −15.5 dB)")
    plt.ylabel("Pixel Density")
    plt.legend(frameon=True, fontsize=8.5)
    plt.tight_layout()
    plt.savefig(DOCS_DIR / "hh_histogram.png")
    plt.close()

    summary = {
        "sensor": "NASA-ISRO NISAR L2 GCOV (L-band, Track 040 Frame 015 crop, Ascending, 10 m)",
        "product_status": "PROVISIONAL (CRID P05023)",
        "crs_native": str(src_crs),
        "bounds_wgs84": wgs84_bounds,
        "study_box_km2": total_box_km2,
        "frequently_water_observed_km2": perm_km2,
        "occasionally_water_observed_km2": seasonal_km2,
        "hh_core_channel_contrast_db": round(hh_core_contrast, 1),
        "hv_core_channel_contrast_db": round(hv_core_contrast, 1),
        "jul22_highest_across_all_thresholds": jul22_stays_highest,
        "has_imerg_rainfall": imerg_rain is not None,
        "frequency_png": "data/inundation_frequency.png",
        "dates": records,
    }

    with open(OUT_DIR / "nisar_metrics.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Done! IMERG Rainfall loaded: {imerg_rain is not None} | "
          f"Core-channel contrast HH: {summary['hh_core_channel_contrast_db']} dB, HV: {summary['hv_core_channel_contrast_db']} dB")


if __name__ == "__main__":
    main()