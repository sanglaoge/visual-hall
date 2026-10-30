# Kingrest · 2026 Home Collection

滚动式产品展示站（零钉住的流式架构，对齐 getartcraft.com 的交互与手感；Lenis 1.3 + GSAP SplitText，纯静态）。

## 本地预览

```bash
node /Users/sanglaoge/.zcode/skills/scroll-craft/scripts/serve.mjs --root . --port 4500
# 打开 http://localhost:4500 ；手机同 Wi-Fi 加 --lan
```

## 结构

- `index.html` 全部标记 + 页面样式/脚本（token 在 `:root`，六色两字体；`html[data-theme="light"]` 一套暖白变量）
- `scrollcraft.css` / `scrollcraft.js` 引擎文件，**不要按项目改**
- `assets/` 14 张 webp + 3 条竖版 H.264（无声轨、faststart，均 <13MB）
- `BRIEF.md` 情绪曲线/峰值/评分表 + v3 修订记录；`ARTCRAFT-HERO-SPEC.md` 官网首屏逆向规格（galaxy 参数全量）；`lab/` 三套验证截图
- 顶部导航（2026-10-16 对齐官网）：48px sticky 毛玻璃条——左簇 Kingrest(24px)+gogreen(12px) 双 logo 带分隔线，标签行（mono 11px，hover/当前反色药丸，滚动 spy 高亮），右侧主题钮；<900px 藏标签
- 首屏 = **星系系统**（对齐官网 galaxy，规格见 `ARTCRAFT-HERO-SPEC.md`）：6 臂阿基米德螺旋（手机 3 臂），28 张卡（手机 14，恒方形原比例、帽 240px）在字标口袋"出生"（小/方/模糊/淡入）沿臂外流、出屏重生；滚动位置耦合（1000px=0.2 程，可逆）；整场 −50°/min 旋转；悬停=刹车+2×+鼠标场拉拽，点击=3× 切换；臂线+虚线构造圆+**水滴形彗星**（中间鼓两头尖，JS 沿臂外流 ~130px/s，浅灰/深蓝；无十字刻度，圈距按 0.85 圈/臂 拉开≈5-6 圈）；中心=GOGREEN/&KINGREST 两排大字标（径向 scrim，磨砂板已按用户要求删除）+h1+正文+双 CTA+mono 行，整层鼠标穿透
- 桌面端 = word rail（4 词：首屏无词；章节词竖排贴右缘→右上横排巨字→过章灰堆，可点跳章）+ 蓝色百分比刻度尺
- 默认浅色暖白主题，导航右格太阳/月亮切换深色；导航左簇 gogreen(12px)+Kingrest(24px) 双 logo（gogreen 在前）

## 内容增删（改 index.html）

**产品网格**：搜 `class="grid"`（第一章）。

```html
<figure class="cell">
  <div class="ph"><img src="assets/你的图.webp" width="1400" height="1400" alt="一句话描述" loading="lazy"></div>
  <figcaption class="lab"><b>品名</b><span>材质 · 印花号 · 尺寸</span></figcaption>
</figure>
```

- 加主题组：`<div class="gcell"><span>主题名</span><span>05</span></div>`
- 删：删对应 `<figure class="cell">` 或 `.gcell` 块

**首屏轨道卡**：搜 `CARD_IMGS`（index.html 脚本内）。每张卡：

```js
["assets/图.webp", "无障碍描述"],
```

- 数量：桌面 28 / 手机 14，由 `layout()` 里的 `CARD_N` 控制；图片循环取用
- 加图：往 `CARD_IMGS` 数组加一行即可（webp，建议 ≤200KB）
- 行为（出生/速度/悬停/点击）参数都在 `frame()` 里，注释对齐 `ARTCRAFT-HERO-SPEC.md`

**视频**：改 `class="reel"` 里的 `<figure class="frame">`。

## 部署前清单（未做，等拍板）

1. 仓库若 public，产品图将公开可见
2. 视频已 <13MB，图共 ~3.5MB，GitHub Pages 无压力
3. 目录可直接作为 Pages 根（index.html 已在根部）
