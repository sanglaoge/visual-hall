import json, html
G=json.load(open('assets/data/craft-groups.json'))
CAP={
 'craft-giftbox':('电热毯礼盒','礼盒 · 控制器'),'craft-cert':('Intertek 认证','检测报告'),
 'a03':('凉感被包装盒','包装盒'),'a05':('纯色四件套彩卡','彩卡'),'a26-001':('凉感被洗标','品牌标 · 水洗标'),'a06':('绗缝被彩卡','彩卡'),
 'a25-002':('防水枕套包装','全棉汗布 · 2pack'),'a25-060':('万圣毯彩卡','色号'),'a25-055':('飞机盒刀版','结构'),'a25-028':('儿童套件彩卡','21×15.3'),'a25-007':('竹棉枕套包装','2pack'),'a25-061':('圣诞彩卡','色号'),'a25-034':('圣诞贴纸 3','贴纸'),'a25-032':('圣诞贴纸 1','贴纸'),
 'a25-069':('狗垫彩卡','18×25'),'a25-081':('床笠彩卡','30×24'),'a25-074':('竹涤套件彩卡','彩卡'),'a25-082':('毛巾彩卡','22×16'),'a25-077':('贴纸 02','贴纸'),'a25-068':('床桥彩卡','14.2×14.2'),'a25-076':('贴纸 01','贴纸'),'a25-085':('被芯贴纸','贴纸'),
 'a25-093':('套件包装 01','印刷稿'),'a25-098':('枕套彩卡 4pack','25×19'),'a25-094':('套件包装 02','印刷稿'),'a25-095':('套件包装 03','印刷稿'),'a25-096':('套件包装 04','印刷稿'),'a25-099':('枕头彩卡','22×16'),'a25-100':('医院床笠彩卡','彩卡'),'a25-101':('毛巾彩卡','16×22')}
BIG={'2026':'craft-giftbox','GOGREEN':'a25-002','HITIME':'a25-081','KINGREST':'a25-093'}
WIDE={'2026':'a06','GOGREEN':'a25-028','HITIME':'a25-074','KINGREST':'a25-098'}
LOGO={'GOGREEN':'../../assets/brand-logos/gogreen-horizontal.png','HITIME':'../../assets/brand-logos/Hitime-primary.png','KINGREST':'../../assets/brand-logos/Kingrest-dark.png'}
def e(x): return html.escape(x,quote=True)
def t(x): return CAP.get(x['id'],(x['title'],''))[0]
def s(x): return CAP.get(x['id'],(x['title'],''))[1]
def im(x): return '../../'+x['src']
def head(g):
    if g in LOGO: return f'<img class="logo" src="{LOGO[g]}" alt="{g}">'
    return f'<span class="wordmark">{g if g!="2026" else "2026 新品"}</span>'
# A
A=[]
for g in ['2026','GOGREEN','HITIME','KINGREST']:
    items=G[g]; bigid=BIG[g]; wideid=WIDE[g]
    ordered=[next(x for x in items if x['id']==bigid)]+[x for x in items if x['id'] not in (bigid,wideid)]+[next(x for x in items if x['id']==wideid)]
    flip=' flip' if g in ('GOGREEN','KINGREST') else ''
    A.append(f'<section class="ds"><div class="dh">{head(g)}<span>{len(items)} 件</span></div><div class="grid{flip}">')
    for x in ordered:
        cls='big' if x['id']==bigid else ('wide' if x['id']==wideid else '')
        A.append(f'<figure class="card {cls}"><div class="paper"><img src="{im(x)}" alt="{e(t(x))}"></div><figcaption><b>{e(t(x))}</b><span>{e(s(x))}</span></figcaption></figure>')
    A.append('</div></section>')
