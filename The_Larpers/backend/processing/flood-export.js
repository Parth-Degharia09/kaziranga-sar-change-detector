/**
 * Kaziranga SAR Change Detector Sentinel-1 flood-extent export
 * Run in the GEE Code Editor (code.earthengine.google.com), then press Run on each task in the Tasks tab.
 *
 * Outputs (Google Drive folder "sar_atlas"), one GeoJSON FeatureCollection each:
 *   baseline_mar.geojson, flood_feb.geojson, flood_may.geojson, flood_jul.geojson, flood_oct.geojson
 * Drop them in a ./data folder next to the HTML, set REAL_DATA_BASE = './data', and serve over http.
 *
 * Feature properties the app reads:
 *   area_km2      polygon area (km²)               -> "Submerged area"
 *   mean_db       mean VV backscatter (dB)         -> "Mean backscatter" (area-weighted)
 *   habitat_km2   area on cropland/natural cover   -> "Cropland / habitat affected %" = sum / sum(area_km2)
 *   pop_exposed   WorldPop people inside polygon   -> "Estimated population exposed"
 * plus stage, window, sensor, polarisation, threshold_db (metadata).
 */

// ---------- Parameters ----------
var YEAR = 2024;                 // season to map
var AOI = ee.Geometry.Rectangle([91.9, 26.0, 94.95, 27.4]);  // Brahmaputra valley, Dibrugarh to Guwahati
var THRESH_DB = -18;             // open water: VV backscatter below this
var SCALE = 100;                 // metres; vectorising at 10 m over this AOI will time out (try 30 m on sub-regions)
var MIN_KM2 = 0.25;              // drop specks smaller than this
var MAX_FEATURES = 5000;         // keep the largest N polygons per stage (keeps GeoJSON browser-friendly)
var SIMPLIFY_M = 100;            // geometry simplification tolerance (m)
var MAX_SLOPE_DEG = 5;           // mask radar shadow on hill slopes

var WINDOWS = {
  baseline_mar: [YEAR + '-03-01', YEAR + '-04-01'],
  flood_feb:    [YEAR + '-02-01', YEAR + '-03-01'],
  flood_may:    [YEAR + '-05-01', YEAR + '-06-01'],
  flood_jul:    [YEAR + '-07-01', YEAR + '-08-01'],
  flood_oct:    [YEAR + '-10-01', YEAR + '-11-01']
};

// ---------- Inputs ----------
// Sentinel-1 GRD in GEE is already in dB. Ascending and descending passes are both used.
var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .filterBounds(AOI)
  .select('VV');

var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'));
var landcover = ee.ImageCollection('ESA/WorldCover/v200').first().select('Map');
// tree, shrub, grass, crop, herbaceous wetland, mangrove
var habitat = landcover.remap([10, 20, 30, 40, 90, 95], [1, 1, 1, 1, 1, 1], 0);
// Verify the band name ('population') in the dataset page if this errors.
var pop = ee.ImageCollection('WorldPop/GP/100m/pop')
  .filter(ee.Filter.eq('country', 'IND'))
  .filter(ee.Filter.eq('year', 2020))
  .mosaic().select('population').unmask(0);

// ---------- Water mask for a date window ----------
function waterImage(start, end) {
  var vv = s1.filterDate(start, end).median().focal_median(50, 'circle', 'meters');
  var water = vv.lt(THRESH_DB).and(slope.lt(MAX_SLOPE_DEG)).selfMask();
  var connected = water.connectedPixelCount(100, true);
  return water.updateMask(connected.gte(25));   // remove isolated speckle
}

// ---------- One stage -> FeatureCollection in the app's schema ----------
function num(v) { return ee.Number(ee.Algorithms.If(v, v, 0)); }

function buildStage(name, win) {
  var vv = s1.filterDate(win[0], win[1]).median();
  var water = waterImage(win[0], win[1]);

  var vec = water.reduceToVectors({
    geometry: AOI, scale: SCALE, geometryType: 'polygon', eightConnected: true,
    maxPixels: 1e13, tileScale: 4
  }).map(function (f) {
    return f.set('area_km2', f.geometry().area(100).divide(1e6));
  }).filter(ee.Filter.gte('area_km2', MIN_KM2))
    .limit(MAX_FEATURES, 'area_km2', false);

  var stack = ee.Image.cat([
    vv.rename('vv'),
    ee.Image.pixelArea().divide(1e6).multiply(habitat).rename('habitat_km2'),
    pop.rename('pop'),
    ee.Image.constant(1).rename('n')
  ]);

  var stats = stack.reduceRegions({
    collection: vec, reducer: ee.Reducer.sum(), scale: SCALE, tileScale: 4
  });

  return stats.map(function (f) {
    return ee.Feature(f.geometry().simplify(SIMPLIFY_M), {
      stage: name,
      window: win[0] + '/' + win[1],
      sensor: 'Sentinel-1 C-band IW GRD',
      polarisation: 'VV',
      threshold_db: THRESH_DB,
      area_km2: f.get('area_km2'),
      mean_db: num(f.get('vv')).divide(num(f.get('n')).max(1)),
      habitat_km2: num(f.get('habitat_km2')),
      pop_exposed: num(f.get('pop'))
    });
  });
}

// ---------- Exports ----------
Object.keys(WINDOWS).forEach(function (name) {
  Export.table.toDrive({
    collection: buildStage(name, WINDOWS[name]),
    description: name,
    folder: 'sar-change-detector',
    fileNamePrefix: name,
    fileFormat: 'GeoJSON'
  });
});

// ---------- Quick visual check (July peak) ----------
Map.centerObject(AOI, 8);
Map.addLayer(waterImage(WINDOWS.flood_jul[0], WINDOWS.flood_jul[1]), {palette: ['1D4ED8']}, 'Jul water (VV < ' + THRESH_DB + ' dB)');
Map.addLayer(waterImage(WINDOWS.baseline_mar[0], WINDOWS.baseline_mar[1]), {palette: ['0F2942']}, 'Mar baseline water');

// ---------- Chart arrays for the app (paste into RAIN and EXT) ----------
var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY');
var months = ee.List.sequence(1, 12);
print('RAIN (mm/month, AOI mean)', months.map(function (m) {
  var s = ee.Date.fromYMD(YEAR, m, 1);
  var r = chirps.filterDate(s, s.advance(1, 'month')).sum()
    .reduceRegion({reducer: ee.Reducer.mean(), geometry: AOI, scale: 5566, maxPixels: 1e9});
  return ee.Number(r.get('precipitation')).round();
}));
print('EXT (km2 water per month)', months.map(function (m) {
  var s = ee.Date.fromYMD(YEAR, m, 1);
  var a = waterImage(s, s.advance(1, 'month')).unmask(0).multiply(ee.Image.pixelArea()).divide(1e6)
    .reduceRegion({reducer: ee.Reducer.sum(), geometry: AOI, scale: SCALE, maxPixels: 1e13, tileScale: 4});
  return ee.Number(a.get('VV')).round();
}));