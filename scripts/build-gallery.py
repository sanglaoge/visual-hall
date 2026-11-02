#!/usr/bin/env python3
"""把「网页素材」源目录转成站点可用素材，并生成 assets/data/works.js + 作品清单.md。

用法：
    python3 scripts/build-gallery.py              全部重跑（已转过的会跳过）
    python3 scripts/build-gallery.py --skip-video 只处理图
    python3 scripts/build-gallery.py --force      强制重转全部

增删作品：改源目录（加/删图片、加文件夹）→ 重跑本脚本 → 提交。
需要改产品归类的，改下面的 PRODUCTS / UGC_TO_PRODUCT / ACC_TO_PRODUCT / VIDEO_TO_PRODUCT。
"""
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

SRC = os.path.expanduser("~/Downloads/B2B&B2C/网页素材")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

SKIP_DIRS = ("a+", "缩略图", "视频素材")
IMG_EXT = (".jpg", ".jpeg", ".png")
FORCE = "--force" in sys.argv
ONLY_VIDEO = "--only-video" in sys.argv

# 产品：源文件夹 -> (对外名称, 页面 key)
PRODUCTS = {
    "1-电热毯主图": ("电热毯", "electric-blanket"),
    "2-单面橡筋兔毛毯主图": ("单面橡筋兔毛毯", "rabbit"),
    "3-全涤印花绗缝被主图": ("全涤印花绗缝被", "quilt"),
    "毛巾主图-5色": ("毛巾", "towel"),
    "水洗磨毛布主图": ("水洗磨毛布", "brushed"),
    "G-沃尔玛圣诞套件-5": ("圣诞系列", "christmas"),
    "H-沃尔玛圣诞套件-8": ("圣诞系列", "christmas"),
    "tk圣诞毯主图-3": ("圣诞系列", "christmas"),
    "【数码】圣诞被套套件主图-5": ("圣诞系列", "christmas"),
    "万圣毯主图-6": ("万圣毯", "halloween"),
    "圣诞毯主图-18": ("圣诞系列", "christmas"),
    "（圆网）圣诞床单套件主图-12": ("圣诞系列", "christmas"),
}

# 只有 UGC / 辅料、没有主图的产品
EXTRA_PRODUCTS = [
    ("法拉绒毯子", "fleece"),
    ("凉感被", "cooling"),
    ("纯色四件套", "sheet-set"),
]

PRODUCT_ORDER = ["electric-blanket", "rabbit", "quilt", "towel", "brushed",
                 "christmas", "halloween", "fleece", "cooling", "sheet-set"]

UGC_TO_PRODUCT = {
    "h绗缝被": "quilt",
    "兔毛毯": "rabbit",
    "法拉绒毯子": "fleece",
    "电热毯": "electric-blanket",
    "面料特写": None,
}

ACC_TITLES = {
    "k-100% bamboo.pdf": "Bamboo 材质说明",
    "k-凉感被包装盒.pdf": "凉感被包装盒",
    "k-兔毛毯-塑料袋4070.pdf": "兔毛毯塑料袋 40×70",
    "k-电热毯纸盒包装.pdf": "电热毯纸盒包装",
    "k-纯色四件套彩卡.pdf": "纯色四件套彩卡",
    "k-绗缝被-彩卡.jpg": "绗缝被彩卡",
}
ACC_TO_PRODUCT = {
    "k-兔毛毯-塑料袋4070.pdf": "rabbit",
    "k-电热毯纸盒包装.pdf": "electric-blanket",
    "k-绗缝被-彩卡.jpg": "quilt",
    "k-凉感被包装盒.pdf": "cooling",
    "k-纯色四件套彩卡.pdf": "sheet-set",
    "k-100% bamboo.pdf": None,
}
ACC_KIND = {
    "k-凉感被包装盒.pdf": "包装盒",
    "k-电热毯纸盒包装.pdf": "包装盒",
    "k-兔毛毯-塑料袋4070.pdf": "包装",
    "k-纯色四件套彩卡.pdf": "彩卡",
    "k-绗缝被-彩卡.jpg": "彩卡",
    "k-100% bamboo.pdf": "材质说明",
}
# 已有成品实物照的辅料（源图 -> 产出名）
ACC_PHOTOS = {
    "k-电热毯纸盒包装.pdf": ("01-主图系列/新品系列/1-电热毯主图/电热毯-主图视频素材/hero_giftbox.jpg",
                        "assets/acc/photo-electric-box.webp"),
}

