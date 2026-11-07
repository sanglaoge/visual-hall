#!/usr/bin/env python3
"""从 assets/data/works.js 生成 作品清单.md。"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw = open(os.path.join(ROOT, "assets", "data", "works.js")).read()
W = json.loads(re.sub(r"^window\.WORKS\s*=\s*|\s*;\s*$", "", raw))


# v3 副本：GOGREEN 选图结果 + 去掉三视图
selection_path = os.path.join(ROOT, "assets", "data", "gogreen-selection.json")
SEL = json.load(open(selection_path)) if os.path.exists(selection_path) else None
HIDE = {"a25-116", "a25-117"}

def kept_count(brand_key, s):
    if brand_key != "gogreen" or not SEL:
        return s["count"]
    ex = (SEL.get("sets", {}).get(s["id"], {}) or {}).get("exclude", [])
    return len(s["images"]) - len(ex)

def visible_sets(brand):
    rows = []
    for s in brand.get("sets", []):
        if brand["key"] == "gogreen" and (s["id"] in HIDE or kept_count(brand["key"], s) <= 0):
            continue
        rows.append((s, kept_count(brand["key"], s)))
    return rows


L = ["# 作品清单", "", "> 本文件由 `scripts/manifest.py` 依据 `assets/data/works.js` 生成，手改会被覆盖。", "", "> v3 副本：GOGREEN 按 `gogreen-selection.json` 排除图片；三视图不列入辅料。", "",
     "## 品牌与年份", "", "| 品牌 | 年份 | 套 | 张 | 辅料 |", "|---|---|---|---|---|"]
amap = {}
for a in W["acc"]:
    if a.get("kind") == "三视图":
        continue
    amap[a.get("brand", "—")] = amap.get(a.get("brand", "—"), 0) + 1
for b in W["brands"]:
    rows = visible_sets(b)
    count = len(rows) if b.get("year") == 2025 else b["count"]
    images = sum(n for _, n in rows) if b.get("year") == 2025 else b["images"]
    L.append("| %s | %s | %d | %d | %d |" % (
        b["name"], b.get("year", ""), count, images, amap.get(b["name"], 0)))

L += ["", "## 2025 品类", "", "| 品牌 | 品类 | 套 | 张 |", "|---|---|---|---|"]
for b in W["brands"]:
    if b.get("year") != 2025:
        continue
    for c in b["categories"]:
        ss = [(s, n) for s, n in visible_sets(b) if s["cat"] == c["name"]]
        L.append("| %s | %s | %d | %d |" % (b["name"], c["name"], len(ss), sum(n for _, n in ss)))

L += ["", "## 2026 品类", "", "| 品类 | 套 | 张 |", "|---|---|---|"]
for p in W["products"]:
    L.append("| %s | %d | %d |" % (p["name"], len(p["sets"]), sum(s["count"] for s in p["sets"])))

L += ["", "## 2025 主图明细", "", "| 品牌 | 品类 | 套名 | 张数 |", "|---|---|---|---|"]
for b in W["brands"]:
    if b.get("year") != 2025:
        continue
    for s, n in visible_sets(b):
        L.append("| %s | %s | %s | %d |" % (b["name"], s["cat"], s["sku"], n))

L += ["", "## 2026 主图明细", "", "| 品类 | 套名 | 张数 |", "|---|---|---|"]
for p in W["products"]:
    for s in p["sets"]:
        L.append("| %s | %s | %d |" % (p["name"], s["sub"], s["count"]))

L += ["", "## 辅料", "", "| 品牌 | 件数 |", "|---|---|"]
for k, v in amap.items():
    L.append("| %s | %d |" % (k, v))

open(os.path.join(ROOT, "作品清单.md"), "w").write("\n".join(L) + "\n")
print("ok", len(W["brands"]), "brands")
