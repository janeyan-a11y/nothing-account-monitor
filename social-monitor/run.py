#!/usr/bin/env python3
"""
社媒舆情监控 — 主入口
运行所有平台抓取器 → 合并数据 → 生成看板 → 负面邮件告警

用法:
  python run.py              # 抓取 + 生成看板 + 邮件告警
  python run.py --stats      # 仅查看统计
  python run.py --dashboard  # 仅重新生成看板（不抓取）
"""
import json, os, sys, argparse, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone

if sys.platform == "win32":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except: pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (DATA_FILE, DASHBOARD_OUTPUT,
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ALERT_EMAIL, ALERT_THRESHOLD)
from data_manager import load_existing, save_mentions, merge_new, get_stats
from generate_dashboard import save_dashboard

# ============================================================
# 情感分析（与 generate_dashboard.py 保持一致）
# ============================================================
NEG_KW = ["error","problem","issue","fail","failed","bug","crash","can't","cannot","won't",
    "not working","broken","hate","terrible","frustrating","annoying","delete","deactivate",
    "stuck","forced","useless","garbage","worst","wtf","ridiculous","unacceptable",
    "disappointed","doesn't work","unable","impossible","authorization error",
    "account error","login issue","sign in requirement"]
POS_KW = ["love","great","good","awesome","fixed","solved","helpful","works","easy",
    "best","amazing","nice","thank","thanks","wow","excellent","brilliant","fantastic",
    "perfect","smooth","finally","appreciation","impressive","recommend"]

def _sentiment(title, text):
    c = (title + " " + text).lower()
    n = sum(1 for k in NEG_KW if k in c)
    p = sum(1 for k in POS_KW if k in c)
    return "negative" if n > p else ("positive" if p > n else "neutral")

# ============================================================
# 邮件告警
# ============================================================
def send_alert(neg_posts: list[dict], today_str: str) -> bool:
    """发送负面舆情告警邮件"""
    if not SMTP_PASS:
        print("  ⚠ 未配置 SMTP_PASS，跳过邮件告警")
        return False

    count = len(neg_posts)
    subject = f"🚨 Nothing Account 负面舆情告警 — {today_str} ({count}条)"

    # 构造邮件正文
    rows = ""
    for i, p in enumerate(neg_posts[:10], 1):
        plat = p.get("platform", "?")
        title = p.get("title", "")[:100]
        url = p.get("url", "#")
        text = p.get("text", "")[:200]
        rows += f"""
  [{i}] [{plat}] {title}
      {text[:150]}
      {url}
"""

    body = f"""Nothing Account 社媒舆情 — 负面告警

日期: {today_str}
负面帖数: {count} 条（阈值: {ALERT_THRESHOLD} 条）

详情:
{rows}

--
看板: https://janeyan-a11y.github.io/nothing-account-monitor/
自动发送 - Nothing Account Social Monitor
"""

    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = ALERT_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"  ✓ 告警邮件已发送到 {ALERT_EMAIL}")
        return True
    except Exception as e:
        print(f"  ✗ 邮件发送失败: {e}")
        return False


def check_credentials() -> bool:
    return True


