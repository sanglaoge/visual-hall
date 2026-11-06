#!/usr/bin/env python3
"""从 assets/data/works.js 生成 作品清单.md。"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = open(os.path.join(ROOT, "assets", "data", "works.js")).read()
W = json.loads(re.sub(r"^window\.WORKS\s*=\s*|\s*;\s*$", "", raw))

L = ["# 作品清单", "", "> 本文件由 `scripts/manifest.py` 依据 `assets/data/works.js` 生成，手改会被覆盖。", "",
     "## 品牌与年份", "", "| 品牌 | 年份 | 套 | 张 | 辅料 |", "|---|---|---|---|---|"]
amap = {}
for a in W["acc"]:
    amap[a.get("brand", "—")] = amap.get(a.get("brand", "—"), 0) + 1
for b in W["brands"]:
    L.append("| %s | %s | %d | %d | %d |" % (
        b["name"], b.get("year", ""), b["count"], b["images"], amap.get(b["name"], 0)))

L += ["", "## 2025 品类", "", "| 品牌 | 品类 | 套 | 张 |", "|---|---|---|---|"]
for b in W["brands"]:
    if b.get("year") != 2025:
        continue
    for c in b["categories"]:
        ss = [s for s in b["sets"] if s["cat"] == c["name"]]
        L.append("| %s | %s | %d | %d |" % (b["name"], c["name"], len(ss), sum(s["count"] for s in ss)))

L += ["", "## 2026 品类", "", "| 品类 | 套 | 张 |", "|---|---|---|"]
for p in W["products"]:
    L.append("| %s | %d | %d |" % (p["name"], len(p["sets"]), sum(s["count"] for s in p["sets"])))

L += ["", "## 2025 主图明细", "", "| 品牌 | 品类 | 套名 | 张数 |", "|---|---|---|---|"]
for b in W["brands"]:
    if b.get("year") != 2025:
        continue
    for s in b["sets"]:
        L.append("| %s | %s | %s | %d |" % (b["name"], s["cat"], s["sku"], s["count"]))

L += ["", "## 2026 主图明细", "", "| 品类 | 套名 | 张数 |", "|---|---|---|"]
for p in W["products"]:
    for s in p["sets"]:
        L.append("| %s | %s | %d |" % (p["name"], s["sub"], s["count"]))

L += ["", "## 辅料", "", "| 品牌 | 件数 |", "|---|---|"]
for k, v in amap.items():
    L.append("| %s | %d |" % (k, v))

open(os.path.join(ROOT, "作品清单.md"), "w").write("\n".join(L) + "\n")
print("ok", len(W["brands"]), "brands")