# 首页辅料章节的实物 / 细节图（1600px，够大屏用）
CRAFT_PHOTOS = {
    "assets/craft/giftbox.webp": (
        "01-主图系列/新品系列/1-电热毯主图/电热毯-主图视频素材/hero_giftbox.jpg", 1600, 87),
    "assets/craft/controller.webp": (
        "01-主图系列/新品系列/1-电热毯主图/电热毯-主图视频素材/controller_closeup.jpg", 1600, 86),
    "assets/craft/cert.webp": (
        "01-主图系列/新品系列/1-电热毯主图/电热毯-主图视频素材/cert_intertek.jpg", 1400, 86),
}

VIDEO_TITLES = {
    "AI视频/视频1/kingrest-1.mp4": ("梦境", "AI 生成 / 竖版", "云与熊猫的睡眠场景，偏情绪向"),
    "AI视频/视频2/kingrest-2.mp4": ("温暖居室", "AI 生成 / 竖版", "客厅、宠物与毛毯的生活感镜头"),
    "AI视频/视频3/视频3.mp4": ("兔毛毯场景", "AI 生成 / 竖版", "村落晨雾开场，落到居室暖调"),
    "代码生成视频/01-电热毯/电热毯主图视频_竖版TK_v4_9x16.mp4": ("电热毯 · TikTok 竖版", "代码生成 / 竖版", "控制器与卖点的快节奏演示"),
    "代码生成视频/01-电热毯/电热毯主图视频_v6_成片_16x9.mp4": ("电热毯 · 横版", "代码生成 / 横版", "卖点分镜：调温、定时、安全"),
    "代码生成视频/02-兔毛毯/兔毛毯主图视频_v9_成片_16x9.mp4": ("兔毛毯 · 横版", "代码生成 / 横版", "面料特写与使用场景交替"),
    "代码生成视频/02-兔毛毯/兔毛毯主图视频_v9_成片_9x16.mp4": ("兔毛毯 · 竖版", "代码生成 / 竖版", "同款逻辑为竖屏重排"),
    "代码生成视频/03-绗缝被/绗缝被主图视频_v2_成片_16x9.mp4": ("绗缝被 · 横版", "代码生成 / 横版", "印花铺陈、绗缝厚度与铺床效果"),
}
VIDEO_TO_PRODUCT = {
    "代码生成视频/01-电热毯/电热毯主图视频_竖版TK_v4_9x16.mp4": "electric-blanket",
    "代码生成视频/01-电热毯/电热毯主图视频_v6_成片_16x9.mp4": "electric-blanket",
    "代码生成视频/02-兔毛毯/兔毛毯主图视频_v9_成片_16x9.mp4": "rabbit",
    "代码生成视频/02-兔毛毯/兔毛毯主图视频_v9_成片_9x16.mp4": "rabbit",
    "代码生成视频/03-绗缝被/绗缝被主图视频_v2_成片_16x9.mp4": "quilt",
}


def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode != 0:
        print("  ! fail:", " ".join(cmd[:3]), r.stderr.decode()[:200])
    return r.returncode == 0


def fresh(out, src):
    if FORCE:
        return False
    return os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src)


def to_webp(src, out, size=1200, q=80):
    if fresh(out, src):
        return True
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return run(["cwebp", "-quiet", "-q", str(q), "-resize", str(size), "0", src, "-o", out])


def pdf_page_count(src):
    r = subprocess.run(["pdfinfo", src], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split()[1])
            except Exception:
                break
    return 1


def pdf_preview(src, out):
    """多页 PDF 取最后一页（成品面），单页取第一页。"""
    page = pdf_page_count(src)
    if fresh(out, src):
        return True
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".png"
    ok = run(["pdftoppm", "-f", str(page), "-l", str(page), "-scale-to", "1400", "-png", "-singlefile", src, tmp[:-4]])
    if not ok:
        return False
    ok = to_webp(tmp, out, 1400, 82)
    if os.path.exists(tmp):
        os.remove(tmp)
    return ok


def images_in(d):
    return sorted(
        f for f in os.listdir(d)
        if f.lower().endswith(IMG_EXT) and not f.startswith(".")
    )


