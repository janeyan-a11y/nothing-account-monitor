"""Nothing Account 社媒舆情看板生成器"""
import json, os, sys
from datetime import datetime, timezone, timedelta
from collections import Counter

if sys.platform == "win32":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DASHBOARD_OUTPUT, DATA_FILE
from data_manager import load_existing, get_stats

# ============================================================
# 情感分析关键词
# ============================================================
NEG_KW = ["error","problem","issue","fail","failed","bug","crash","can't","cannot","won't",
    "not working","broken","hate","terrible","frustrating","annoying","delete","deactivate",
    "stuck","forced","useless","garbage","worst","wtf","ridiculous","unacceptable",
    "disappointed","doesn't work","unable","impossible","authorization error",
    "account error","login issue","sign in requirement"]
POS_KW = ["love","great","good","awesome","fixed","solved","helpful","works","easy",
    "best","amazing","nice","thank","thanks","wow","excellent","brilliant","fantastic",
    "perfect","smooth","finally","appreciation","impressive","recommend"]

def _sentiment(ti, tx):
    c = (ti + " " + tx).lower()
    n = sum(1 for k in NEG_KW if k in c); p = sum(1 for k in POS_KW if k in c)
    return "negative" if n > p else ("positive" if p > n else "neutral")

# ============================================================
# 话题标签规则
# ============================================================
TOPIC_RULES = [
    ("#登录", ["login","sign in","sign-in","signin","log in"]),
    ("#注销", ["delete account","deactivate","account delete","remove account"]),
    ("#密码", ["password","passcode","pin","forgot password","reset password"]),
    ("#验证", ["verify","verification","2fa","two-factor","two factor","authenticator","auth","authorization"]),
    ("#同步", ["sync","backup","restore","cloud backup","cloud sync"]),
    ("#注册", ["sign up","sign-up","signup","register","create account","new account"]),
    ("#Gmail", ["gmail","google account","google mail"]),
    ("#FRP", ["frp","factory reset","hard reset"]),
    ("#EssentialSpace", ["essential space"]),
]

def _topics(ti, tx):
    c = (ti + " " + tx).lower()
    tags = [t for t, ks in TOPIC_RULES if any(k in c for k in ks)]
    return tags or ["#其他"]

# ============================================================
# 周/月对比
# ============================================================
def _comparison(mentions):
    now = datetime.now(timezone.utc); tw = 0; lw = 0
    for m in mentions:
        d = m.get("created_at","")[:10]
        if not d: continue
        try:
            dt = datetime.fromisoformat(d)
            da = (now - dt.replace(tzinfo=timezone.utc)).days
            if 0 <= da < 7: tw += 1
            elif 7 <= da < 14: lw += 1
        except: pass
    if lw == 0: trend = "↑ 新增" if tw > 0 else "→ 持平"
    else:
        pct = round((tw - lw) / lw * 100)
        trend = f"↑ +{pct}%" if pct > 0 else (f"↓ {pct}%" if pct < 0 else "→ 持平")
    return {"this_week": tw, "last_week": lw, "trend": trend}

# ============================================================
# 每日摘要
# ============================================================
def _summary(mentions):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    tp = [m for m in mentions if m.get("created_at","")[:10] == today]
    if not tp:
        ld = max((m.get("created_at","")[:10] for m in mentions), default="?")
        tp = [m for m in mentions if m.get("created_at","")[:10] == ld]; dl = ld
    else: dl = today
    if not tp: return "暂无数据，等待首次抓取。"
    neg = sum(1 for m in tp if _sentiment(m.get("title",""),m.get("text",""))=="negative")
    pos = sum(1 for m in tp if _sentiment(m.get("title",""),m.get("text",""))=="positive")
    all_t = []; [all_t.extend(_topics(m.get("title",""),m.get("text",""))) for m in tp]
    top_t = [t for t,_ in Counter(all_t).most_common(3)]
    parts = [f"{dl} 共 {len(tp)} 条讨论"]
    if neg: parts.append(f"{neg} 条负面")
    if pos: parts.append(f"{pos} 条正面")
    if top_t: parts.append(f"热点 {' '.join(top_t)}")
    return "；".join(parts) + "。"

