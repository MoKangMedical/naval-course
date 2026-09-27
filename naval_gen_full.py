#!/usr/bin/env python3
"""Merge data files and generate all 100 course pages"""
import os, json

FRONTEND = "/var/www/kangboacademy/frontend"
OUT_DIR = os.path.join(FRONTEND, "naval-courses")
AUDIO_DIR = os.path.join(FRONTEND, "audio", "naval")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Phase definitions
PHASES = [
    {"num":1,"name":"财富创造基础","icon":"💰","desc":"理解财富的本质、专长、杠杆——纳瓦尔财富哲学的完整基础"},
    {"num":2,"name":"判断力与决策","icon":"🧠","desc":"清晰思考、心智模型、认知偏差——做出更好的决策"},
    {"num":3,"name":"幸福与内在平静","icon":"😌","desc":"幸福是一种技能。减少欲望、练习冥想、活在当下"},
    {"num":4,"name":"自我修炼","icon":"💪","desc":"健康、习惯、时间管理——成为更好的自己"},
    {"num":5,"name":"科技与创业","icon":"🚀","desc":"从0到1、增长黑客、天使投资——科技创业者的核心知识"},
    {"num":6,"name":"经济学思维","icon":"📊","desc":"微观、宏观、博弈论——用经济学眼光看世界"},
    {"num":7,"name":"投资智慧","icon":"💎","desc":"价值投资、资产配置、风险管理——建立你的财富系统"},
    {"num":8,"name":"阅读与学习","icon":"📖","desc":"元学习、知识管理、终身学习——学会如何学习"},
    {"num":9,"name":"关系与自由","icon":"🤝","desc":"长期关系、信任、自由——设计你想要的人生"},
    {"num":10,"name":"东西方哲学融合","icon":"🏛️","desc":"斯多葛、佛教、道家——搭建你的个人哲学体系"},
]

# Phase colors
PHASE_COLORS = {
    1: ("#f59e0b", "rgba(245,158,11,.08)", "rgba(245,158,11,.15)"),
    2: ("#3b82f6", "rgba(59,130,246,.08)", "rgba(59,130,246,.15)"),
    3: ("#22c55e", "rgba(34,197,94,.08)", "rgba(34,197,94,.15)"),
    4: ("#ef4444", "rgba(239,68,68,.08)", "rgba(239,68,68,.15)"),
    5: ("#8b5cf6", "rgba(139,92,246,.08)", "rgba(139,92,246,.15)"),
    6: ("#06b6d4", "rgba(6,182,212,.08)", "rgba(6,182,212,.15)"),
    7: ("#e2b64f", "rgba(226,182,79,.08)", "rgba(226,182,79,.15)"),
    8: ("#ec4899", "rgba(236,72,153,.08)", "rgba(236,72,153,.15)"),
    9: ("#14b8a6", "rgba(20,184,166,.08)", "rgba(20,184,166,.15)"),
    10:("#f97316", "rgba(249,115,22,.08)", "rgba(249,115,22,.15)"),
}

# Load course data from uploaded files
with open(os.path.expanduser("~/naval_100_courses_data.py")) as f:
    exec(f.read())
data1 = list(COURSES)

with open(os.path.expanduser("~/naval_100_courses_data_51_100.py")) as f:
    exec(f.read())
data2 = list(COURSES)

ALL_COURSES = data1 + data2
ALL_COURSES.sort(key=lambda x: x["n"])
print(f"Loaded {len(ALL_COURSES)} courses")