def natural_key(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def build_main():
    jobs = []
    sets = {}
    covers = {}
    seq = 0
    base = os.path.join(SRC, "01-主图系列")
    for top in sorted(os.listdir(base), key=natural_key):
        p = os.path.join(base, top)
        if not os.path.isdir(p):
            continue
        folders = []
        if top in ("新品系列", "节日系列"):
            folders = [(s, os.path.join(p, s)) for s in sorted(os.listdir(p), key=natural_key)]
        else:
            folders = [(top, p)]
        for folder, path in folders:
            if folder not in PRODUCTS or not os.path.isdir(path):
                continue
            name, key = PRODUCTS[folder]
            for sub in sorted(os.listdir(path), key=natural_key):
                sp = os.path.join(path, sub)
                if not os.path.isdir(sp) or any(k in sub for k in SKIP_DIRS):
                    continue
                imgs = images_in(sp)
                if not imgs:
                    continue
                seq += 1
                wid = "m%03d" % seq
                rels = []
                for i, fn in enumerate(imgs, 1):
                    rel = "assets/main/%s/%02d.webp" % (wid, i)
                    jobs.append((os.path.join(sp, fn), os.path.join(ROOT, rel)))
                    rels.append(rel)
                sets.setdefault(key, []).append({
                    "id": wid,
                    "sub": sub,
                    "cover": rels[0],
                    "images": rels,
                    "count": len(rels),
                })
                covers[wid] = os.path.join(sp, imgs[0])
    return sets, jobs, covers


def build_orbit(covers):
    """首屏星系卡片：用原图单独转 1600px，点击放大不发虚。"""
    outdir = os.path.join(ASSETS, "orbit")
    os.makedirs(outdir, exist_ok=True)
    for wid, src in covers.items():
        out = os.path.join(outdir, wid + ".webp")
        if not fresh(out, src):
            run(["cwebp", "-quiet", "-q", "86", "-resize", "1600", "0", src, "-o", out])


def build_ugc():
    jobs = []
    items = []
    seq = 0
    base = os.path.join(SRC, "04-ugc系列")
    for sub in sorted(os.listdir(base), key=natural_key):
        p = os.path.join(base, sub)
        if not os.path.isdir(p):
            continue
        label = re.sub(r"^UGC-", "", sub)
        for fn in images_in(p):
            seq += 1
            rel = "assets/ugc/%03d.webp" % seq
            jobs.append((os.path.join(p, fn), os.path.join(ROOT, rel)))
            items.append({
                "id": "u%03d" % seq,
                "group": label,
                "product": UGC_TO_PRODUCT.get(label),
                "title": os.path.splitext(fn)[0],
                "src": rel,
            })
    return items, jobs


def build_acc():
    items = []
    base = os.path.join(SRC, "03-辅料系列")
    seq = 0
    for fn in sorted(os.listdir(base), key=natural_key):
        if fn.startswith(".") or fn not in ACC_TITLES:
            continue
        src = os.path.join(base, fn)
        seq += 1
        rel = "assets/acc/a%02d-p%d.webp" % (seq, pdf_page_count(src) if fn.lower().endswith(".pdf") else 1)
        if fn.lower().endswith(".pdf"):
            pdf_preview(src, os.path.join(ROOT, rel))
        else:
            to_webp(src, os.path.join(ROOT, rel), 1400, 82)
        photo = None
        if fn in ACC_PHOTOS:
            src_photo, out_photo = ACC_PHOTOS[fn]
            if to_webp(os.path.join(SRC, src_photo), os.path.join(ROOT, out_photo), 1200, 82):
                photo = out_photo
        items.append({
            "id": "a%02d" % seq,
            "title": ACC_TITLES[fn],
            "file": fn,
            "kind": ACC_KIND.get(fn, "印刷件"),
            "product": ACC_TO_PRODUCT.get(fn),
            "preview": photo or rel,
            "die": rel if photo else None,
            "type": "PDF" if fn.lower().endswith(".pdf") else "JPG",
        })
    return items


def build_craft_photos():
    for out_rel, (src_rel, size, q) in CRAFT_PHOTOS.items():
        to_webp(os.path.join(SRC, src_rel), os.path.join(ROOT, out_rel), size, q)


def build_videos():
    items = []
    base = os.path.join(SRC, "02-产品视频系列")
    seq = 0
    for rel_src, (title, tag, note) in VIDEO_TITLES.items():
        src = os.path.join(base, rel_src)
        if not os.path.exists(src):
            print("  ! missing", src)
            continue
        seq += 1
        vid = "v%02d" % seq
        out_mp4 = os.path.join(ASSETS, "video", vid + ".mp4")
        out_poster = os.path.join(ASSETS, "video", vid + ".webp")
        os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
        if not fresh(out_mp4, src):
            print("  video %s -> %s" % (rel_src, vid))
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                 "-vf", "scale='min(1280,iw)':-2",
                 "-c:v", "libx264", "-crf", "27", "-preset", "slow",
                 "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
                 out_mp4])
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-show_entries", "format=duration",
             "-of", "json", src], capture_output=True, text=True)
        try:
            info = json.loads(probe.stdout)
            w = int(info["streams"][0]["width"])
            h = int(info["streams"][0]["height"])
            dur = float(info["format"]["duration"])
        except Exception:
            w = h = 0
            dur = 0
        if not fresh(out_poster, src):
            run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", src,
                 "-frames:v", "1", "-vf", "scale=900:-2", "-q:v", "3", out_poster.replace(".webp", ".jpg")])
            jpg = out_poster.replace(".webp", ".jpg")
            if os.path.exists(jpg):
                run(["cwebp", "-quiet", "-q", "80", jpg, "-o", out_poster])
                os.remove(jpg)
        items.append({
            "id": vid,
            "title": title,
            "tag": tag,
            "note": note,
            "product": VIDEO_TO_PRODUCT.get(rel_src),
            "src": "assets/video/%s.mp4" % vid,
            "poster": "assets/video/%s.webp" % vid,
            "long": "竖" if h > w else "横",
            "dur": round(dur, 1),
        })
    return items


