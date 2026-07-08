"""
Bluesky 数据抓取器 — AT Protocol 公开 API
策略: 精确短语搜索确保品牌匹配 + 账号关键词过滤
"""
import json, sys, os, time
from datetime import datetime, timezone

if sys.platform == "win32":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MAX_RESULTS

# 精确短语搜索
SEARCH_QUERIES = [
    '"Nothing Phone"',
    '"Nothing OS"',
    '"Nothing" account',
    '"Nothing" login',
]

# 账号 + 品牌相关关键词
ACCOUNT_KW = [
    "account", "login", "sign in", "sign-in", "signin",
    "password", "verify", "verification", "auth",
    "delete account", "deactivate", "register", "2fa",
    "sign up", "sign-up", "signup",
]

# 品牌校验 — 必须是 Nothing 品牌 + 账号关键词
BRAND_MARKERS = [
    "nothing phone", "nothing os", "nothingos",
    "nothing tech", "#nothing",
]

SEARCH_URL = "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts"


def _is_relevant(text: str) -> bool:
    """三层过滤: 品牌 + 账号 + 排除噪音"""
    t = text.lower()
    # 1. 必须是 Nothing 品牌相关
    brand = any(k in t for k in BRAND_MARKERS)
    if not brand: return False
    # 2. 必须有账号相关讨论
    acct = any(k in t for k in ACCOUNT_KW)
    if not acct: return False
    # 3. 排除明显噪音
    noise = ["trump", "biden", "maga", "nasa", "satellite", "president"]
    if any(n in t for n in noise): return False
    return True


def _parse_time(bsky_time: str) -> str:
    if not bsky_time: return ""
    try: return bsky_time.replace("Z", "+00:00")
    except: return bsky_time


def _search_posts(query: str, limit: int = 25) -> list[dict]:
    import requests
    try:
        resp = requests.get(SEARCH_URL,
            params={"q": query, "limit": min(limit, 100), "sort": "latest"},
            timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
        results = []
        for post in data.get("posts", []):
            author = post.get("author", {})
            record = post.get("record", {})
            text = record.get("text", "")
            if not _is_relevant(text):
                continue
            author_handle = author.get("handle", "")
            post_uri = post.get("uri", "")
            post_id = post_uri.split("/")[-1] if post_uri else ""
            created_at = _parse_time(record.get("createdAt", "") or post.get("indexedAt", ""))
            results.append({
                "id": f"bsky_{post_id}" if post_id else f"bsky_{hash(post_uri)}",
                "title": text[:120].replace("\n"," "),
                "text": text[:500] if text else "",
                "created_at": created_at,
                "author_name": author.get("displayName", "") or author_handle,
                "author_username": author_handle,
                "author_followers": author.get("followersCount", 0),
                "retweets": post.get("repostCount", 0),
                "likes": post.get("likeCount", 0),
                "replies": post.get("replyCount", 0),
                "url": f"https://bsky.app/profile/{author_handle}/post/{post_id}" if author_handle and post_id else "",
                "platform": "Bluesky",
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })
        return results
    except Exception as e:
        print(f"    search error: {e}")
        return []


def search_bluesky(keywords=None, max_results=None) -> list[dict]:
    if keywords is None: keywords = SEARCH_QUERIES
    if max_results is None: max_results = MAX_RESULTS
    all_posts, seen_ids = [], set()
    for q in keywords:
        if len(all_posts) >= max_results: break
        print(f"  搜索: {q}...")
        for p in _search_posts(q, limit=20):
            if p["id"] in seen_ids: continue
            seen_ids.add(p["id"]); all_posts.append(p)
        time.sleep(0.5)
    all_posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return all_posts[:max_results]


def check_bluesky_status() -> dict:
    import requests
    try:
        resp = requests.get(SEARCH_URL, params={"q": "Nothing Phone", "limit": 1}, timeout=15)
        if resp.status_code == 200:
            return {"connected": True, "method": "AT Protocol public API"}
        return {"connected": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"connected": False, "error": str(e)}


if __name__ == "__main__":
    import requests as _  # noqa
    print("=" * 60)
    print("  Bluesky 抓取器 — Nothing Account 舆情监控")
    print("  策略: 精确短语 + 账号关键词双过滤")
    print("=" * 60)
    status = check_bluesky_status()
    print(f"\n连接: {status}")
    if status["connected"]:
        posts = search_bluesky()
        print(f"\n找到 {len(posts)} 条相关帖子:")
        print("-" * 60)
        for i, p in enumerate(posts, 1):
            text = p["text"].replace("\n", " ")[:100]
            print(f"  [{i}] @{p['author_username']} | {p['created_at'][:16]}")
            print(f"      ❤{p['likes']} 🔄{p['retweets']} 💬{p['replies']}")
            print(f"      {text}")
            print(f"      {p['url']}")
            print()
        out = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "latest_bluesky.json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"已保存: {out}")