A='\n'.join(A)
# B
B=[]
for g in ['2026','GOGREEN','HITIME','KINGREST']:
    B.append(f'<section class="blk"><div class="bar"><b>{g if g!="2026" else "2026 新品"}</b><span>{len(G[g])} PIECES</span></div><div class="strip">')
    for x in G[g]:
        B.append(f'<figure style="--ar:{max(.7,min(1.6,x["ar"])):.2f}"><img src="{im(x)}" alt="{e(t(x))}"><figcaption><b>{e(t(x))}</b><span>{e(s(x))}</span></figcaption></figure>')
    B.append('</div></section>')
B='\n'.join(B)
# C
C=[]
for g in ['2026','GOGREEN','HITIME','KINGREST']:
    C.append(f'<section class="spread"><aside><div class="brand">{head(g)}</div><p>{len(G[g])} 件 · 2026</p><span class="rule"></span><p class="note">包装 / 彩卡 / 洗标 / 刀版</p></aside><div class="mosaic">')
    for i,x in enumerate(G[g]):
        cls='big' if i==0 else ('wide' if i in (1,4) else '')
        C.append(f'<figure class="{cls}"><img src="{im(x)}" alt="{e(t(x))}"><figcaption>{e(t(x))}<span>{e(s(x))}</span></figcaption></figure>')
    C.append('</div></section>')
