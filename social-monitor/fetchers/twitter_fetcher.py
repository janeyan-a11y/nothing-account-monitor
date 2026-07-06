"""
Twitter/X 数据抓取器 — 通过 twikit 搜索（免 API 额度，需 X 账号登录）
"""
import asyncio
import json
import sys
import os
from datetime import datetime, timezone

# Windows Git Bash 编码兼容
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 允许作为脚本直接运行
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SEARCH_QUERY, MAX_RESULTS, X_EMAIL, X_PASSWORD

# ============================================================
# twikit 客户端
# ============================================================
from twikit import Client

COOKIE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "twitter_cookies.json"
)

_client = None


async def _get_client_async() -> Client:
    """获取或创建 twikit 客户端（自动复用 cookie）"""
    global _client
    if _client is not None:
        return _client

    client = Client(language="en-US")

    # 尝试加载已保存的 cookie
    if os.path.exists(COOKIE_FILE):
        try:
            client.load_cookies(COOKIE_FILE)
            print("  ✓ 已加载登录缓存")
            _client = client
            return client
        except Exception:
            print("  Cookie 过期，重新登录...")

    # 登录
    print(f"  登录中 ({X_EMAIL})...")
    try:
        await client.login(
            auth_info_1=X_EMAIL,
            auth_info_2=X_EMAIL,
            password=X_PASSWORD,
        )
        # 保存 cookie 供下次复用
        os.makedirs(os.path.dirname(COOKIE_FILE), exist_ok=True)
        client.save_cookies(COOKIE_FILE)
        print("  ✓ 登录成功，cookie 已缓存")
        _client = client
        return client
    except Exception as e:
        print(f"  ✗ 登录失败: {e}")
        raise


def _get_client() -> Client:
    """同步包装器"""
    return asyncio.run(_get_client_async())


async def _search_tweets_async(query: str, max_results: int) -> list[dict]:
    """异步搜索推文"""
    client = await _get_client_async()

    all_tweets = []
    try:
        results = await client.search_tweet(query, product="Latest")

        for tweet in results:
            if len(all_tweets) >= max_results:
                break
            all_tweets.append(_parse_tweet(tweet))

        # 翻页（最多 2 页）
        page = 0
        while len(all_tweets) < max_results and page < 2:
            try:
                results = await results.next()
                page += 1
                for tweet in results:
                    if len(all_tweets) >= max_results:
                        break
                    all_tweets.append(_parse_tweet(tweet))
            except Exception:
                break

    except Exception as e:
        print(f"  ✗ 搜索失败: {e}")
        return []

    return all_tweets


def search_tweets(query: str = None, max_results: int = None) -> list[dict]:
    """
    搜索推文（同步接口）

    Args:
        query: 搜索关键词，默认使用 config.SEARCH_QUERY
        max_results: 最大结果数，默认 config.MAX_RESULTS

    Returns:
        推文列表，统一格式
    """
    if query is None:
        query = SEARCH_QUERY
    if max_results is None:
        max_results = MAX_RESULTS

    return asyncio.run(_search_tweets_async(query, max_results))


def _parse_tweet(tweet) -> dict:
    """将 twikit tweet 对象转成统一格式"""
    created_raw = getattr(tweet, "created_at", "")
    created_iso = _parse_twitter_time(created_raw)

    return {
        "id": str(getattr(tweet, "id", "")),
        "text": getattr(tweet, "text", ""),
        "created_at": created_iso,
        "lang": getattr(tweet, "lang", ""),
        "source": "twikit",
        "author_name": getattr(tweet.user, "name", "") if hasattr(tweet, "user") else "",
        "author_username": getattr(tweet.user, "screen_name", "") if hasattr(tweet, "user") else "",
        "author_followers": getattr(tweet.user, "followers_count", 0) if hasattr(tweet, "user") else 0,
        "retweets": getattr(tweet, "retweet_count", 0),
        "likes": getattr(tweet, "favorite_count", 0),
        "replies": getattr(tweet, "reply_count", 0),
        "views": getattr(tweet, "view_count", 0),
        "url": f"https://x.com/{getattr(tweet.user, 'screen_name', 'i') if hasattr(tweet, 'user') else 'i'}/status/{getattr(tweet, 'id', '')}",
        "platform": "X/Twitter",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def _parse_twitter_time(raw: str) -> str:
    """将 Twitter 时间格式转 ISO 8601"""
    if not raw:
        return ""
    try:
        # 'Thu Apr 07 08:55:28 +0000 2022'
        dt = datetime.strptime(raw, "%a %b %d %H:%M:%S %z %Y")
        return dt.isoformat()
    except ValueError:
        return raw


def check_api_status() -> dict:
    """检查 twikit 客户端状态"""
    try:
        client = _get_client()
        return {
            "connected": True,
            "method": "twikit (cookie-based, no API credits needed)",
            "cookies_cached": os.path.exists(COOKIE_FILE),
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}


# ============================================================
# 命令行测试入口
# ============================================================
def _main():
    print("=" * 60)
    print("  Twitter/X 抓取器 — Nothing Account 舆情监控")
    print("  方案: twikit (免 API 额度)")
    print("=" * 60)

    # 1. 检查连接
    print("\n[1/3] 检查连接...")
    status = check_api_status()
    if status["connected"]:
        print(f"  ✓ 已连接 (方式: {status['method']})")
        print(f"  Cookie 缓存: {'是' if status['cookies_cached'] else '否（将重新登录）'}")
    else:
        print(f"  ✗ 连接失败: {status.get('error', 'Unknown')}")
        print("  请检查 X_EMAIL / X_PASSWORD 是否正确")
        sys.exit(1)

    # 2. 搜索
    print(f"\n[2/3] 搜索关键词...")
    print(f"  Query: {SEARCH_QUERY[:120]}...")
    tweets = search_tweets()
    print(f"  → 找到 {len(tweets)} 条推文")

    # 3. 展示结果
    print(f"\n[3/3] 搜索结果预览:")
    print("-" * 60)
    for i, t in enumerate(tweets[:10], 1):
        text = t["text"].replace("\n", " ")[:100]
        print(f"  [{i}] @{t['author_username']} | {t['created_at'][:16]}")
        print(f"      ❤{t['likes']} 🔄{t['retweets']} 💬{t['replies']}")
        print(f"      {text}")
        print(f"      {t['url']}")
        print()
    if len(tweets) > 10:
        print(f"  ... 还有 {len(tweets) - 10} 条")

    # 保存原始数据
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "latest_twitter.json"
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)
    print(f"\n原始数据已保存: {output_path}")


if __name__ == "__main__":
    _main()
