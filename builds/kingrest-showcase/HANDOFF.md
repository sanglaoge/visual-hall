# HANDOFF — 新会话继续开发提示词（2026-10-16）

> 把下面整段提示词复制到新会话即可继续。工作区不变时，记忆也会自动带上大部分背景。

---

## 提示词（复制这段）

我在 ~/valve/视觉厅/ 有一个进行中的项目：Kingrest 家纺产品展示站（纯静态 HTML/CSS/JS），目标是 100% 复刻 getartcraft.com 的交互与手感。已完成 v4.1，现在继续迭代。

**先读这些文件恢复上下文**：
- 视觉厅/builds/kingrest-showcase/index.html（全部代码）
- 视觉厅/builds/kingrest-showcase/README.md（预览命令 + 内容增删指南）
- 视觉厅/builds/kingrest-showcase/BRIEF.md（设计简报 + v3/v4 修订记录）
- 视觉厅/builds/kingrest-showcase/HANDOFF.md（本文件，含技术坑清单）

**本地预览**：node ~/.zcode/skills/scroll-craft/scripts/serve.mjs --root builds/kingrest-showcase --port 4500，浏览器开 http://localhost:4500

**当前已实现（不要回退）**：
1. 零钉住纯文档流架构（约 8.6 屏）——用户明确判定钉住段=“滑不动”，任何滚动时页面必须可见移动
2. 首屏漩涡：12 张无边框产品卡骑 4 条同心环逆时针公转（rAF 极坐标），呼吸缩放 ±5%，深度遮挡，半透明已改回 100% 不透明，无描边
3. 滚动驱动旋转：Lenis velocity → boost，下滑漩涡加速、上滑卡片倒转回位（用户最喜欢的效果，保留）
4. 黑色螺旋线条已按用户要求删除（只剩细同心环+渐变弧线）
5. 双主题：默认浅色暖白，右上角太阳/月亮切换深色，img[data-light] 双版本 logo 由 JS 换 src
6. 真 logo：hero 中心 gogreen（上）+ Kingrest（下）同高双 logo；左上角 mark 和收板也用真 logo（assets/logo-*.png，透明底双版本；**gogreen 待用户重新提供 PNG 替换**，放 assets/ 改名 logo-gogreen-on-light/dark.png 即可）
7. 章节词 rail：scrub 三态——静息**隐藏**（opacity 0，用户要求划到才出现）→ 随滚动从竖排贴刻度尺旋转+字母组装成右上横排巨字 → 过章弱化 opacity .22 收进顶部窄带（不与大标题重叠）；-webkit-text-stroke 4px 背景色描边保可读；词可点击跳章
8. 产品/辅料：artcraft 式发丝线网格（gap:1px 技巧），四主题分组，craft 章节牛皮纸底
9. 传送带：产品类型词轮播，蓝色菱形 #4d7cff，间距 56px
10. 蓝色百分比刻度尺（mono 数字 0-100）、 Films 三条竖版视频入视口自动播放

**待办**：
1. ~~用户重新提供 gogreen PNG~~ ✅ 2026-10-16 已完成：用户给了 `~/Downloads/gogreen 横板logo.pdf`（+带®的 -r 版，已采用带®版做正稿）。pdftocairo -transp 直接渲出真透明，深色版把低饱和暗像素翻成米白 #f2ede3（绿保留），存 assets/logo-gogreen-on-light/dark.png（1035×180，各 ~50KB）。注意：gogreen 紧裁横版 5.75:1，CSS 高度必须只有 Kingrest 的一半（clamp 18-26px）两 logo 才视觉等高等宽；废弃的旧 gogreen webp 已移出 assets
2. 用户逐屏测试反馈（重点：首屏漩涡手感、标题飞行、网格排版）
3. Phase 2：用户挑选新增素材/主题扩充
4. 部署 GitHub Pages（提醒：repo public 则产品图公开）

**技术坑（血泪，别再踩）**：
- 引擎 .sc-stage 是 sticky+100svh，项目 CSS 不能覆盖其 position/height
- Playwright hover 对持续动画元素报 not-stable，用坐标级 mouse.move
- IAB 后台标签 rAF 被暂停（自转/Lenis 全停），测试要聚焦标签页或用 headless Chrome（playwright-core 已装在 build 目录，channel:'chrome'）
- 零幕页面 harness 只拍一帧，走查需自己等距截图 + ffmpeg tile 拼 sheet
- macOS sips 不支持 webp 编码，用 Pillow；Pillow 存带 alpha 的 logo 用 PNG（webp 曾丢 alpha）
- 透明度公式：lum 归一化 0-1 后用 (1-lum)*255*k，别写成 (255-lum)
- scroll-craft harness 对零钉住页面会只拍一帧属正常

**用户偏好（重要）**：桑老哥要极简汇报+自己真机测试；改前先说改哪、改完带截图证据；一次别改太多；他发火是因为回归，所以每轮改动必须先跑桌面+手机两套截图自查再交。

---

## 技术坑清单（备份，同上）
见提示词内“技术坑”部分。
