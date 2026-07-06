"""
Nothing Community 抓取器 — 通过 Flarum 公开 API 搜索讨论
API 无需认证，端点: https://nothing.community/api/discussions
"""
import json
import sys
import os
import re
import time
from datetime import datetime, timezone
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
BASE_URL = "https://nothing.community"
API_BASE = f"{BASE_URL}/api"
DISCUSSION_URL = f"{BASE_URL}/d"

SEARCH_QUERIES = [
    "Nothing account",
    "account error",
    "login account",
    "sign in account",
    "Essential Space account",
    "account authorization",
    "account password",
    "account verify",
    "Nothing login",
    "account sync",
]

# 标题相关性过滤关键词（必须出现在标题中）
TITLE_KEYWORDS = [
    "account", "login", "sign in", "sign-in", "signin",
    "password", "verify", "verification", "auth",
    "sign up", "sign-up", "signup",
    "2FA", "two-factor", "two factor",
    "gmail",
    "essential space",  # Essential Space 是 Nothing Account 核心功能
]

# 内容关键词（标题匹配后再看内容，避免无意义帖子）
CONTENT_KEYWORDS = [
    "account", "login", "sign in", "auth", "password",
    "verify", "verification", "credential",
]

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def _strip_html(html_text) -> str:
    """去除 HTML 标签，保留纯文本"""
    if not html_text or not isinstance(html_text, str):
        return ""
    # 处理换行
    text = re.sub(r"<br\s*/?>", "\n", html_text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n", text)
    # 去标签
    text = re.sub(r"<[^>]+>", "", text)
    # 压缩空白
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def _is_relevant(title: str, content: str = "") -> bool:
    """判断帖子是否与 Nothing Account 相关 — 标题必须命中"""
    title_lower = title.lower()

    # 标题必须包含至少一个账号关键词
    title_match = any(kw in title_lower for kw in TITLE_KEYWORDS)
    if not title_match:
        return False

    # 额外：内容中也要有实质性讨论（排除只在标题碰巧出现的情况）
    content_lower = content.lower() if content else ""
    content_match = any(kw in content_lower for kw in CONTENT_KEYWORDS)
    if not content_match:
        # 如果标题明确提到 account/login/auth，即使内容短也算
        strong_title = any(kw in title_lower for kw in ["account", "login", "sign in", "auth", "gmail"])
        if not strong_title:
            return False

    return True


def _search_discussions(query: str, limit: int = 10) -> list[dict]:
    """搜索讨论列表（含首帖内容）"""
    import requests

    params = {
        "filter[q]": query,
        "sort": "-createdAt",
        "page[limit]": limit,
        "include": "user,firstPost",
    }

    try:
        resp = requests.get(
            f"{API_BASE}/discussions",
            headers=BROWSER_HEADERS,
            params=params,
            timeout=15,
        )
        if resp.status_code != 200:
            return []

        data = resp.json()

        # 解析 included（用户和首帖）
        users = {}
        posts = {}
        for inc in data.get("included", []):
            if inc["type"] == "users":
                attrs = inc.get("attributes", {})
                users[inc["id"]] = {
                    "username": attrs.get("username", ""),
                    "displayName": attrs.get("displayName", ""),
                    "avatarUrl": attrs.get("avatarUrl", ""),
                }
            elif inc["type"] == "posts":
                post_attrs = inc.get("attributes", {})
                posts[inc["id"]] = {
                    "contentHtml": post_attrs.get("contentHtml", ""),
                    "content": _strip_html(post_attrs.get("contentHtml", "")),
                }

        # 解析讨论
        results = []
        for disc in data.get("data", []):
            attrs = disc.get("attributes", {})
            rels = disc.get("relationships", {})
            disc_id = disc["id"]

            # 获取作者
            user_data = rels.get("user", {}).get("data", {})
            user_id = user_data.get("id") if user_data else None
            user = users.get(user_id, {}) if user_id else {}

            # 获取首帖内容
            first_post_data = rels.get("firstPost", {}).get("data", {})
            post_id = first_post_data.get("id") if first_post_data else None
            post = posts.get(post_id, {}) if post_id else {}
            content_html = post.get("contentHtml", "")
            content_text = post.get("content", "")

            title = attrs.get("title", "")
            slug = attrs.get("slug", "")
            created_at = attrs.get("createdAt", "")

            # 客户端相关性过滤
            if not _is_relevant(title, content_text):
                continue

            results.append({
                "id": f"community_{disc_id}",
                "title": title,
                "text": f"{title}\n\n{content_text[:500] if content_text else ''}",
                "content_full": content_text[:1000] if content_text else "",
                "created_at": created_at,
                "author_name": user.get("displayName", "") or user.get("username", ""),
                "author_username": user.get("username", ""),
                "author_followers": 0,
                "retweets": 0,
                "likes": 0,
                "replies": attrs.get("commentCount", 0),
                "views": attrs.get("viewCount", 0) or 0,
                "url": f"{DISCUSSION_URL}/{disc_id}-{slug}",
                "platform": "Nothing Community",
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })

        return results

    except Exception as e:
        print(f"    search error: {e}")
        return []


def search_community(keywords: list[str] = None, max_results: int = None) -> list[dict]:
    """
    搜索 Nothing Community 上与账户相关的讨论

    Returns:
        统一格式的 mention 列表
    """
    if keywords is None:
        keywords = SEARCH_QUERIES
    if max_results is None:
        max_results = MAX_RESULTS

    all_posts = []
    seen_ids = set()

    for q in keywords:
        if len(all_posts) >= max_results:
            break

        posts = _search_discussions(q, limit=10)
        for p in posts:
            pid = p["id"]
            if pid in seen_ids:
                continue
            seen_ids.add(pid)
            all_posts.append(p)

        time.sleep(1.0)  # 礼貌间隔

    all_posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return all_posts[:max_results]


def check_community_status() -> dict:
    """检查 Nothing Community API 是否可访问"""
    import requests
    try:
        resp = requests.get(
            f"{API_BASE}/discussions",
            headers=BROWSER_HEADERS,
            params={"page[limit]": 1},
            timeout=15,
        )
        if resp.status_code == 200:
            return {"connected": True, "method": "Flarum public API (no auth needed)"}
        return {"connected": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"connected": False, "error": str(e)}


if __name__ == "__main__":
    import requests  # noqa

    print("=" * 60)
    print("  Nothing Community 抓取器 — Nothing Account 舆情监控")
    print("  方案: Flarum Public API")
    print("=" * 60)

    status = check_community_status()
    print(f"\n连接状态: {status}")

    if status["connected"]:
        print("\n搜索 Nothing Community...")
        posts = search_community()
        print(f"\n找到 {len(posts)} 条相关讨论:")
        print("-" * 60)
        for i, p in enumerate(posts, 1):
            print(f"\n  [{i}] {p['title'][:100]}")
            print(f"      作者: {p['author_name']}  |  回复: {p['replies']}  |  {p['created_at'][:10]}")
            print(f"      {p['url']}")
            if p.get("content_full"):
                preview = p["content_full"][:150]
                print(f"      > {preview}")

        output_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "latest_community.json",
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存: {output_path}")
