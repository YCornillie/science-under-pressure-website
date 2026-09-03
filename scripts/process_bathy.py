#!/usr/bin/env python3
"""Turn raw swissBATHY3D ESRI-ASCII-GRID tiles into one compact heightmap PNG.

Pipeline (documented for reproducibility — the raw tiles are NOT kept in the repo):
  1. Download the lake from the swisstopo STAC API, e.g. Walensee:
       https://data.geo.admin.ch/ch.swisstopo.swissbathy3d/
         swissbathy3d_walensee/swissbathy3d_walensee_2056_5728.esriasciigrid.zip
  2. Unzip the .asc tiles into  ./raw_swissbathy3d/
  3. Run:  python process_bathy.py
  4. Output:  ../assets/walensee_heightmap.png
              (R = depth 0..255 [deep..shore], G = water mask, B = 0)
  5. Then run ../build.py to embed it into index.html.

Heightmap encoding used by the WebGL hero shader:
  R channel = normalized elevation (0 = deepest point, 255 = shoreline/surface)
  G channel = water mask (255 = lake bed data present, 0 = land -> discarded)
"""
import numpy as np, glob, os
from PIL import Image

HERE   = os.path.dirname(os.path.abspath(__file__))
DDIR   = os.path.join(HERE, "raw_swissbathy3d")          # put the raw .asc tiles here
OUTPNG = os.path.join(HERE, "..", "assets", "walensee_heightmap.png")
FACTOR = 12                                              # downsample factor (1 m -> 12 m cells)

files = sorted(glob.glob(os.path.join(DDIR, "*.asc")))
if not files:
    raise SystemExit(f"no .asc tiles in {DDIR} — see the docstring for how to fetch them")
print("tiles:", len(files))

# --- pass 1: headers + mosaic extent ---
meta, minx, miny, maxx, maxy, cell = [], 1e18, 1e18, -1e18, -1e18, None
for f in files:
    hdr = {}
    with open(f) as fh:
        for _ in range(6):
            k, v = fh.readline().split(); hdr[k.lower()] = float(v)
    ncols, nrows = int(hdr["ncols"]), int(hdr["nrows"])
    xll, yll, cell, nd = hdr["xllcorner"], hdr["yllcorner"], hdr["cellsize"], hdr["nodata_value"]
    meta.append((f, ncols, nrows, xll, yll, nd))
    minx, miny = min(minx, xll), min(miny, yll)
    maxx, maxy = max(maxx, xll + ncols * cell), max(maxy, yll + nrows * cell)

W, H = int(round((maxx - minx) / cell)), int(round((maxy - miny) / cell))
mos = np.full((H, W), np.nan, dtype=np.float32)

# --- pass 2: place tiles into the mosaic ---
for (f, ncols, nrows, xll, yll, nd) in meta:
    with open(f) as fh:
        for _ in range(6):
            fh.readline()
        arr = np.array(fh.read().split(), dtype=np.float32).reshape(nrows, ncols)
    arr[arr == nd] = np.nan
    col0 = int(round((xll - minx) / cell))
    row0 = int(round((maxy - (yll + nrows * cell)) / cell))
    mos[row0:row0 + nrows, col0:col0 + ncols] = arr

valid = ~np.isnan(mos)
area_km2 = valid.sum() * cell * cell / 1e6
print(f"water area {area_km2:.2f} km2, depth range {np.nanmax(mos)-np.nanmin(mos):.1f} m")

# --- crop to the lake bounding box (+ margin) ---
rows, cols = np.where(valid.any(axis=1))[0], np.where(valid.any(axis=0))[0]
m = 40
mos = mos[max(rows.min()-m,0):min(rows.max()+m,H-1)+1,
          max(cols.min()-m,0):min(cols.max()+m,W-1)+1]

# --- NaN-aware block-mean downsample ---
Hc, Wc = (mos.shape[0]//FACTOR)*FACTOR, (mos.shape[1]//FACTOR)*FACTOR
mm = mos[:Hc, :Wc].reshape(Hc//FACTOR, FACTOR, Wc//FACTOR, FACTOR)
with np.errstate(invalid="ignore"):
    small = np.nanmean(mm, axis=(1, 3))

# --- encode: R = height (0 deep .. 255 shore), G = water mask ---
smin, smax = np.nanmin(small), np.nanmax(small)
water = ~np.isnan(small)
height = np.where(water, (small - smin) / (smax - smin), 1.0)
R = np.clip(height * 255, 0, 255).astype(np.uint8)
G = (water * 255).astype(np.uint8)
B = np.zeros_like(R)
Image.fromarray(np.dstack([R, G, B]), "RGB").save(os.path.normpath(OUTPNG))
print("saved", os.path.normpath(OUTPNG), small.shape[::-1])
