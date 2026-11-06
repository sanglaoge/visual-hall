# 视觉厅

桑老哥的视觉作品集（近一年电商视觉产出：产品主图、主图视频、UGC 买家秀等）。
两个目的：① 记录自己的工作点滴 ② 分享给领导，让产出可见。
长期维护型项目——会持续增删内容，不是一次做完就完事。

- 2026-10-30 从 `~/valve/热点日报/产品展示站/` 搬出独立建库（原名产品展示站，同日定名视觉厅）
- 2026-11-02 改成「产品优先」结构：总览（随机主图 + 产品分类）→ 产品页（主图整套 + 视频 + 买家秀 + 辅料），另设视频/辅料/买家秀三个专项页；Kingrest 站降为延伸阅读
- 2026-11-06 改「品牌优先」：全部作品 → GOGREEN / HITIME / KINGREST / 2026 新品 → 品类 → 套图；新增 `brand.html`，`library.html` 改为品牌墙
- 溯源：源于日报 2026-10-14 发现的 scroll-craft skill；首个成品是 Kingrest 家纺品牌站
- 进度、决策、待办统一记在 `index.md`

## 目录约定

| 目录/文件 | 用途 |
|---|---|
| `index.html` | 首页：scroll-craft 滚动站（星系首屏 + 产品章节 + 辅料 + 视频），首页即门面 |
| `library.html` | 全部作品：品牌墙（2025 三家 + 2026 新品），点进品牌页 |
| `brand.html` | 品牌页，按 `?b=key` 渲染该品牌的品类筛选、整套主图与辅料 |
| `index-v1.html` | 旧版预览页（临时，待删） |
| `product.html` | 2026 产品页，按 `?p=key` 渲染该品类的整套主图/视频/买家秀/辅料 |
| `videos.html` `accessories.html` `ugc.html` | 三个专项页 |
| `rooms/` | 旧四厅页面，已被上面替代（待删） |
| `builds/` | 深度案例（当前 `kingrest-showcase/`，scroll-craft 独立站） |
| `assets/` | 站点产物：`main/` `video/` `ugc/` `acc/` `orbit/` + `data/works.js`（brands / sets2025 / products / acc）+ 共用 `gallery.css/js` + `scrollcraft.css/js`（引擎，勿按项目改） |
| `scripts/build-gallery.py` | 源素材 → 上站产物，幂等可重跑；⚠️ 旧目录路径，待重写 |
| `scripts/manifest.py` | 读 `assets/data/works.js` 生成 `作品清单.md` |
| `素材/` | 收料口（当前空；原片仍在本机 Downloads，见下） |
| `作品清单.md` | 作品台账，脚本生成，勿手改 |
| `FINGERPRINTS.md` | scroll-craft build 登记表 |

素材源目录：`~/Downloads/B2B&B2C/网页素材/`（2025 按品牌 GOGREEN / HITIME / KINGREST / 辅料系列，2026 按类型 01-主图 / 02-视频 / 03-辅料 / 04-ugc，约 3.2G，不入库）

> ⚠️ 2026-11-06 起源目录改成「年度/品牌/品类」结构，`scripts/build-gallery.py` 还写着旧路径，跑之前先改；2025 的导入与合并暂用 `网页素材/_筛选/` 里的临时脚本。

## 常用命令

- 本地预览：`node ~/.zcode/skills/scroll-craft/scripts/serve.mjs --root . --port 4500`
- 重新生成作品清单：`python3 scripts/manifest.py`（读 `assets/data/works.js`）
- 重新生成素材与数据：`python3 scripts/build-gallery.py`（⚠️ 旧目录路径，待按年度结构重写）
- 发布：`git commit + push` → GitHub Pages 自动部署（约 1 分钟生效）

## 上线

- 地址：`https://sanglaoge.github.io/visual-hall/`（仓库 `sanglaoge/visual-hall`，main 分支根目录发布）
- 暂时公开访问；页面与 `robots.txt` 已设 `noindex`，不被搜索引擎收录
- ⚠️ 公开即全网可看，品牌素材（含买家秀）上线前须过一遍敏感信息检查

## 容量红线（GitHub Pages 免费版）

- 单文件 < 100MB（硬限）｜整站 < 1GB｜月流量 100GB（软限）
- 视频按桑老哥口径控制：每条几十秒、几十 MB，只放几条；超限的改外链嵌入
- 当前实测：站点资产约 443MB（主图 293 / 首屏 78 / 视频 59 / 辅料 6），单文件最大 24MB（视频 v03）
- 图片长边 1200px webp q80；首屏 orbit 1600px webp q86；视频 1280 内 H.264 CRF27（脚本已固化）

## 工作流

1. 桑老哥把新素材丢进源目录的分类文件夹（命名沿用现有格式）
2. 跑 `python3 scripts/build-gallery.py`：转 webp/mp4、刷新 `assets/data/works.js` 与 `作品清单.md`
3. 本地起服务预览（命令见「常用命令」），看四个厅的排布
4. 桑老哥点头后 `git commit + push`，Pages 自动发布（约 1 分钟生效）

## 母版规则（2026-11-02 定）

- `main` 分支 + `v1-master` tag = 当前母版，不再直接改
- 后续改版：新建 `wip/日期-主题` 分支（或复制目录）改，满意后再合并到 `main` 发布
- 新增素材先补源目录，再跑脚本；母版只做紧急修复，日常实验都在副本

## 铁律

- 未经桑老哥拍板，不擅自删作品、不擅自改公开范围
- 元数据不猜：产品名/SKU 沿用源目录文件夹名；平台与转化数据没有就不写，不编
- 对外名称用「视觉厅」，不出现「桑老哥」等人设昵称
