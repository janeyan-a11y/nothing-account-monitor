"""
看板生成器 — 将 mentions.json 渲染为静态 HTML 看板
"""
import json
import os
import sys
from datetime import datetime, timezone

# Windows Git Bash 编码兼容
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DASHBOARD_OUTPUT, DATA_FILE
from data_manager import load_existing, get_stats


def _escape_html(text: str) -> str:
    """转义 HTML 特殊字符"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _format_time(iso_str: str) -> str:
    """格式化 ISO 时间为可读格式"""
    if not iso_str:
        return "—"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except (ValueError, AttributeError):
        return iso_str[:16]


def _generate_mentions_html(mentions: list[dict]) -> str:
    """生成推文列表 HTML"""
    if not mentions:
        return '<div class="empty">暂无数据。等待 GitHub Actions 自动抓取...</div>'

    rows = []
    for m in mentions[:100]:  # 最多展示 100 条
        text = _escape_html(m.get("text", ""))
        author = _escape_html(m.get("author_name", "?"))
        username = _escape_html(m.get("author_username", "?"))
        url = m.get("url", "#")
        time_str = _format_time(m.get("created_at", ""))
        platform = m.get("platform", "?")
        # 平台分色
        platform_class = "platform-reddit" if platform == "Reddit" else "platform-community"
        likes = m.get("likes", 0)
        retweets = m.get("retweets", 0)
        replies = m.get("replies", 0)
        followers = m.get("author_followers", 0)

        rows.append(
            f"""
            <div class="mention-card">
              <div class="mention-header">
                <span class="platform-badge {platform_class}">{platform}</span>
                <span class="author">
                  <strong>{author}</strong>
                  <span class="username">@{username}</span>
                  <span class="followers">{followers:,} followers</span>
                </span>
                <span class="time">{time_str}</span>
              </div>
              <div class="mention-text">{text}</div>
              <div class="mention-footer">
                <span>❤ {likes}</span>
                <span>🔄 {retweets}</span>
                <span>💬 {replies}</span>
                <a href="{url}" target="_blank" class="source-link">查看原文 →</a>
              </div>
            </div>"""
        )

    if len(mentions) > 100:
        rows.append(
            f'<div class="more-hint">... 还有 {len(mentions) - 100} 条记录</div>'
        )

    return "\n".join(rows)


def _generate_trend_chart(mentions: list[dict]) -> str:
    """生成简易趋势数据（最近 7 天每日数量）"""
    from collections import Counter

    # 按日期统计最近 7 天
    dates = []
    for m in mentions:
        created = m.get("created_at", "")[:10]
        if created:
            dates.append(created)

    if not dates:
        return ""

    counts = Counter(dates)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # 最近 7 天
    from datetime import timedelta

    last_7 = []
    for i in range(6, -1, -1):
        d = (datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y-%m-%d")
        count = counts.get(d, 0)
        last_7.append((d, count))

    max_count = max(c for _, c in last_7) if last_7 else 1
    max_count = max(max_count, 1)

    bars = []
    for d, c in last_7:
        pct = int(c / max_count * 100) if max_count > 0 else 0
        label = d[-5:]  # MM-DD
        bars.append(
            f"""
            <div class="bar-col">
              <div class="bar-value">{c}</div>
              <div class="bar-fill" style="height:{max(pct, 4)}%"></div>
              <div class="bar-label">{label}</div>
            </div>"""
        )

    return f"""
    <div class="trend-section">
      <h3>📊 近 7 天趋势</h3>
      <div class="bar-chart">{"".join(bars)}</div>
    </div>"""


def generate_dashboard() -> str:
    """生成完整的看板 HTML"""
    mentions = load_existing()
    stats = get_stats(mentions)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 平台分布
    platform_html = "".join(
        f'<span class="stat-chip">{p}: {c}</span>'
        for p, c in stats.get("by_platform", {}).items()
    )

    # Top 作者
    top_authors_html = "".join(
        f'<li><strong>{_escape_html(a["name"])}</strong> @{_escape_html(a["username"])} — {a["count"]} 条 · {a["followers"]:,} followers</li>'
        for a in stats.get("top_authors", [])[:5]
    )

    dashboard_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nothing Account 社媒舆情看板</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #fff; color: #333; padding: 24px; }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  h1 {{ font-size: 1.8rem; margin-bottom: 4px; color: #111; }}
  .subtitle {{ color: #999; font-size: 0.85rem; margin-bottom: 24px; }}

  /* 统计卡片 */
  .stats-grid {{ display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }}
  .stat-card {{ background: #f8f9fa; border: 1px solid #e8e8e8; border-radius: 10px; padding: 16px 20px; min-width: 140px; flex: 1; }}
  .stat-card .number {{ font-size: 2rem; font-weight: 700; color: #111; }}
  .stat-card .label {{ color: #888; font-size: 0.8rem; margin-top: 4px; }}
  .stat-chip {{ display: inline-block; background: #eef1f5; padding: 2px 8px; border-radius: 4px; margin: 2px; font-size: 0.8rem; color: #444; }}

  /* 趋势图 */
  .trend-section {{ background: #f8f9fa; border: 1px solid #e8e8e8; border-radius: 10px; padding: 20px; margin-bottom: 24px; }}
  .trend-section h3 {{ margin-bottom: 16px; font-size: 1rem; color: #333; }}
  .bar-chart {{ display: flex; gap: 12px; align-items: flex-end; height: 160px; }}
  .bar-col {{ display: flex; flex-direction: column; align-items: center; flex:1; height: 100%; justify-content: flex-end; }}
  .bar-value {{ font-size: 0.75rem; color: #888; margin-bottom: 4px; }}
  .bar-fill {{ background: linear-gradient(180deg, #5b9bd5, #2563eb); border-radius: 4px 4px 0 0; width: 100%; max-width: 50px; min-height: 4px; transition: height .3s; }}
  .bar-label {{ font-size: 0.7rem; color: #aaa; margin-top: 6px; }}

  /* 帖子卡片 */
  .mentions-section {{ margin-bottom: 24px; }}
  .mentions-section h3 {{ font-size: 1rem; color: #333; margin-bottom: 12px; }}
  .mention-card {{ background: #fff; border: 1px solid #e8e8e8; border-radius: 10px; padding: 16px; margin-bottom: 10px; transition: box-shadow .2s; }}
  .mention-card:hover {{ border-color: #2563eb; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
  .mention-header {{ display:flex; align-items:center; gap:10px; margin-bottom:8px; font-size:0.85rem; flex-wrap:wrap; }}
  .platform-badge {{ color:#fff; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:600; }}
  .platform-reddit {{ background:#ff4500; }}
  .platform-community {{ background:#1d4ed8; }}
  .author {{ color:#333; }}
  .username {{ color:#999; margin-left:4px; }}
  .followers {{ color:#bbb; font-size:0.7rem; margin-left:6px; }}
  .time {{ color:#bbb; font-size:0.75rem; margin-left:auto; }}
  .mention-text {{ color:#444; line-height:1.6; margin-bottom:8px; word-break:break-word; }}
  .mention-footer {{ display:flex; gap:16px; font-size:0.8rem; color:#999; }}
  .source-link {{ color:#2563eb; text-decoration:none; margin-left:auto; }}
  .source-link:hover {{ text-decoration:underline; }}

  /* 状态区 */
  .empty {{ text-align:center; padding:60px 20px; color:#999; font-size:1rem; }}
  .more-hint {{ text-align:center; color:#bbb; padding:12px; font-size:0.85rem; }}

  /* Top 作者 */
  .top-authors {{ background: #f8f9fa; border: 1px solid #e8e8e8; border-radius: 10px; padding: 20px; margin-bottom: 24px; }}
  .top-authors h3 {{ font-size: 1rem; color: #333; margin-bottom: 12px; }}
  .top-authors ol {{ padding-left: 20px; color: #333; line-height: 1.8; font-size: 0.9rem; }}
  .top-authors li {{ margin-bottom: 4px; }}

  .footer {{ text-align:center; color:#ccc; font-size:0.75rem; padding:24px; }}
</style>
</head>
<body>
<div class="container">

  <h1>🔍 Nothing Account 社媒舆情看板</h1>
  <div class="subtitle">最后更新: {now} · 监控来源: Reddit + Nothing Community · 每日自动刷新</div>

  <!-- 统计卡片 -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="number">{stats['total']}</div>
      <div class="label">累计抓取</div>
    </div>
    <div class="stat-card">
      <div class="number">{stats['today']}</div>
      <div class="label">今日新增</div>
    </div>
    <div class="stat-card">
      <div class="number">{stats['avg_likes']}</div>
      <div class="label">平均点赞</div>
    </div>
    <div class="stat-card">
      <div class="label" style="margin-top:4px;">平台分布</div>
      <div style="margin-top:8px;">{platform_html or '<span class="stat-chip">暂无</span>'}</div>
    </div>
  </div>

  <!-- 趋势图 -->
  {_generate_trend_chart(mentions)}

  <!-- Top 作者 -->
  <div class="top-authors">
    <h3>📢 影响力 Top 作者</h3>
    <ol>{top_authors_html or '<li style="color:#666;">暂无数据</li>'}</ol>
  </div>

  <!-- 最新提及 -->
  <div class="mentions-section">
    <h3>📋 最新提及 ({len(mentions)} 条)</h3>
    {_generate_mentions_html(mentions)}
  </div>

  <div class="footer">
    Nothing Account Social Monitor · Reddit + Nothing Community · Daily Auto Refresh
  </div>

</div>
</body>
</html>"""

    return dashboard_html


def save_dashboard() -> str:
    """生成并保存看板 HTML，返回文件路径"""
    html = generate_dashboard()
    os.makedirs(os.path.dirname(DASHBOARD_OUTPUT), exist_ok=True)
    with open(DASHBOARD_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    return DASHBOARD_OUTPUT


if __name__ == "__main__":
    path = save_dashboard()
    print(f"看板已生成: {path}")
    print(f"文件大小: {os.path.getsize(path):,} bytes")
