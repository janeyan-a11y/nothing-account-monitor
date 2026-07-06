"""
Reddit 数据抓取器 — 通过 Reddit RSS/Atom 搜索（免 API，免登录）
"""
import json
import sys
import os
import time
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from urllib.parse import quote

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MAX_RESULTS

# ============================================================
# 配置
# ============================================================
SUBREDDITS = [
    "NothingTech",
    "Nothing",
    "Android",
    "PickAnAndroidForMe",
    "smartphone",
]

# 搜索关键词（RSS 搜索精度较低，抓回来后再标题过滤）
SEARCH_KEYWORDS = [
    "Nothing Account",
    "Nothing login",
    "Nothing OS account",
    "Nothing Phone account",
    "Nothing sign in",
    "NothingOS",
]

# 标题/内容必须包含的关键词（客户端过滤，提高精度）
# 注意：只保留账号相关的精确关键词，避免 NothingOS 这种太泛的
TITLE_FILTERS = [
    "account",
    "login",
    "sign in",
    "sign-in",
    "signin",
    "sign up",
    "sign-up",
    "signup",
    "password",
    "verify",
    "verification",
    "2FA",
    "two-factor",
    "two factor",
    "authenticator",
    "sync",
    "backup",
    "restore",
    "delete account",
    "deactivate",
    "注销",
]

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

# Atom namespace
ATOM_NS = "http://www.w3.org/2005/Atom"


def _is_relevant(title: str, text: str = "") -> bool:
    """判断帖子是否与 Nothing Account 相关"""
    combined = (title + " " + text).lower()
    for f in TITLE_FILTERS:
        if f.lower() in combined:
            return True
    return False


def _search_rss(subreddit: str, query: str, limit: int = 25, retries: int = 3) -> list[dict]:
    """通过 Reddit RSS 搜索一个 subreddit（带重试）"""
    url = f"https://www.reddit.com/r/{subreddit}/search.rss"
    params = {
        "q": quote(query),
        "sort": "new",
        "restrict_sr": "on",
        "limit": str(limit),
    }
    import requests as req

    for attempt in range(retries):
        try:
            resp = req.get(url, headers=BROWSER_HEADERS, params=params, timeout=15)

            if resp.status_code == 429:
                wait = (attempt + 1) * 10  # 10s, 20s, 30s
                print(f"    429 rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue

            if resp.status_code != 200:
                return []

            # 解析 Atom feed
            root = ET.fromstring(resp.content)
            results = []
            for entry in root.findall(f"{{{ATOM_NS}}}entry"):
                title_el = entry.find(f"{{{ATOM_NS}}}title")
                link_el = entry.find(f"{{{ATOM_NS}}}link")
                author_el = entry.find(f"{{{ATOM_NS}}}author")
                updated_el = entry.find(f"{{{ATOM_NS}}}updated")
                content_el = entry.find(f"{{{ATOM_NS}}}content")

                title = title_el.text if title_el is not None and title_el.text else ""
                link = link_el.get("href") if link_el is not None else ""
                author = ""
                if author_el is not None:
                    name_el = author_el.find(f"{{{ATOM_NS}}}name")
                    author = name_el.text if name_el is not None and name_el.text else ""
                updated = updated_el.text if updated_el is not None and updated_el.text else ""
                content = content_el.text if content_el is not None and content_el.text else ""

                # 从 URL 提取 post ID
                post_id = ""
                id_match = re.search(r"/comments/([a-z0-9]+)/", link)
                if id_match:
                    post_id = id_match.group(1)

                # 解析时间
                created_iso = ""
                if updated:
                    try:
                        dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                        created_iso = dt.isoformat()
                    except (ValueError, AttributeError):
                        pass

                results.append({
                    "id": f"reddit_{post_id}" if post_id else f"reddit_{hash(link)}",
                    "title": title,
                    "text": f"{title}\n\n{content[:500] if content else ''}",
                    "author_name": author,
                    "author_username": author,
                    "author_followers": 0,
                    "retweets": 0,
                    "likes": 0,
                    "replies": 0,
                    "subreddit": f"r/{subreddit}",
                    "url": link,
                    "created_at": created_iso,
                    "platform": "Reddit",
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "_raw_content": content,
                })

            return results

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(5)
            else:
                print(f"    r/{subreddit} RSS error: {e}")

    return []


def search_reddit(keywords: list[str] = None, max_results: int = None) -> list[dict]:
    """
    搜索 Reddit 上与 Nothing Account 相关的帖子（RSS 方式，免 API）

    Returns:
        统一格式的 mention 列表
    """
    if keywords is None:
        keywords = SEARCH_KEYWORDS
    if max_results is None:
        max_results = MAX_RESULTS

    all_posts = []
    seen_ids = set()

    # 精简搜索策略（控制请求量避免 429）
    priority_searches = [
        ("NothingTech", "Nothing Account"),
        ("Nothing", "Nothing Account"),
        ("NothingTech", "Nothing login"),
        ("Android", "Nothing Phone account"),
    ]

    for sr, kw in priority_searches:
        if len(all_posts) >= max_results:
            break

        print(f"  搜索 r/{sr} \"{kw}\"...")
        posts = _search_rss(sr, kw, limit=15)

        for p in posts:
            pid = p["id"]
            if pid in seen_ids:
                continue

            # 客户端过滤
            if not _is_relevant(p["title"], p.get("_raw_content", "")):
                continue

            seen_ids.add(pid)
            del p["_raw_content"]
            all_posts.append(p)

        print(f"    -> {len(posts)} raw, {len([x for x in posts if x['id'] in seen_ids])} new relevant")
        time.sleep(8.0)  # 间隔 8 秒，避免 429

    all_posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return all_posts[:max_results]


def check_reddit_status() -> dict:
    """检查 Reddit RSS 是否可访问"""
    try:
        import requests
        resp = requests.get(
            "https://www.reddit.com/r/NothingTech/search.rss",
            headers=BROWSER_HEADERS,
            params={"q": "Nothing", "limit": 1},
            timeout=15,
        )
        if resp.status_code == 200:
            return {"connected": True, "method": "RSS/Atom (no API key needed)"}
        return {"connected": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"connected": False, "error": str(e)}


if __name__ == "__main__":
    import requests  # noqa

    print("=" * 60)
    print("  Reddit 抓取器 — Nothing Account 舆情监控")
    print("  方案: RSS/Atom (免 API)")
    print("=" * 60)

    status = check_reddit_status()
    print(f"\n连接状态: {status}")

    if status["connected"]:
        print("\n搜索 Reddit...")
        posts = search_reddit()
        print(f"找到 {len(posts)} 条相关帖子")
        for i, p in enumerate(posts[:15], 1):
            print(f"  [{i}] {p['subreddit']} | ❤{p['likes']} 💬{p['replies']}")
            print(f"      {p['title'][:100]}")
            print(f"      {p['url']}")
            print()

        output_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "latest_reddit.json",
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"数据已保存: {output_path}")