# ============================================================
# 各平台抓取状态
# ============================================================
def _pstatus(mentions):
    platforms = {}
    for m in mentions:
        p = m.get("platform","?"); ft = m.get("fetched_at","")
        if p not in platforms or ft > platforms[p]: platforms[p] = ft
    now = datetime.now(timezone.utc); rows = []
    for p in ["Reddit","Nothing Community","YouTube","Bluesky"]:
        ft = platforms.get(p,"")
        if ft:
            try:
                dt = datetime.fromisoformat(ft.replace("Z","+00:00"))
                if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
                diff = now - dt
                if diff.days == 0:
                    ago = f"{diff.seconds//3600}小时前" if diff.seconds>=3600 else f"{max(diff.seconds//60,1)}分钟前"
                else: ago = f"{diff.days}天前"
                st = "🟢" if diff.days<2 else ("🟡" if diff.days<4 else "🔴")
            except: st,ago = "⚪","未知"
        else: st,ago = "🔴","无数据"
        rows.append(f'<span class="status-chip">{st} {p}: {ago}</span>')
    return "".join(rows)

# ============================================================
# HTML helpers
# ============================================================
def _e(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&#39;")
def _fmt(iso):
    if not iso: return "—"
    try: return datetime.fromisoformat(iso.replace("Z","+00:00")).strftime("%Y-%m-%d %H:%M UTC")
    except: return iso[:16]

def _cards(mentions):
    if not mentions: return '<div class="empty">暂无数据。等待 GitHub Actions 自动抓取...</div>'
    rows = []
    pc = {"Reddit":"platform-reddit","Nothing Community":"platform-community","YouTube":"platform-youtube","Bluesky":"platform-bluesky"}
    for m in mentions[:200]:
        p = m.get("platform","?")
        sent = _sentiment(m.get("title",""),m.get("text",""))
        sl = {"positive":"😊 正面","negative":"🔴 负面","neutral":"➖ 中性"}.get(sent,"")
        tags = _topics(m.get("title",""),m.get("text",""))
        th = "".join(f'<span class="topic-tag">{t}</span>' for t in tags)
        rows.append(f"""<div class="mention-card" data-platform="{p}" data-sentiment="{sent}" data-date="{m.get('created_at','')[:10]}" data-tags="{' '.join(tags)}">
  <div class="mention-header">
    <span class="platform-badge {pc.get(p,'platform-community')}">{p}</span>
    <span class="sent-badge sent-{sent}">{sl}</span> {th}
    <span class="author"><strong>{_e(m.get('author_name','?'))}</strong> <span class="username">@{_e(m.get('author_username','?'))}</span></span>
    <span class="time">{_fmt(m.get('created_at',''))}</span>
  </div>
  <div class="mention-text">{_e(m.get('text',''))}</div>
  <div class="mention-footer">
    <span>❤ {m.get('likes',0)}</span><span>🔄 {m.get('retweets',0)}</span><span>💬 {m.get('replies',0)}</span>
    <a href="{m.get('url','#')}" target="_blank" class="source-link">查看原文 →</a>
  </div>
</div>""")
    return "\n".join(rows)

def _trend(mentions):
    dates = Counter(m.get("created_at","")[:10] for m in mentions if m.get("created_at","")[:10])
    if not dates: return ""
    now = datetime.now(timezone.utc)
    last_7 = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6,-1,-1)]
    counts = [dates.get(d,0) for d in last_7]; mx = max(counts) or 1
    bars = "".join(f'<div class="bar-col"><div class="bar-value">{c}</div><div class="bar-fill" style="height:{max(int(c/mx*100),4)}%"></div><div class="bar-label">{d[-5:]}</div></div>' for d,c in zip(last_7,counts))
    return f'<div class="trend-section"><h3>📊 近 7 天趋势</h3><div class="bar-chart">{bars}</div></div>'

