from pathlib import Path
import numpy as np
import rasterio

# Automatically find data/raw_tifs relative to this script's location
BASE_DIR = Path(__file__).resolve().parents[2]
TIF_DIR = BASE_DIR / "data" / "raw_tifs"

files = sorted(list(TIF_DIR.glob("*.tif")) + list(TIF_DIR.glob("*.tiff")))

print(f"Looking in: {TIF_DIR}")
print(f"Found {len(files)} GeoTIFF files.\n")
print(f"{'Filename':<32} | {'CRS':<12} | {'Shape':<12} | {'Res (m)':<10} | {'Min':<10} | {'Median':<10} | {'Max':<10} | {'NaN %':<6}")
print("-" * 115)

for f in files:
    with rasterio.open(f) as src:
        arr = src.read(1).astype("float64")
        nodata = src.nodata
        if nodata is not None:
            arr[arr == nodata] = np.nan
        arr[arr <= 0] = np.nan

        valid = arr[~np.isnan(arr)]
        nan_pct = 100.0 * np.isnan(arr).sum() / arr.size
        res_x, res_y = src.res

        print(f"{f.name:<32} | {str(src.crs):<12} | {str(arr.shape):<12} | "
              f"{res_x:.1f}x{res_y:.1f} | {np.min(valid):<10.5f} | {np.median(valid):<10.5f} | "
              f"{np.max(valid):<10.5f} | {nan_pct:<5.1f}%")