# HTML Page template
PAGE_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_meta}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#07070a;--bg2:#0a0a10;--card:#121218;--card2:#18181f;--card3:#1e1e27;--border:#22222d;--border2:#2e2e3a;--text:#f5f5f7;--text2:#a0a0ab;--text3:#656570;--gold:#e2b64f;--gold-light:#f0d478;--gold-dark:#b8922e;--green:#22c55e;--blue:#3b82f6;--purple:#a78bfa;--accent:#06b6d4;--serif:'Noto Serif SC',serif;--sans:'Inter',-apple-system,sans-serif;--radius:14px;--radius-lg:20px}}
body{{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.85;font-size:17px;-webkit-font-smoothing:antialiased}}
a{{color:var(--gold);text-decoration:none}}
.nav{{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(7,7,10,.88);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.06);height:60px;display:flex;align-items:center}}
.nav-inner{{max-width:960px;margin:0 auto;padding:0 28px;width:100%;display:flex;align-items:center;justify-content:space-between}}
.nav-brand{{display:flex;align-items:center;gap:8px;font-family:var(--serif);font-size:.95rem;font-weight:700;color:var(--gold)}}
.nav-info{{font-size:.78rem;color:var(--text3);background:var(--card2);padding:4px 14px;border-radius:20px}}
.nav-links{{display:flex;gap:14px;flex-wrap:wrap}}
.nav-links a{{font-size:.78rem;color:var(--text3);padding:4px 10px;border-radius:6px;transition:all .2s}}
.nav-links a:hover{{color:var(--gold);background:rgba(226,182,79,.06)}}
.progress-bar{{position:fixed;top:60px;left:0;right:0;height:3px;background:var(--border);z-index:99}}
.progress-fill{{height:100%;background:linear-gradient(90deg,var(--gold),var(--gold-light));transition:width .1s;width:0}}
.main{{max-width:800px;margin:0 auto;padding:90px 28px 60px}}
.lesson-header{{text-align:center;margin-bottom:48px}}
.lesson-phase{{display:inline-block;font-size:.7rem;font-weight:600;color:{phase_color};background:{phase_bg};border:1px solid {phase_border};padding:5px 16px;border-radius:20px;margin-bottom:16px;letter-spacing:.08em;text-transform:uppercase}}
.lesson-header h1{{font-family:var(--serif);font-size:clamp(1.8rem,4.5vw,2.6rem);font-weight:900;line-height:1.25;margin-bottom:14px;background:linear-gradient(135deg,var(--text) 30%,var(--gold-light));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.lesson-header .subtitle{{font-size:1rem;color:var(--text3);margin-bottom:12px}}
.lesson-meta{{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;color:var(--text3);font-size:.82rem}}
.lesson-meta .badge{{padding:3px 10px;border-radius:6px;font-size:.7rem;font-weight:500}}
.lesson-meta .badge-phase{{background:rgba(139,92,246,.1);color:#a78bfa}}
.content h2{{font-family:var(--serif);font-size:1.35rem;font-weight:700;color:var(--text);margin:40px 0 16px;padding-bottom:10px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px}}
.content h2::before{{content:'';width:3px;height:20px;background:var(--gold);border-radius:2px;flex-shrink:0}}
.content h3{{font-size:1.1rem;font-weight:600;color:var(--gold-light);margin:28px 0 10px}}
.content p{{color:var(--text2);font-size:1rem;margin-bottom:12px;line-height:1.9}}
.content strong{{color:var(--text);font-weight:600}}
.content em{{color:var(--gold)}}
.content blockquote{{background:linear-gradient(135deg,rgba(226,182,79,.06),rgba(226,182,79,.02));border-left:3px solid var(--gold);padding:16px 20px;margin:20px 0;border-radius:0 10px 10px 0;color:var(--text);font-size:.95rem;line-height:1.8}}
.content ul{{padding-left:24px;margin:12px 0;color:var(--text2)}}
.content li{{margin:8px 0;line-height:1.75}}
.content li::marker{{color:var(--gold-dark)}}
.callout{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px 28px;margin:24px 0}}
.callout.gold{{border-left:4px solid var(--gold)}}
.callout-label{{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;color:var(--gold)}}
.callout p{{font-size:.93rem;line-height:1.85}}
.concept-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0}}
@media(max-width:640px){{.concept-grid{{grid-template-columns:1fr}}}}
.concept-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px}}
.concept-card .cc-icon{{font-size:1.2rem;margin-bottom:6px}}
.concept-card .cc-text{{font-size:.88rem;color:var(--text3);line-height:1.65}}
.exercise{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:28px 32px;margin:28px 0;border-left:3px solid var(--blue)}}
.exercise h3{{color:var(--text);font-size:1.05rem;margin-bottom:10px}}
.exercise .q{{color:var(--text);font-weight:500;margin-bottom:10px}}
.exercise textarea{{width:100%;min-height:80px;background:var(--card2);border:1px solid var(--border);border-radius:12px;padding:14px 16px;color:var(--text);font-family:var(--sans);font-size:.93rem;resize:vertical;transition:border-color .2s;line-height:1.8}}
.exercise textarea:focus{{outline:none;border-color:var(--gold)}}
.exercise details{{margin-top:12px;padding:12px 16px;background:var(--card2);border-radius:8px}}
.exercise details summary{{cursor:pointer;color:var(--gold);font-weight:500;font-size:.88rem}}
.exercise details[open] summary{{margin-bottom:8px}}
.exercise details p{{font-size:.85rem;color:var(--text3)}}
.bottom-nav{{display:flex;justify-content:space-between;align-items:center;padding:40px 0;margin-top:48px;border-top:1px solid var(--border)}}
.bottom-nav a{{display:flex;align-items:center;gap:8px;padding:14px 28px;border-radius:12px;font-weight:500;transition:all .25s;font-size:.93rem}}
.bottom-nav .prev{{color:var(--text3);border:1px solid var(--border)}}
.bottom-nav .prev:hover{{border-color:var(--gold);color:var(--gold)}}
.bottom-nav .next{{background:var(--gold);color:#1a1a0a}}
.bottom-nav .next:hover{{background:var(--gold-light);transform:translateY(-1px)}}
@media(max-width:640px){{.main{{padding:80px 16px 48px}}.lesson-header h1{{font-size:1.5rem}}.content h2{{font-size:1.15rem}}.exercise{{padding:20px}}.bottom-nav a{{padding:12px 20px;font-size:.85rem}}}}
</style>
</head>
<body>

<nav class="nav">
 <div class="nav-inner">
  <a href="../index.html" class="nav-brand"><svg width="22" height="22" viewBox="0 0 28 28" fill="none"><circle cx="14" cy="14" r="12" stroke="#e2b64f" stroke-width="1.5"/><path d="M6 18c2-6 4-8 8-10s6 2 8 6" stroke="#e2b64f" stroke-width="1.5" fill="none"/><circle cx="14" cy="12" r="2.5" fill="#e2b64f"/></svg>康波研究院</a>
  <div class="nav-links">
   <a href="../naval-course.html">纳瓦尔总览</a>
   <a href="index.html">课程索引</a>
   <a href="../index.html">返回首页</a>
  </div>
 </div>
</nav>

<div class="progress-bar"><div class="progress-fill" id="pf"></div></div>

<div class="main">

<div class="lesson-header">
 <div class="lesson-phase">{phase_label}</div>
 <h1>{title}</h1>
 <div class="subtitle">{subtitle}</div>
 <div class="lesson-meta">
  <span>{icon} 第{n}课 / 共100课</span>
  <span>⏱️ 约{est_time}分钟</span>
  <span class="badge badge-phase">阶段{phase_num}</span>
 </div>
</div>

<div class="content">

<h2>核心洞察</h2>
<blockquote><p>{insight}</p></blockquote>

<h2>关键概念</h2>
<div class="concept-grid">
{concept_cards}
</div>

<h2>本章实践</h2>
<div class="callout gold">
 <div class="callout-label">💡 立即行动</div>
 <p>{practice}</p>
</div>

<h2>思考与练习</h2>

<div class="exercise">
 <h3>🖊️ 本课作业</h3>
 <p class="q">{exercise}</p>
 <textarea placeholder="在这里写下你的思考和答案..."></textarea>
</div>

</div><!-- .content -->

<div class="bottom-nav">
 {prev_link}
 {next_link}
</div>

</div><!-- .main -->

<script>
(function(){{
 var pf=document.getElementById('pf');
 if(pf){{
  window.addEventListener('scroll',function(){{
   var doc=document.documentElement,st=doc.scrollTop,sh=doc.scrollHeight-doc.clientHeight;
   pf.style.width=sh?Math.min(100,(st/sh)*100)+'%':'0';
  }});
 }}
}})();
</script>

</body>
</html>"""

# Index page HTML
INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>纳瓦尔通识课程 · 100门完整体系 — 康波研究院</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#07070a;--bg2:#0a0a10;--card:#121218;--card2:#18181f;--card3:#1e1e27;--border:#22222d;--text:#f5f5f7;--text2:#a0a0ab;--text3:#656570;--gold:#e2b64f;--gold-light:#f0d478;--serif:'Noto Serif SC',serif;--sans:'Inter',-apple-system,sans-serif;--radius:14px;--radius-lg:20px}}
body{{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.85;font-size:17px;-webkit-font-smoothing:antialiased}}
a{{color:var(--gold);text-decoration:none}}
.nav{{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(7,7,10,.88);backdrop-filter:blur(24px);border-bottom:1px solid rgba(255,255,255,.06);height:60px;display:flex;align-items:center}}
.nav-inner{{max-width:1000px;margin:0 auto;padding:0 28px;width:100%;display:flex;align-items:center;justify-content:space-between}}
.nav-brand{{display:flex;align-items:center;gap:8px;font-family:var(--serif);font-size:.95rem;font-weight:700;color:var(--gold)}}
.nav-links{{display:flex;gap:14px}}
.nav-links a{{font-size:.78rem;color:var(--text3);padding:4px 10px;border-radius:6px;transition:all .2s}}
.nav-links a:hover{{color:var(--gold);background:rgba(226,182,79,.06)}}
.main{{max-width:1000px;margin:0 auto;padding:90px 28px 60px}}
.hero{{text-align:center;margin-bottom:48px}}
.hero .hero-icon{{font-size:4rem;margin-bottom:16px}}
.hero h1{{font-family:var(--serif);font-size:2.4rem;font-weight:900;background:linear-gradient(135deg,var(--text) 30%,var(--gold-light));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}}
.hero p{{color:var(--text2);font-size:1.1rem;max-width:600px;margin:0 auto;line-height:1.8}}
.stats{{display:flex;justify-content:center;gap:32px;margin:32px 0;flex-wrap:wrap}}
.stats .stat{{text-align:center}}
.stats .stat-num{{font-family:var(--serif);font-size:2rem;font-weight:900;color:var(--gold)}}
.stats .stat-label{{font-size:.8rem;color:var(--text3)}}
.phase-section{{margin-bottom:40px}}
.phase-header{{display:flex;align-items:flex-start;gap:16px;padding:20px 24px;background:var(--card);border-radius:var(--radius-lg);margin-bottom:16px;border:1px solid var(--border)}}
.phase-icon{{font-size:2rem;min-width:50px;text-align:center}}
.phase-info h2{{font-family:var(--serif);font-size:1.25rem;color:var(--text);margin-bottom:4px}}
.phase-info p{{font-size:.85rem;color:var(--text3);line-height:1.6}}
.course-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px;padding-left:12px}}
.course-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;transition:all .2s;display:block}}
.course-card:hover{{border-color:rgba(226,182,79,.3);transform:translateY(-1px)}}
.course-card .cc-num{{font-size:.78rem;color:var(--gold);font-weight:600;margin-bottom:4px}}
.course-card .cc-title{{font-size:.9rem;font-weight:600;color:var(--text);margin-bottom:2px}}
.course-card .cc-sub{{font-size:.78rem;color:var(--text3)}}
@media(max-width:640px){{.hero h1{{font-size:1.6rem}}.course-grid{{grid-template-columns:1fr}}.stats{{gap:20px}}}}
</style>
</head>
<body>
<nav class="nav">
 <div class="nav-inner">
  <a href="../index.html" class="nav-brand"><svg width="22" height="22" viewBox="0 0 28 28" fill="none"><circle cx="14" cy="14" r="12" stroke="#e2b64f" stroke-width="1.5"/><path d="M6 18c2-6 4-8 8-10s6 2 8 6" stroke="#e2b64f" stroke-width="1.5" fill="none"/><circle cx="14" cy="12" r="2.5" fill="#e2b64f"/></svg>康波研究院</a>
  <div class="nav-links">
   <a href="../naval-course.html">纳瓦尔总览</a>
   <a href="../index.html">返回首页</a>
  </div>
 </div>
</nav>
<div class="main">
<div class="hero">
 <div class="hero-icon">🧘</div>
 <h1>纳瓦尔知识体系 · 100门通识课程</h1>
 <p>基于纳瓦尔·拉维坎特的全部公开资料——推文、播客、采访和《纳瓦尔宝典》——系统构建的完整知识体系。10个阶段，100门课，从财富创造到哲学体系。</p>
 <div class="stats">
  <div class="stat"><div class="stat-num">100</div><div class="stat-label">课程</div></div>
  <div class="stat"><div class="stat-num">10</div><div class="stat-label">阶段</div></div>
  <div class="stat"><div class="stat-num">400+</div><div class="stat-label">核心概念</div></div>
  <div class="stat"><div class="stat-num">100</div><div class="stat-label">实操作业</div></div>
 </div>
</div>
{phase_rows}
</div>
</body>
</html>"""

def gen_page(course):
    n = course["n"]; p = course["p"]
    pc, pbg, pbr = PHASE_COLORS[p]
    phase = PHASES[p-1]
    est = 18 + len(course.get("concepts",[]))*3

    prev = f'<a href="naval{n-1:03d}.html" class="prev">← 第{n-1}课</a>' if n > 1 else f'<a href="index.html" class="prev">← 课程索引</a>'
    next = f'<a href="naval{n+1:03d}.html" class="next">第{n+1}课 →</a>' if n < 100 else f'<a href="index.html" class="next">📚 课程索引</a>'

    icons = ["🔹","🔸","🔷","🔶","💠","🟡","🟢","🔵"]
    cards = []
    for i, c in enumerate(course["concepts"]):
        cards.append(f'  <div class="concept-card"><div class="cc-icon">{icons[i%8]}</div><div class="cc-text">{c}</div></div>')

    html = PAGE_HTML.format(
        title_meta=f"{course['t']} — 纳瓦尔通识课第{n}课 — 康波研究院",
        phase_color=pc, phase_bg=pbg, phase_border=pbr,
        phase_label=f"阶段 {p} · {phase['name']}",
        title=f"{course['icon']} {course['t']}",
        subtitle=course["sub"],
        n=n, est_time=est, phase_num=p,
        insight=course["insight"],
        concept_cards="\n".join(cards),
        practice=course["practice"],
        exercise=course["exercise"],
        prev_link=prev, next_link=next,
    )
    html = html.replace("{{", "{").replace("}}", "}")

    with open(os.path.join(OUT_DIR, f"naval{n:03d}.html"), 'w', encoding='utf-8') as f:
        f.write(html)

def gen_index():
    rows = []
    for p in range(1, 11):
        phase = PHASES[p-1]
        pc, _, _ = PHASE_COLORS[p]
        p_courses = [c for c in ALL_COURSES if c["p"] == p]
        rows.append(f'''    <div class="phase-section">
     <div class="phase-header" style="border-left:4px solid {pc}">
      <div class="phase-icon">{phase["icon"]}</div>
      <div class="phase-info">
       <h2>阶段 {p}：{phase["name"]}（第{p_courses[0]['n']}-{p_courses[-1]['n']}课）</h2>
       <p>{phase["desc"]}</p>
      </div>
     </div>
     <div class="course-grid">''')
        for c in p_courses:
            rows.append(f'      <a href="naval{c["n"]:03d}.html" class="course-card"><div class="cc-num">{c["icon"]} {c["n"]:02d}</div><div class="cc-title">{c["t"]}</div><div class="cc-sub">{c["sub"]}</div></a>')
        rows.append('     </div>\n    </div>')

    html = INDEX_HTML.replace("{phase_rows}", "\n".join(rows))
    with open(os.path.join(OUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(html)

def gen_audio_scripts():
    scripts = {}
    for c in ALL_COURSES:
        n = c["n"]
        text = f"欢迎来到康波研究院纳瓦尔通识课程。第{n}课：{c['t']}。{c['sub']}。{c['insight'][:80]}。现在开始今天的学习。"
        scripts[n] = text
    with open(os.path.join(AUDIO_DIR, "narration_scripts.json"), 'w', encoding='utf-8') as f:
        json.dump(scripts, f, ensure_ascii=False, indent=2)
    return scripts

# ========== EXECUTE ==========
print(f"Generating 100 course pages...")
for i, c in enumerate(ALL_COURSES):
    gen_page(c)
    if (i+1) % 10 == 0:
        print(f"  {i+1}/100 done")

gen_index()
print(f"Index page generated")

scripts = gen_audio_scripts()
print(f"Audio scripts: {len(scripts)} narractions saved")

# Count files
count = len([f for f in os.listdir(OUT_DIR) if f.endswith('.html')])
print(f"\n✅ Complete! {count} files in {OUT_DIR}")
print(f"   Index: https://kangboacademy.cn/naval-courses/index.html")
print(f"   Course 1: https://kangboacademy.cn/naval-courses/naval001.html")
