#!/usr/bin/env python3
"""Homepage image pipeline: make <=1000px webp variants for heavy images.

Reads index.html, finds <img src> and poster attributes, and for any asset
wider than 1000px or heavier than 150KB writes a 1000px/q78 webp under
assets/opt/ and rewrites the homepage reference. Originals stay untouched
for product / brand / UGC pages that need the larger file.

Run from the project root: python3 scripts/optimize-home-images.py
"""
import os
import re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
OPT = os.path.join(ROOT, "assets", "opt")
MAX_W = 1000
QUALITY = 78
HEAVY_KB = 150

os.makedirs(OPT, exist_ok=True)
html = open(HTML, encoding="utf-8").read()

# src="..." and poster="..." for local assets, excluding already-optimised files
refs = re.findall(r'(?:src|poster)="(assets/(?!opt/)[^"]+)"', html)
unique = sorted(set(refs))
changed = {}

for rel in unique:
    src = os.path.join(ROOT, rel)
    if not os.path.exists(src):
        print("MISSING", rel)
        continue
    if rel.startswith("assets/brand-logos/") or rel.startswith("assets/orbit-card/"):
        continue
    if not rel.lower().endswith((".webp", ".jpg", ".jpeg", ".png")):
        continue
    im = Image.open(src)
    if im.width <= MAX_W and os.path.getsize(src) <= HEAVY_KB * 1024:
        continue
    out_rel = "assets/opt/" + rel[len("assets/"):]
    out = os.path.join(ROOT, out_rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.convert("RGB").save(out, "WEBP", quality=QUALITY, method=6)
    changed[rel] = out_rel
    before = os.path.getsize(src) // 1024
    after = os.path.getsize(out) // 1024
    print(f"{rel} {before}KB -> {out_rel} {after}KB")

for old, new in changed.items():
    html = html.replace(f'"{old}"', f'"{new}"')

open(HTML, "w", encoding="utf-8").write(html)
print(f"\n{len(changed)} files optimized")