def run_fetch():
    print("=" * 60)
    print("  Nothing Account 社媒舆情 — 数据抓取")
    print("=" * 60)
    print()

    if not check_credentials():
        return

    all_new = []

    # --- Twitter/X (待修复) ---
    print("[1] Twitter/X 搜索...")
    try:
        from fetchers.twitter_fetcher import search_tweets, check_api_status
        status = check_api_status()
        if status["connected"]:
            print(f"  ✓ 已连接 ({status.get('method', '')})")
            tweets = search_tweets()
            print(f"  → 抓到 {len(tweets)} 条推文")
            all_new.extend(tweets)
        else:
            print(f"  ⚠ X 不可用: {status.get('error', 'Unknown')}")
    except Exception as e:
        print(f"  ⚠ X 跳过: {e}")

    # --- Reddit ---
    print("[2] Reddit 搜索...")
    try:
        from fetchers.reddit_fetcher import search_reddit, check_reddit_status
        r_status = check_reddit_status()
        if r_status["connected"]:
            print(f"  ✓ API 已连接")
            reddit_posts = search_reddit()
            print(f"  → 抓到 {len(reddit_posts)} 条帖子")
            all_new.extend(reddit_posts)
        else:
            print(f"  ⚠ 跳过: {r_status.get('error', 'Unknown')}")
    except Exception as e:
        print(f"  ⚠ Reddit 跳过: {e}")

    # --- Nothing Community ---
    print("[3] Nothing Community 搜索...")
    try:
        from fetchers.community_fetcher import search_community, check_community_status
        c_status = check_community_status()
        if c_status["connected"]:
            print(f"  ✓ API 已连接 ({c_status['method']})")
            community_posts = search_community()
            print(f"  → 抓到 {len(community_posts)} 条讨论")
            all_new.extend(community_posts)
        else:
            print(f"  ⚠ 跳过: {c_status.get('error', 'Unknown')}")
    except Exception as e:
        print(f"  ⚠ Community 跳过: {e}")

    # --- YouTube ---
    print("[4] YouTube 搜索...")
    try:
        from fetchers.youtube_fetcher import search_youtube, check_youtube_status
        yt_status = check_youtube_status()
        if yt_status["connected"]:
            print(f"  ✓ API 已连接")
            yt_videos = search_youtube()
            print(f"  → 抓到 {len(yt_videos)} 个视频")
            all_new.extend(yt_videos)
        else:
            print(f"  ⚠ 跳过: {yt_status.get('error', 'Unknown')}")
    except Exception as e:
        print(f"  ⚠ YouTube 跳过: {e}")

    # --- Bluesky ---
    print("[5] Bluesky 搜索...")
    try:
        from fetchers.bluesky_fetcher import search_bluesky, check_bluesky_status
        b_status = check_bluesky_status()
        if b_status["connected"]:
            print(f"  ✓ API 已连接")
            bsky_posts = search_bluesky()
            print(f"  → 抓到 {len(bsky_posts)} 条帖子")
            all_new.extend(bsky_posts)
        else:
            print(f"  ⚠ 跳过: {b_status.get('error', 'Unknown')}")
    except Exception as e:
        print(f"  ⚠ Bluesky 跳过: {e}")

    print()

    # 合并去重（保留历史数据）
    existing = load_existing()
    merged, added = merge_new(existing, all_new)
    save_mentions(merged)
    print(f"数据已保存: 新增 {added} 条, 总计 {len(merged)} 条")

    # 生成看板
    print()
    print("[*] 生成看板...")
    path = save_dashboard()
    print(f"  ✓ 看板: {path}")

    # === 负面邮件告警 ===
    print()
    print("[*] 负面舆情检查...")
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_neg = [m for m in merged
        if m.get("created_at", "")[:10] == today_str
        and _sentiment(m.get("title", ""), m.get("text", "")) == "negative"]
    print(f"  今日负面: {len(today_neg)} 条 (告警阈值: {ALERT_THRESHOLD} 条)")
    if len(today_neg) >= ALERT_THRESHOLD:
        send_alert(today_neg, today_str)
    else:
        print(f"  ✓ 未触发告警，跳过邮件")

    # 打印摘要
    stats = get_stats(load_existing())
    print()
    print("=" * 60)
    print("  摘要")
    print("=" * 60)
    print(f"  总计: {stats['total']} 条")
    print(f"  今日: {stats['today']} 条")
    for p, c in stats.get("by_platform", {}).items():
        print(f"  {p}: {c} 条")


def cmd_stats():
    mentions = load_existing()
    stats = get_stats(mentions)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def cmd_dashboard():
    path = save_dashboard()
    print(f"看板已生成: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nothing Account 社媒舆情监控")
    parser.add_argument("--stats", action="store_true", help="仅显示统计")
    parser.add_argument("--dashboard", action="store_true", help="仅重新生成看板")
    args = parser.parse_args()
    if args.stats: cmd_stats()
    elif args.dashboard: cmd_dashboard()
    else: run_fetch()
