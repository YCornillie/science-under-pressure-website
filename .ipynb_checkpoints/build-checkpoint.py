#!/usr/bin/env python3
"""Build a self-contained index.html:
- embeds the real Walensee swissBATHY3D heightmap as a data URI
- injects heightmap dimensions
- generates abstract bathymetry/sonar SVG thumbnails for the project cards
Run:  python build.py
"""
import base64, os, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
assets = os.path.join(HERE, "assets")
os.makedirs(assets, exist_ok=True)
png_local = os.path.join(assets, "walensee_heightmap.png")

# The heightmap lives in assets/ (derived once from swissBATHY3D via process_bathy.py).
# This build is self-contained and does not need the raw swisstopo download.
if not os.path.exists(png_local):
    raise SystemExit(f"missing {png_local} — regenerate it with scripts/process_bathy.py")

img = Image.open(png_local)
HM_W, HM_H = img.size
with open(png_local, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
datauri = "data:image/png;base64," + b64
print(f"heightmap {HM_W}x{HM_H}, data-uri {len(datauri)//1024} KB")

logo_path = os.path.join(HERE, "logo.jpeg")
if not os.path.exists(logo_path):
    raise SystemExit(f"missing {logo_path}")
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("ascii")
logo_datauri = "data:image/jpeg;base64," + logo_b64
print(f"logo data-uri {len(logo_datauri)//1024} KB")

def thumb(seed, hue):
    """abstract sonar / bathymetry contour thumbnail."""
    import math, random
    random.seed(seed)
    W, H = 640, 360
    parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">']
    parts.append(f'''<defs>
      <linearGradient id="bg{seed}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="{hue[0]}"/><stop offset="1" stop-color="{hue[1]}"/>
      </linearGradient>
      <radialGradient id="gl{seed}" cx="{hue[3]}" cy="42%" r="70%">
        <stop offset="0" stop-color="{hue[2]}" stop-opacity=".55"/>
        <stop offset="1" stop-color="{hue[2]}" stop-opacity="0"/>
      </radialGradient>
    </defs>''')
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#bg{seed})"/>')
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#gl{seed})"/>')
    # concentric isobath-style contours around a drifting center
    cx, cy = W*(0.35+0.3*random.random()), H*(0.4+0.2*random.random())
    for i in range(9):
        rx = 40 + i*46 + random.random()*10
        ry = rx*(0.55+0.15*random.random())
        pts = []
        for a in range(0, 361, 12):
            rad = math.radians(a)
            wob = 1 + 0.10*math.sin(rad*3 + seed) + 0.06*math.sin(rad*5 + i)
            x = cx + math.cos(rad)*rx*wob
            y = cy + math.sin(rad)*ry*wob
            pts.append(f"{x:.1f},{y:.1f}")
        op = 0.10 + 0.4*(1 - i/9)
        parts.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{hue[2]}" stroke-width="1.1" opacity="{op:.2f}"/>')
    # sonar scan line + grid ticks
    parts.append(f'<line x1="0" y1="{cy:.0f}" x2="{W}" y2="{cy:.0f}" stroke="{hue[2]}" stroke-width="1" opacity=".25"/>')
    parts.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="3.5" fill="{hue[2]}"/>')
    for gx in range(0, W, 40):
        parts.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="#ffffff" stroke-width=".5" opacity=".035"/>')
    parts.append('</svg>')
    return "".join(parts)

# hue sets: [bgTop, bgBottom, accent, glowCx]
thumbs = {
    "__THUMB_A__": thumb(3, ["#0a3b3a", "#06121f", "#7ff5ec", "38%"]),  # Zürichsee teal
    "__THUMB_B__": thumb(7, ["#0b2748", "#060d1c", "#6ea8ff", "60%"]),  # Bodensee blue
    "__THUMB_C__": thumb(11, ["#123a2e", "#06140f", "#6ef2b8", "45%"]), # Walensee green
    "__THUMB_D__": thumb(17, ["#1a2352", "#070a1c", "#9d8bff", "55%"]), # Vierwaldst. indigo
}

with open(os.path.join(HERE, "_template.html"), encoding="utf-8") as f:
    html = f.read()

html = html.replace("__HEIGHTMAP_DATAURI__", datauri)
html = html.replace("__HM_W__", str(HM_W)).replace("__HM_H__", str(HM_H))
html = html.replace("__LOGO_DATAURI__", logo_datauri)
for k, v in thumbs.items():
    html = html.replace(k, v)

out = os.path.join(HERE, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", out, f"({len(html)//1024} KB)")
# sanity: no placeholders left
for token in ["__HEIGHTMAP_DATAURI__", "__HM_W__", "__HM_H__", "__LOGO_DATAURI__", "__THUMB_A__", "__THUMB_B__", "__THUMB_C__", "__THUMB_D__"]:
    if token in html:
        print("WARNING: placeholder left:", token)
