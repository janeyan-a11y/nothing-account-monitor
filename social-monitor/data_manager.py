"""
数据管理器 — 读取、去重、存储各平台抓取的提及
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA_FILE


def load_existing() -> list[dict]:
    """加载已有的 mentions 数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_mentions(mentions: list[dict]) -> None:
    """保存全量 mentions（覆盖写）"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(mentions, f, ensure_ascii=False, indent=2)


def merge_new(existing: list[dict], new_items: list[dict]) -> tuple[list[dict], int]:
    """
    合并新旧数据，按 id 去重，返回 (全量列表, 新增数量)

    保留历史数据，只追加新条目。
    """
    existing_ids = {item["id"] for item in existing}
    added_count = 0

    for item in new_items:
        if item["id"] not in existing_ids:
            existing.append(item)
            existing_ids.add(item["id"])
            added_count += 1

    # 按时间倒序排列
    existing.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return existing, added_count


def get_stats(mentions: list[dict]) -> dict:
    """生成统计摘要"""
    if not mentions:
        return {
            "total": 0,
            "today": 0,
            "by_platform": {},
            "avg_likes": 0,
            "top_authors": [],
            "latest_fetch": None,
        }

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    # 按平台统计
    by_platform = {}
    for m in mentions:
        p = m.get("platform", "unknown")
        by_platform[p] = by_platform.get(p, 0) + 1

    # 今日新增
    today_count = sum(
        1 for m in mentions if m.get("created_at", "")[:10] == today_str
    )

    # 平均点赞
    likes = [m.get("likes", 0) for m in mentions]
    avg_likes = round(sum(likes) / len(likes), 1) if likes else 0

    # Top 作者（按粉丝数）
    authors = {}
    for m in mentions:
        name = m.get("author_name", "unknown")
        if name not in authors:
            authors[name] = {
                "name": name,
                "username": m.get("author_username", ""),
                "followers": m.get("author_followers", 0),
                "count": 0,
            }
        authors[name]["count"] += 1
    top_authors = sorted(
        authors.values(), key=lambda x: x["followers"], reverse=True
    )[:10]

    return {
        "total": len(mentions),
        "today": today_count,
        "by_platform": by_platform,
        "avg_likes": avg_likes,
        "top_authors": top_authors,
        "latest_fetch": max(m.get("fetched_at", "") for m in mentions) if mentions else None,
    }


if __name__ == "__main__":
    # 测试：打印当前数据摘要
    existing = load_existing()
    print(f"现有记录: {len(existing)} 条")
    stats = get_stats(existing)
    print(json.dumps(stats, ensure_ascii=False, indent=2))
