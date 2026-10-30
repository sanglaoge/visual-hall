# artcraft 首屏（Hero）逆向规格 — 2026-10-16 实测+源码挖掘

来源：IAB 实开逐屏采样 + `_next/static/chunks/223tafwc4nxdm.js`（galaxy 源码，含全部可调参数默认值）。
本地留档：/tmp/acbundle/galaxy.js（美化版）。以下数值均为官网默认值。

## 1. 导航（已复刻 2026-10-16）

- `sticky top-0 z-50`，高 48px，底边 1px hairline，背景 `bg/95 + backdrop-blur`
- 左簇：logo 格（px-4/5，右侧分隔线，logo 高 24px）→ 标签行（Home/Image/Video/Resources▾/Download/Support/Craft Apps）
- 标签样式：Geist Mono 11px/500 大写，px-2.5；内层 span hover 变"反色药丸"（bg=ink、字=bg）；当前页常驻药丸
- 右簇：Pricing / Discord 图标格 / 主题钮格 / Launch App CTA（48px 高黑底药丸）

## 2. Hero 结构

- 容器：`min-h calc(100svh - 48px)`；canvas（WebGL, dpr≤1.5, fov 30，1 世界单位≈1px）absolute inset-0 **pointer-events:none**；外层 div 接 pointer 事件
- 中心覆盖层：z-40，**pointer-events-none**（仅 CTA 行 auto），flex 列 `items-center justify-center`——**像素级垂直居中**
- 中心栈（上→下）：
  1. 大字标 95px 高，逐字 `<span class="wm-letter">`（ARTCRAFT 首字母换成 SVG 图标）
  2. 字标后两块板：① `backdrop-filter: blur(12px)` 透明板（无底色，比字标 x ±6%、y ±34%）② HeroScrim 径向渐变 `radial-gradient(closest-side, bg 85%, transparent)`
  3. h1（display 3xl，tracking -0.03em，短语用衬线斜体）「Capable tools *for artists.*」
  4. 正文两行（max-w-md，text-lg，muted）
  5. 双 CTA 48px（主=ink 底反字+图标，副=bg/ink 描边）
  6. mono 小字行（hud-label, faint）
- 字标逐字 baseX/baseDocY 被导出给 rail 模块：**下滑时中心字标的字母飞到右缘变成竖排章节点**（isHero 条目）——用户记忆"logo 向右变成标题"即此

## 3. 卡片系统（galaxy，非同心环！）

- **6 条阿基米德螺旋臂**（r = c·θ），卡片轮流发到臂上（card i: arm = i%6, slot = i/6）
- turns/arm = 1.05 圈；外半径 rMax = 0.7 × 视口半对角线；出生半径 8% rMax（字标周围的"星云口袋"）
- **传送带式生死**：卡片在中心出生（小、方、模糊、淡入），沿臂向外走，出屏死亡（无退场淡出）。idleSpeed = 0.57 程/分钟（≈105s 走完全程）
- **滚动耦合**：`progress = idleP + scrollY × 0.2 / 1000`——**位置绑定、可逆**（滑 1000px = 0.2 程外流；上滑倒流），不是速度型
- 全局自转 -50°/min（逆时针；臂+刻度+卡片路径一起转，卡片内容保持水平）
- 数量：默认 64@1.65Mpx，按视口面积缩放（1440×900≈50 张，含屏外）；手机档（<0.6Mpx）3 臂/14 卡/rMax 0.8
- 尺寸：高帽 = clamp(25%vh, 70, 340)；内圈帽 45%（出生小）随程长到全帽；再受"最近邻间隙×密度 0.82"限制（永不碰撞）
- 形态：出生方形 → 30% 程变 16:9；圆角 10px；发丝边框（alpha 0.22）
- 抖动：偏离臂位 6px @0.25Hz（两个不同频正弦，逐卡黄金角错相）
- 素材是**视频纹理**（循环、错开起播、屏外 pause、只播 renderOrder 前 8）

## 4. 指针交互（galaxyPointer）

- 鼠标场半径 320px：场内卡片被**拉向鼠标 8px**（高斯衰减）+ 表面朝鼠标隆起（mouseWarp 200px，顶点着色器高斯凸起=用户说的"扭曲变形"）
- 悬停（hold）：卡片运动刹车（tau 0.15s），**全系统跟着减速**（restTau 1s，"流动被手攥住"的感觉）；被悬停卡清晰化（blur/warp/色散全清）
- 邻让：悬停卡周围卡片自动缩小让位（0.98×(2d−U)）
- 点击：①卡片表面点击冲击波（环从点击点扩散 0.75s，位移 20px）②**3× 放大切换**（boostScale，ease 0.18s，再点或移开复原）③色散涟漪从点击点扩散（900px/s，1.8s 寿命，扫过的卡闪色散+22px 隆起）
- 色散：卡边缘色差 0.019；鼠标扫过+0.032（3/s 衰减）

## 5. 背景线条层（"漩涡"）

- 6 条臂的引导线（发丝 2px，alpha 0.15）+ 虚线构造圆（0.56 rMax，段距≈14px）+ 每臂外半段 16 个径向刻度（±6px，alpha 0.3）
- **彗星脉冲**：每臂 3 个，沿线向外跑（0.19 周期/s），黄金角错相永不齐闪；锐头长尾；峰值处线膨胀到 3.5px、alpha +0.72
- 颜色：浅色主题=灰脉冲（ink 混 62%，无彩色）；深色主题=品牌蓝 #2d81ff + 每臂色相偏移
- **线条本身静止时也在动**（彗星流动）；整层随系统 -50°/min 旋转、hold 时减速
- 入场：4s 揭示波从字标扫向外缘（3× 起速 burst 2.5s 缓落），后跟色散耀斑二次扫场

## 6. 咱们的复刻映射（DOM/CSS 近似，无 WebGL）

| 官网 | 咱们方案 |
|---|---|
| WebGL 卡片网格（弯曲/隆起/色散/模糊） | DOM 卡片：呼吸缩放近似弯曲；hover 时 `filter: blur(0)+scale 2~3`；出生模糊用 `filter: blur(px)`+opacity 淡入；色散免（成本高收益低，或 CSS `filter` 双影近似） |
| 鼠标隆起扭曲 | hover 卡 `transform: rotate(小角度随鼠标方位) + scale`；邻卡拉近位移可做（rAF 里算高斯） |
| 螺旋臂+彗星 | SVG：6 条阿基米德螺旋 path + `stroke-dasharray` 动画做彗星（每臂 3 个 dash 段外流），整组 CSS rotate -50°/min |
| 传送带+滚动耦合 | rAF：progress = idle + scrollY×0.2/1000，θ 插值出每卡位置（ births at center） |
| 点击 3× 切换 | 点击卡 `scale:3` 过渡 0.18s，再点/移出复原（替代现 focus overlay，或保留 overlay 做大图） |
| 中心 blur 板 | `backdrop-filter: blur(12px)` 透明板 + 径向 scrim，尺寸比内容 y±34% x±6% |

## 7. 待拍板

1. 中心内容方案（详见汇报）：推荐 KINGREST 大字标 + 一行 h1 + 一行文 + 双 CTA + mono 小字行
2. 卡片数量：官网 1440 下约 50（含屏外）；咱们素材 14 图，建议先 24-30 张循环用图
3. 卡片素材是否换成 3 条竖版视频里的帧（官网是视频卡）
4. 每章独立标题/文案重写（现在 Collection/Craft/Film 太雷同）
