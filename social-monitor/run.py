#!/usr/bin/env python3
"""
社媒舆情监控 — 主入口
运行所有平台抓取器 → 合并数据 → 生成看板

用法:
  python run.py              # 抓取 + 生成看板
  python run.py --stats      # 仅查看统计
  python run.py --dashboard  # 仅重新生成看板（不抓取）
"""
import json
import os
import sys
import argparse

# Windows Git Bash 编码兼容
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 确保可以导入同级模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DATA_FILE, DASHBOARD_OUTPUT
from data_manager import load_existing, save_mentions, merge_new, get_stats
from generate_dashboard import save_dashboard


def check_credentials() -> bool:
    """检查是否至少有一个数据源可用（Reddit RSS 不需要凭证）"""
    # Reddit RSS 免 API，总是可用
    return True


def run_fetch():
    """运行所有抓取器"""
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
            print(f"  → 需 X 付费 API 或等 twikit 修复")
    except ImportError as e:
        print(f"  ⚠ 缺少依赖: {e}")
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
    except ImportError as e:
        print(f"  ⚠ 缺少依赖: {e}")

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
    except ImportError as e:
        print(f"  ⚠ 缺少依赖: {e}")
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
    except ImportError as e:
        print(f"  ⚠ 缺少依赖: {e}")
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
    except ImportError as e:
        print(f"  ⚠ 缺少依赖: {e}")
    except Exception as e:
        print(f"  ⚠ Bluesky 跳过: {e}")

    print()

    if not all_new:
        print("没有新数据。看板将使用已有数据。")
    else:
        # 合并去重
        existing = load_existing()
        merged, added = merge_new(existing, all_new)
        save_mentions(merged)
        print(f"数据已保存: 新增 {added} 条, 总计 {len(merged)} 条")

    # 生成看板
    print()
    print("[*] 生成看板...")
    path = save_dashboard()
    print(f"  ✓ 看板: {path}")
    print(f"  → 用浏览器打开 file:///{path.replace(chr(92), '/')}")

    # 打印摘要
    stats = get_stats(load_existing())
    print()
    print("=" * 60)
    print("  摘要")
    print("=" * 60)
    print(f"  总计: {stats['total']} 条")
    print(f"  今日: {stats['today']} 条")
    if stats["by_platform"]:
        for p, c in stats["by_platform"].items():
            print(f"  {p}: {c} 条")


def cmd_stats():
    """打印统计"""
    mentions = load_existing()
    stats = get_stats(mentions)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


def cmd_dashboard():
    """重新生成看板"""
    path = save_dashboard()
    print(f"看板已生成: {path}")


# ============================================================
# 命令行入口
# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nothing Account 社媒舆情监控"
    )
    parser.add_argument(
        "--stats", action="store_true", help="仅显示统计"
    )
    parser.add_argument(
        "--dashboard", action="store_true", help="仅重新生成看板"
    )
    args = parser.parse_args()

    if args.stats:
        cmd_stats()
    elif args.dashboard:
        cmd_dashboard()
    else:
        run_fetch()