# ============================================================
# 主函数
# ============================================================
def generate_dashboard():
    mentions = load_existing()
    stats = get_stats(mentions)
    comp = _comparison(mentions)
    summary = _summary(mentions)
    pstatus = _pstatus(mentions)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 异常告警：当日负面 >= 5 条
    today_neg = sum(1 for m in mentions
        if m.get("created_at","")[:10] == today_str
        and _sentiment(m.get("title",""),m.get("text",""))=="negative")
    sent_counts = Counter(_sentiment(m.get("title",""),m.get("text","")) for m in mentions)
    neg_pct = round(sent_counts.get("negative",0)/max(len(mentions),1)*100,1)

    alerts = []
    if today_neg >= 5:
        alerts.append(f'🚨 今日负面舆情 {today_neg} 条，超过警戒线 5 条，建议立即排查处理')
    alert_html = "".join(f'<div class="alert-banner">{a}</div>' for a in alerts)

    platform_html = "".join(
        f'<span class="stat-chip pfilter" data-p="{p}" onclick="filterPlatform(\'{p}\')">{p}: {c}</span>'
        for p,c in stats.get("by_platform",{}).items())

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">
<title>Nothing Account 社媒舆情看板</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#fff;color:#333;padding:24px}}
.container{{max-width:960px;margin:0 auto}}
h1{{font-size:1.8rem;margin-bottom:4px;color:#111}}
.subtitle{{color:#999;font-size:.85rem;margin-bottom:16px}}
.daily-summary{{background:#f0f7ff;border:1px solid #c5d9f0;border-radius:10px;padding:14px 18px;margin-bottom:16px;font-size:.95rem;color:#333;line-height:1.6}}
.daily-summary strong{{color:#1a56db}}
.status-bar{{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap}}
.status-chip{{display:inline-block;background:#f8f9fa;border:1px solid #e8e8e8;border-radius:6px;padding:4px 10px;font-size:.78rem;color:#666}}
.toolbar{{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center}}
.toolbar input,.toolbar select,.toolbar button{{padding:8px 12px;border:1px solid #ddd;border-radius:6px;font-size:.85rem;background:#fff}}
.toolbar input{{flex:1;min-width:180px}}
.toolbar input:focus{{border-color:#2563eb;outline:none}}
.toolbar button{{cursor:pointer;background:#2563eb;color:#fff;border-color:#2563eb}}
.toolbar button:hover{{background:#1d4ed8}}
.toolbar .btn-export{{background:#fff;color:#2563eb}}
.toolbar .btn-export:hover{{background:#eef4ff}}
.filter-bar{{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}}
.filter-chip{{padding:6px 14px;border:1px solid #ddd;border-radius:20px;font-size:.8rem;cursor:pointer;background:#fff;transition:all .2s}}
.filter-chip:hover,.filter-chip.active{{background:#2563eb;color:#fff;border-color:#2563eb}}
.alert-banner{{background:#fff3f3;border:1px solid #ffc9c9;border-radius:8px;padding:12px 18px;margin-bottom:16px;color:#d32f2f;font-size:.9rem;font-weight:600}}
.stats-grid{{display:flex;gap:16px;margin-bottom:24px;flex-wrap:wrap}}
.stat-card{{background:#f8f9fa;border:1px solid #e8e8e8;border-radius:10px;padding:16px 20px;min-width:140px;flex:1}}
.stat-card .number{{font-size:2rem;font-weight:700;color:#111}}
.stat-card .label{{color:#888;font-size:.8rem;margin-top:4px}}
.stat-card .trend-up{{color:#d32f2f}}.stat-card .trend-down{{color:#2d8a2d}}
.stat-chip{{display:inline-block;background:#eef1f5;padding:2px 8px;border-radius:4px;margin:2px;font-size:.8rem;color:#444;cursor:pointer;transition:all .2s}}
.stat-chip:hover{{background:#dde3f0}}
.stat-chip.active-chip{{background:#2563eb;color:#fff}}
.trend-section{{background:#f8f9fa;border:1px solid #e8e8e8;border-radius:10px;padding:20px;margin-bottom:24px}}
.trend-section h3{{margin-bottom:16px;font-size:1rem;color:#333}}
.bar-chart{{display:flex;gap:12px;align-items:flex-end;height:160px}}
.bar-col{{display:flex;flex-direction:column;align-items:center;flex:1;height:100%;justify-content:flex-end}}
.bar-value{{font-size:.75rem;color:#888;margin-bottom:4px}}
.bar-fill{{background:linear-gradient(180deg,#5b9bd5,#2563eb);border-radius:4px 4px 0 0;width:100%;max-width:50px;min-height:4px;transition:height .3s}}
.bar-label{{font-size:.7rem;color:#aaa;margin-top:6px}}
.mentions-section{{margin-bottom:24px}}
.mentions-section h3{{font-size:1rem;color:#333;margin-bottom:12px}}
.mention-card{{background:#fff;border:1px solid #e8e8e8;border-radius:10px;padding:16px;margin-bottom:10px;transition:box-shadow .2s}}
.mention-card:hover{{border-color:#2563eb;box-shadow:0 2px 8px rgba(0,0,0,0.06)}}
.mention-header{{display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:.85rem;flex-wrap:wrap}}
.platform-badge{{color:#fff;padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:600}}
.platform-reddit{{background:#ff4500}}.platform-community{{background:#1d4ed8}}
.platform-youtube{{background:red}}.platform-bluesky{{background:#1083fe}}
.sent-badge{{padding:2px 8px;border-radius:4px;font-size:.75rem;font-weight:600}}
.sent-positive{{background:#e6f7e6;color:#2d8a2d}}
.sent-negative{{background:#ffe6e6;color:#d32f2f}}
.sent-neutral{{background:#f0f0f0;color:#888}}
.topic-tag{{display:inline-block;background:#e8f0fe;color:#1a56db;padding:1px 6px;border-radius:3px;font-size:.7rem;cursor:pointer}}
.topic-tag:hover{{background:#d0e0fc}}
.author{{color:#333}}.username{{color:#999;margin-left:4px}}.time{{color:#bbb;font-size:.75rem;margin-left:auto}}
.mention-text{{color:#444;line-height:1.6;margin-bottom:8px;word-break:break-word}}
.mention-footer{{display:flex;gap:16px;font-size:.8rem;color:#999}}
.source-link{{color:#2563eb;text-decoration:none;margin-left:auto}}
.source-link:hover{{text-decoration:underline}}
.empty{{text-align:center;padding:60px 20px;color:#999;font-size:1rem}}
.footer{{text-align:center;color:#ccc;font-size:.75rem;padding:24px}}
.translate-bar{{display:flex;justify-content:flex-end;margin-bottom:16px}}
.btn-translate{{padding:8px 18px;border:1px solid #2563eb;border-radius:6px;background:#fff;color:#2563eb;cursor:pointer;font-size:.9rem;transition:all .2s}}
.btn-translate:hover{{background:#2563eb;color:#fff}}
.btn-translate.active{{background:#2563eb;color:#fff}}
.btn-translate:disabled{{opacity:0.5;cursor:wait}}
.hidden{{display:none!important}}
</style>
</head>
<body>
<div class="container">
<h1>🔍 Nothing Account 社媒舆情看板</h1>
<div class="subtitle">最后更新: {now} · 4平台监控 · 每日自动刷新</div>
<div class="translate-bar"><button class="btn-translate" id="btnTranslate" onclick="toggleTranslate()">🌐 翻译成中文</button></div>
<div class="daily-summary"><strong>📝 今日摘要：</strong>{summary}</div>
<div class="status-bar">{pstatus}</div>
<div class="toolbar">
  <input type="text" id="searchInput" placeholder="🔍 搜索关键词..." oninput="applyFilters()">
  <select id="timeFilter" onchange="applyFilters()"><option value="all">全部时间</option><option value="7">近 7 天</option><option value="30">近 30 天</option><option value="1">今天</option></select>
  <button class="btn-export" onclick="exportCSV()">📥 导出 CSV</button>
</div>
<div class="filter-bar">
  <span class="filter-chip active" data-platform="all" onclick="filterPlatform('all')">全部</span>
  <span class="filter-chip" data-platform="Reddit" onclick="filterPlatform('Reddit')">🟠 Reddit</span>
  <span class="filter-chip" data-platform="Nothing Community" onclick="filterPlatform('Nothing Community')">🔵 Community</span>
  <span class="filter-chip" data-platform="YouTube" onclick="filterPlatform('YouTube')">🔴 YouTube</span>
  <span class="filter-chip" data-platform="Bluesky" onclick="filterPlatform('Bluesky')">🔵 Bluesky</span>
</div>
{alert_html}
<div class="stats-grid">
  <div class="stat-card"><div class="number">{stats['total']}</div><div class="label">累计抓取</div></div>
  <div class="stat-card"><div class="number">{today_neg}</div><div class="label">今日负面</div></div>
  <div class="stat-card"><div class="number">{comp['this_week']}</div><div class="label">本周 <span class="{'trend-up' if '↑' in comp['trend'] else ('trend-down' if '↓' in comp['trend'] else '')}">{comp['trend']}</span> (上周 {comp['last_week']})</div></div>
  <div class="stat-card"><div class="number" style="color:{'#d32f2f' if neg_pct > 30 else '#111'}">{neg_pct}%</div><div class="label">负面占比</div></div>
  <div class="stat-card" style="flex:2;min-width:280px;"><div class="label" style="margin-top:4px;">平台分布</div><div style="margin-top:8px;">{platform_html or '<span class="stat-chip">暂无</span>'}</div></div>
</div>
{_trend(mentions)}
<div class="mentions-section">
  <h3>📋 最新提及 (<span id="mentionCount">{len(mentions)}</span> 条)</h3>
  {_cards(mentions)}
</div>
<div class="footer">Nothing Account Social Monitor · 4 Platforms · Daily Auto Refresh</div>
</div>
<script>
var _platform='all';
function filterPlatform(p){{_platform=p;document.querySelectorAll('.filter-chip').forEach(function(c){{c.classList.toggle('active',c.dataset.platform===p||(p==='all'&&c.dataset.platform==='all'));}});document.querySelectorAll('.pfilter').forEach(function(c){{c.classList.toggle('active-chip',c.dataset.p===p);}});applyFilters();}}
function applyFilters(){{var q=(document.getElementById('searchInput').value||'').toLowerCase();var days=parseInt(document.getElementById('timeFilter').value)||0;var cards=document.querySelectorAll('.mention-card');var count=0;var today=new Date().toISOString().slice(0,10);cards.forEach(function(c){{var platform=c.dataset.platform;var date=c.dataset.date||'';var text=c.textContent.toLowerCase();var show=true;if(_platform!=='all'&&platform!==_platform)show=false;if(q&&text.indexOf(q)===-1)show=false;if(days===1&&date!==today)show=false;if(days>1){{var cutoff=new Date();cutoff.setDate(cutoff.getDate()-days);if(date<cutoff.toISOString().slice(0,10))show=false;}}c.classList.toggle('hidden',!show);if(show)count++;}});document.getElementById('mentionCount').textContent=count;}}
function exportCSV(){{var rows=[['平台','日期','作者','标题','情感','点赞','评论','URL'].join(',')];document.querySelectorAll('.mention-card:not(.hidden)').forEach(function(c){{var p=c.querySelector('.platform-badge').textContent.trim();var t=c.querySelector('.time').textContent.trim();var a=c.querySelector('.author strong').textContent.trim();var txt='"'+c.querySelector('.mention-text').textContent.trim().replace(/"/g,'""').substring(0,200)+'"';var s=c.querySelector('.sent-badge').textContent.trim();var likes=c.querySelector('.mention-footer span').textContent.replace(/[^0-9]/g,'')||'0';var replies=c.querySelectorAll('.mention-footer span')[2].textContent.replace(/[^0-9]/g,'')||'0';var url=c.querySelector('.source-link').href;rows.push([p,t,a,txt,s,likes,replies,url].join(','));}});var blob=new Blob(['\\ufeff'+rows.join('\\n')],{{type:'text/csv;charset=utf-8'}});var link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='nothing-account-'+new Date().toISOString().slice(0,10)+'.csv';link.click();}}
var _t=false,_api='https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&dt=t&q=';
async function toggleTranslate(){{var b=document.getElementById('btnTranslate'),els=document.querySelectorAll('.mention-text');if(_t){{els.forEach(function(el){{if(el.dataset.o){{el.textContent=el.dataset.o;el.removeAttribute('data-o');}}}});b.textContent='🌐 翻译成中文';b.classList.remove('active');_t=false;}}else{{b.textContent='翻译中...';b.disabled=true;for(var i=0;i<els.length;i++){{var el=els[i],orig=el.textContent.trim();if(!orig||orig.length<5)continue;if(!el.dataset.o)el.dataset.o=orig;try{{var r=await fetch(_api+encodeURIComponent(orig.substring(0,1500)));var d=await r.json();var t=d[0].filter(function(x){{return x[0]}}).map(function(x){{return x[0]}}).join('');if(t)el.textContent=t;}}catch(e){{}}}}b.textContent='🔤 显示原文';b.classList.add('active');b.disabled=false;_t=true;}}}}
</script>
</body></html>"""
    return html

def save_dashboard():
    html = generate_dashboard()
    os.makedirs(os.path.dirname(DASHBOARD_OUTPUT), exist_ok=True)
    with open(DASHBOARD_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    return DASHBOARD_OUTPUT

if __name__ == "__main__":
    print(f"OK: {save_dashboard()}")