C='\n'.join(C)
BASE='''*{box-sizing:border-box}body{margin:0;background:#f2f1ee;color:#14120f;font-family:Archivo,system-ui,"PingFang SC",sans-serif}img{display:block;max-width:100%}a{color:inherit}.top{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:14px;justify-content:space-between;padding:12px 20px;background:rgba(242,241,238,.94);border-bottom:1px solid rgba(20,18,15,.16);font:500 11px/1 "Geist Mono",monospace;letter-spacing:.1em}.top a{text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:2px}.top b{font:600 14px/1 Archivo;letter-spacing:.04em}.top .sw{display:flex;gap:12px}.wrap{max-width:1320px;margin:0 auto;padding:32px 20px 80px}.kicker{font:500 10px/1 "Geist Mono";letter-spacing:.18em;color:#676157}.h1{font:600 clamp(34px,6vw,72px)/1 Archivo;letter-spacing:-.04em;margin:10px 0 0}.intro{max-width:44em;color:#676157;font-size:14px;line-height:1.9;margin:14px 0 0}.serif{font-family:"Instrument Serif",Georgia,serif;font-style:italic;font-weight:400}'''
HEAD='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet"><style>{css}</style><body>{body}</body></html>'''
def top(name): return f'<header class="top"><b>{name}</b><span class="sw"><a href="index.html">三方向</a><a href="../../index.html">回站</a></span></header>'
cssA=BASE+'''body{background:#1b1712}.top{background:#1b1712;color:#f4f1ea;border-color:rgba(244,241,234,.2)}.kicker{color:#b9a68d}.h1{color:#f4f1ea}.intro{color:#c9b9a6}.desk{background:#b3906b url(../../assets/texture-kraft.webp) center/620px repeat;background-blend-mode:multiply;color:#241a10;padding:clamp(20px,4vw,44px);margin-top:26px}.ds{padding:26px 0}.ds+.ds{border-top:1px solid rgba(36,26,16,.3)}.dh{display:flex;align-items:center;justify-content:space-between;gap:14px;margin-bottom:14px;font:400 10px/1.4 "Geist Mono";letter-spacing:.12em;color:rgba(36,26,16,.7)}.dh .logo{height:22px;width:auto}.dh .wordmark{font:600 1rem/1 Archivo;color:#241a10}.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:14px}.grid.flip{direction:rtl}.grid.flip>*{direction:ltr}.card{margin:0;grid-column:span 3;display:flex;flex-direction:column}.card.big{grid-column:span 6;grid-row:span 2}.card.wide{grid-column:span 12}.card .paper{background:#fbf8f0;display:grid;place-items:center;padding:12px;flex:1;min-height:150px;box-shadow:0 18px 30px -22px rgba(36,26,16,.9),inset 0 0 0 1px rgba(36,26,16,.08)}.card.big .paper{min-height:370px}.card.wide .paper{min-height:170px}.card img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}.card figcaption{display:flex;justify-content:space-between;gap:8px;padding:8px 2px 0;font:400 10px/1.5 "Geist Mono";color:rgba(36,26,16,.7)}.card figcaption b{font:600 12px/1.3 Archivo;color:#241a10}.card figcaption span{text-align:right}@media(max-width:860px){.card,.card.wide{grid-column:span 6}.card.big{grid-column:span 12;grid-row:auto}.card.big .paper{min-height:330px}}@media(max-width:600px){.card,.card.big,.card.wide{grid-column:span 12}.card .paper{min-height:200px}}'''
bodyA=f'''{top('方向 A · 纸样台深化')}<div class="wrap"><div class="kicker">CRAFT / DIRECTION A</div><h1 class="h1">纸样台，<span class="serif">再铺开一点。</span></h1><p class="intro">牛皮纸底、白色纸卡、大图 + 通栏 + 一组常规卡；GOGREEN / KINGREST 两段左右翻转，避免四段完全同构。</p><div class="desk">{A}</div></div>'''
open('prototypes/craft-directions/a-kraft.html','w').write(HEAD.format(title='方向 A · 纸样台深化',css=cssA,body=bodyA))
cssB=BASE+'''body{background:#eae8e2}.top{background:#eae8e2}.blk{margin-top:34px;border-top:1px solid rgba(20,18,15,.35);padding-top:12px}.bar{display:flex;justify-content:space-between;align-items:baseline;font:500 10px/1 "Geist Mono";letter-spacing:.14em;color:#676157;margin-bottom:10px}.bar b{font:600 13px/1 Archivo;color:#14120f;letter-spacing:.02em}.strip{display:flex;gap:6px;align-items:flex-start}.strip figure{flex:var(--ar) 1 0;min-width:0;margin:0}.strip img{width:100%;height:auto;display:block;border:1px solid rgba(20,18,15,.18);background:#fff}.strip figcaption{padding-top:6px;font:400 9px/1.4 "Geist Mono";color:#676157}.strip figcaption b{display:block;font:600 11px/1.3 Archivo;color:#14120f}.strip figcaption span{display:block;margin-top:2px}@media(max-width:700px){.strip{overflow-x:auto}.strip figure{flex:0 0 42vw}}'''
bodyB=f'''{top('方向 B · 样张档案')}<div class="wrap"><div class="kicker">CRAFT / DIRECTION B</div><h1 class="h1">像一册，<span class="serif">样张档案。</span></h1><p class="intro">去掉纸卡和阴影，按品牌分组，用图片自身比例铺成四条档案带；信息密度高，更像印刷厂的样张册。</p>{B}</div>'''
open('prototypes/craft-directions/b-archive.html','w').write(HEAD.format(title='方向 B · 样张档案',css=cssB,body=bodyB))
cssC=BASE+'''body{background:#11100e;color:#f4f1ea}.top{background:#11100e;color:#f4f1ea;border-color:rgba(244,241,234,.18)}.kicker{color:#a59a88}.h1{color:#f4f1ea}.intro{color:#b7ab99}.spread{display:grid;grid-template-columns:250px minmax(0,1fr);gap:clamp(20px,4vw,52px);padding:clamp(26px,4vh,44px) 0;border-top:1px solid rgba(244,241,234,.2)}.spread aside{position:sticky;top:64px;align-self:start}.spread .logo{height:26px;width:auto;filter:brightness(0) invert(1)}.spread .wordmark{font:600 clamp(24px,3.4vw,40px)/1 Archivo;letter-spacing:-.03em}.spread p{font:400 10px/1.6 "Geist Mono";letter-spacing:.12em;color:#a59a88;margin:14px 0 0}.spread .rule{display:block;height:1px;background:rgba(244,241,234,.25);margin:18px 0}.spread .note{color:#7f7566}.mosaic{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:120px;gap:8px}.mosaic figure{margin:0;position:relative;overflow:hidden;background:#191714;border:1px solid rgba(244,241,234,.12)}.mosaic figure.big{grid-column:span 2;grid-row:span 2}.mosaic figure.wide{grid-column:span 2}.mosaic img{width:100%;height:100%;object-fit:contain;background:#fbf8f0}.mosaic figcaption{position:absolute;left:0;right:0;bottom:0;padding:18px 8px 7px;background:linear-gradient(transparent,rgba(10,10,10,.82));font:600 10px/1.3 Archivo;color:#fff}.mosaic figcaption span{display:block;font:400 8px/1.4 "Geist Mono";color:rgba(255,255,255,.65);margin-top:2px}@media(max-width:800px){.spread{grid-template-columns:1fr}.spread aside{position:static}.mosaic{grid-auto-rows:90px}}'''
bodyC=f'''{top('方向 C · 品牌册页')}<div class="wrap"><div class="kicker">CRAFT / DIRECTION C</div><h1 class="h1">每个品牌，<span class="serif">一页。</span></h1><p class="intro">深色册页，左边品牌、右边大图和小图混排；更像一本品牌辅料样册，不像素材墙。</p>{C}</div>'''
open('prototypes/craft-directions/c-lookbook.html','w').write(HEAD.format(title='方向 C · 品牌册页',css=cssC,body=bodyC))
ov='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>辅料排版三方向</title><link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;700&family=Instrument+Serif:ital@0;1&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet"><style>*{box-sizing:border-box}body{margin:0;background:#f2f1ee;color:#14120f;font-family:Archivo,system-ui,"PingFang SC";padding:40px 24px}.wrap{max-width:1000px;margin:0 auto}h1{font:600 clamp(34px,6vw,62px)/1 Archivo;letter-spacing:-.04em;margin:0}.k{font:500 10px/1 "Geist Mono";letter-spacing:.18em;color:#676157}p{max-width:44em;color:#676157;line-height:1.9;font-size:14px}.list{display:grid;gap:0;margin-top:30px}a.card{display:grid;grid-template-columns:80px 1fr;gap:20px;align-items:center;padding:22px 0;border-top:1px solid rgba(20,18,15,.25);text-decoration:none;color:inherit}a.card:hover{background:#e9e5dc}a.card>b{font:600 28px/1 Archivo}a.card .t{font:600 20px/1 Archivo}a.card .d{display:block;font:400 10px/1.5 "Geist Mono";color:#676157;letter-spacing:.06em;margin-top:6px}a.card em{font:400 16px/1.6 "Instrument Serif";font-style:italic;color:#676157}</style><div class="wrap"><div class="k">CRAFT / 3 DIRECTIONS</div><h1>辅料排版，<em style="font-family:'Instrument Serif';font-style:italic;font-weight:400">三个方向。</em></h1><p>同一批 30 件辅料：2026 新品 6 件，GOGREEN / HITIME / KINGREST 各 8 件。三版都保留真实品牌资产，但组织方式不同。</p><div class="list"><a class="card" href="a-kraft.html"><b>A</b><span><span class="t">纸样台深化</span><span class="d">牛皮纸 + 纸卡 + 大图通栏；四段左右翻转</span><em>最接近你现在喜欢的那版，但更讲究。</em></span></a><a class="card" href="b-archive.html"><b>B</b><span><span class="t">样张档案</span><span class="d">去掉纸卡，按比例铺成四条档案带</span><em>信息密度最高，像印刷厂样张册。</em></span></a><a class="card" href="c-lookbook.html"><b>C</b><span><span class="t">品牌册页</span><span class="d">深色册页，左品牌右图墙</span><em>最像一本品牌辅料样册。</em></span></a></div></div></html>'''
open('prototypes/craft-directions/index.html','w').write(ov)
print('built')
