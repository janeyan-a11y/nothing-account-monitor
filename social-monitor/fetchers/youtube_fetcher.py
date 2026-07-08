"""
YouTube 数据抓取器 — 通过 YouTube Data API v3 搜索视频和评论
免费额度: 10,000 quota/天 (搜索 ~100 units/次，评论 ~1 unit/条)
"""
import json
import sys
import os
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
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")

SEARCH_QUERIES = [
    "Nothing Phone account",
    "Nothing login problem",
    "Nothing account problem",
    "Nothing sign in",
    "Nothing account delete",
]

TITLE_KEYWORDS = [
    "account", "login", "sign in", "sign-in", "signin",
    "password", "verify", "verification", "auth",
    "2FA", "two-factor", "delete account", "deactivate",
    "sign up", "sign-up", "signup", "register",
]

API_BASE = "https://www.googleapis.com/youtube/v3"


def _is_relevant(title: str, description: str = "") -> bool:
    """判断视频是否与 Nothing Account 相关"""
    combined = (title + " " + description).lower()
    for kw in TITLE_KEYWORDS:
        if kw.lower() in combined:
            return True
    return False


def _search_videos(query: str, max_results: int = 10) -> list[dict]:
    """搜索 YouTube 视频"""
    import requests

    params = {
        "part": "snippet",
        "q": query,
        "maxResults": min(max_results, 50),
        "type": "video",
        "order": "date",
        "relevanceLanguage": "en",
        "key": YOUTUBE_API_KEY,
    }

    try:
        resp = requests.get(f"{API_BASE}/search", params=params, timeout=15)
        if resp.status_code != 200:
            err = resp.json().get("error", {}).get("message", resp.text)
            print(f"    API error: {err}")
            return []

        data = resp.json()
        results = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId", "")
            title = snippet.get("title", "")
            description = snippet.get("description", "")
            channel = snippet.get("channelTitle", "")
            published = snippet.get("publishedAt", "")

            if not _is_relevant(title, description):
                continue

            results.append({
                "id": f"youtube_{video_id}",
                "title": title,
                "text": f"{title}\n\n{description[:500] if description else ''}",
                "created_at": published,
                "author_name": channel,
                "author_username": channel,
                "author_followers": 0,
                "retweets": 0,
                "likes": 0,
                "replies": 0,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "platform": "YouTube",
                "fetched_at": datetime.now(timezone.utc).isoformat(),
            })

        return results

    except Exception as e:
        print(f"    search error: {e}")
        return []


def _get_video_stats(video_ids: list[str]) -> dict:
    """批量获取视频统计数据（点赞、评论数等）"""
    import requests

    if not video_ids:
        return {}

    params = {
        "part": "statistics",
        "id": ",".join(video_ids[:50]),
        "key": YOUTUBE_API_KEY,
    }

    try:
        resp = requests.get(f"{API_BASE}/videos", params=params, timeout=15)
        if resp.status_code != 200:
            return {}

        data = resp.json()
        stats = {}
        for item in data.get("items", []):
            vid = item.get("id", "")
            stat = item.get("statistics", {})
            stats[vid] = {
                "likes": int(stat.get("likeCount", 0)),
                "replies": int(stat.get("commentCount", 0)),
                "views": int(stat.get("viewCount", 0)),
            }
        return stats
    except Exception:
        return {}


def search_youtube(keywords: list[str] = None, max_results: int = None) -> list[dict]:
    """
    搜索 YouTube 上与 Nothing Account 相关的视频

    Returns:
        统一格式的 mention 列表
    """
    if keywords is None:
        keywords = SEARCH_QUERIES
    if max_results is None:
        max_results = MAX_RESULTS

    if not YOUTUBE_API_KEY:
        print("  ⚠ YouTube API Key 未配置，跳过")
        print("  获取方式: https://console.cloud.google.com/apis/library/youtube.googleapis.com")
        return []

    all_videos = []
    seen_ids = set()

    for q in keywords[:3]:  # 限制搜索次数，省 quota
        if len(all_videos) >= max_results:
            break

        print(f"  搜索: \"{q}\"...")
        videos = _search_videos(q, max_results=10)
        for v in videos:
            vid = v["id"]
            if vid in seen_ids:
                continue
            seen_ids.add(vid)
            all_videos.append(v)

        time.sleep(1.0)

    # 批量获取统计数据
    if all_videos:
        video_ids = [v["id"].replace("youtube_", "") for v in all_videos]
        stats = _get_video_stats(video_ids)
        for v in all_videos:
            vid = v["id"].replace("youtube_", "")
            if vid in stats:
                v["likes"] = stats[vid]["likes"]
                v["replies"] = stats[vid]["replies"]
                v["views"] = stats[vid]["views"]

    all_videos.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return all_videos[:max_results]


def check_youtube_status() -> dict:
    """检查 YouTube API 是否可用"""
    if not YOUTUBE_API_KEY:
        return {"connected": False, "error": "未配置 YOUTUBE_API_KEY"}
    import requests
    try:
        resp = requests.get(
            f"{API_BASE}/search",
            params={"part": "snippet", "q": "Nothing", "maxResults": 1, "key": YOUTUBE_API_KEY},
            timeout=15,
        )
        if resp.status_code == 200:
            return {"connected": True, "method": "YouTube Data API v3 (free quota)"}
        err = resp.json().get("error", {}).get("message", f"HTTP {resp.status_code}")
        return {"connected": False, "error": err}
    except Exception as e:
        return {"connected": False, "error": str(e)}


if __name__ == "__main__":
    import requests  # noqa

    print("=" * 60)
    print("  YouTube 抓取器 — Nothing Account 舆情监控")
    print("=" * 60)

    status = check_youtube_status()
    print(f"\n连接状态: {status}")

    if status["connected"]:
        print("\n搜索 YouTube...")
        videos = search_youtube()
        print(f"\n找到 {len(videos)} 个相关视频:")
        print("-" * 60)
        for i, v in enumerate(videos, 1):
            print(f"\n  [{i}] {v['title'][:90]}")
            print(f"      频道: {v['author_name']}  |  ❤{v['likes']}  💬{v['replies']}")
            print(f"      {v['url']}")
            print(f"      {v['created_at'][:10]}")

        output_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "latest_youtube.json",
        )
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)
        print(f"\n数据已保存: {output_path}")
