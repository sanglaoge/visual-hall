#!/usr/bin/env python3
"""静态检查：本地引用、锚点、query 目标、works.js 资源。"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

pages = ["index.html", "library.html", "brand.html", "product.html", "videos.html",
         "accessories.html", "ugc.html"] + glob.glob("review/*.html") + glob.glob("prototypes/*/index.html")

missing = []
anchors = []
refs = 0
for p in pages:
    if not os.path.exists(p):
        continue
    html = open(p).read()
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    for m in re.findall(r'(?:src|href|poster)="([^"]+)"', html):
        if m.startswith(("http://", "https://", "mailto:", "data:", "javascript:")):
            continue
        if "+" in m or "${" in m:
            continue
        if m.startswith("#"):
            if m[1:] and m[1:] not in ids:
                anchors.append((p, m))
            continue
        path = m.split("?")[0].split("#")[0]
        if not path:
            continue
        full = os.path.normpath(os.path.join(os.path.dirname(p), path))
        refs += 1
        if not os.path.exists(full):
            missing.append((p, m, full))

# query targets
brands = {"gogreen", "hitime", "kingrest", "own"}
raw = open("assets/data/works.js").read()
W = json.loads(re.sub(r"^window\.WORKS\s*=\s*|\s*;\s*$", "", raw))
products = {x["key"] for x in W["products"]}
bad_q = []
for p in pages:
    html = open(p).read()
    for m in re.findall(r'href="(brand\.html\?b=|product\.html\?p=)([^"#]+)', html):
        kind, val = m
        if "'" in val or "+" in val or "${" in val:
            continue
        if kind.startswith("brand") and val not in brands:
            bad_q.append((p, "brand", val))
        if kind.startswith("product") and val not in products:
            bad_q.append((p, "product", val))

# works.js assets
asset_missing = []
def chk(path):
    if path and not os.path.exists(path):
        asset_missing.append(path)
for b in W["brands"]:
    for s in b.get("sets", []):
        chk(s.get("cover"))
        for i in s.get("images", []): chk(i)
for a in W["acc"]:
    for i in a.get("images", []): chk(i)
    chk(a.get("preview"))
for v in W["videos"]:
    chk(v.get("src")); chk(v.get("poster"))
for u in W["ugc"]:
    chk(u.get("src"))

print(f"页面 {len(pages)}｜本地引用 {refs}｜缺失 {len(missing)}｜坏锚点 {len(anchors)}｜坏 query {len(bad_q)}｜works 资源缺失 {len(asset_missing)}")
for x in missing[:15]: print("  缺文件", x)
for x in anchors[:15]: print("  坏锚点", x)
for x in bad_q[:15]: print("  坏 query", x)
for x in asset_missing[:15]: print("  缺资源", x)
raise SystemExit(1 if (missing or anchors or bad_q or asset_missing) else 0)