def main():
    do_video = not ONLY_VIDEO or ONLY_VIDEO
    sets = {}
    ugc, acc, videos = [], [], []
    jobs = []
    if not ONLY_VIDEO:
        sets, jobs, covers = build_main()
        ugc, ugc_jobs = build_ugc()
        jobs += ugc_jobs
        acc = build_acc()
        build_craft_photos()
        print("图片待转 %d" % len(jobs))
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda j: to_webp(j[0], j[1]), jobs))
        build_orbit(covers)
        build_craft_photos()
    videos = build_videos()

    names = {k: n for f, (n, k) in PRODUCTS.items()}
    products = []
    for key in PRODUCT_ORDER:
        item = {
            "key": key,
            "name": names.get(key) or dict((k, n) for n, k in EXTRA_PRODUCTS).get(key),
            "sets": sets.get(key, []),
            "videos": [v["id"] for v in videos if v["product"] == key],
            "ugc": [u["id"] for u in ugc if u["product"] == key],
            "acc": [a["id"] for a in acc if a["product"] == key],
        }
        if item["name"]:
            products.append(item)

    hero = []
    for key in ["electric-blanket", "rabbit", "quilt", "towel", "brushed", "christmas", "halloween"]:
        hero += [s["cover"] for s in sets.get(key, [])]

    data = {
        "products": products,
        "videos": videos,
        "ugc": ugc,
        "acc": acc,
        "hero": hero,
    }
    os.makedirs(os.path.join(ASSETS, "data"), exist_ok=True)
    with open(os.path.join(ASSETS, "data", "works.js"), "w") as f:
        f.write("window.WORKS = ")
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write(";\n")
    print("products:", [(p["name"], len(p["sets"]), len(p["videos"]), len(p["ugc"]), len(p["acc"])) for p in products])
    print("sets=%d ugc=%d acc=%d videos=%d hero=%d" % (
        sum(len(p["sets"]) for p in products), len(ugc), len(acc), len(videos), len(hero)))

    write_manifest(products, videos, ugc, acc)


def write_manifest(products, videos, ugc, acc):
    L = ["# 作品清单", "",
         "> 本文件由 `scripts/build-gallery.py` 依据源目录自动生成，手改会被覆盖。",
         "> 源目录：`~/Downloads/B2B&B2C/网页素材/`", "",
         "## 按产品", "",
         "| 产品 | 主图套组 | 主图张数 | 视频 | 买家秀 | 辅料 |",
         "|---|---|---|---|---|---|"]
    for p in products:
        L.append("| %s | %d | %d | %d | %d | %d |" % (
            p["name"], len(p["sets"]), sum(s["count"] for s in p["sets"]),
            len(p["videos"]), len(p["ugc"]), len(p["acc"])))
    L += ["", "## 主图明细", "", "| 产品 | SKU / 颜色 | 张数 |", "|---|---|---|"]
    for p in products:
        for s in p["sets"]:
            L.append("| %s | %s | %d |" % (p["name"], s["sub"], s["count"]))
    L += ["", "## 视频", "", "| 名称 | 规格 | 时长 | 归属 |", "|---|---|---|---|"]
    pmap = {p["key"]: p["name"] for p in products}
    for v in videos:
        L.append("| %s | %s | %ss | %s |" % (v["title"], v["tag"], v["dur"], pmap.get(v["product"], "—")))
    L += ["", "## 辅料", "", "| 名称 | 类别 | 格式 | 归属 |", "|---|---|---|---|"]
    for a in acc:
        L.append("| %s | %s | %s | %s |" % (a["title"], a["kind"], a["type"], pmap.get(a["product"], "—")))
    L += ["", "## 买家秀", ""]
    counts = {}
    for u in ugc:
        counts[u["group"]] = counts.get(u["group"], 0) + 1
    for k, v in counts.items():
        L.append("- %s：%d 张" % (k, v))
    with open(os.path.join(ROOT, "作品清单.md"), "w") as f:
        f.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
