"""
Posting Analytics Module
Tracks posting times and performance to determine optimal upload windows.
Learns from YOUR audience data to recommend the best posting times.
"""

import os
import json
from datetime import datetime, timedelta
from typing import List
from collections import defaultdict
from config import ROOT_DIR
from status import info, success, warning

ANALYTICS_FILE = os.path.join(ROOT_DIR, ".mp", "posting_analytics.json")


def _load_analytics() -> dict:
    if not os.path.exists(ANALYTICS_FILE):
        return {"posts": [], "settings": {}}
    try:
        with open(ANALYTICS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"posts": [], "settings": {}}


def _save_analytics(data: dict):
    os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_post(
    platform: str,
    title: str,
    niche: str,
    posted_at: str = None,
    video_path: str = None,
    url: str = None,
) -> dict:
    """
    Logs a new post for analytics tracking.

    Args:
        platform: Platform name (youtube, tiktok, instagram)
        title: Video title
        niche: Content niche
        posted_at: ISO datetime string (default: now)
        video_path: Path to the video file
        url: URL of the uploaded video

    Returns:
        The logged post entry
    """
    if posted_at is None:
        posted_at = datetime.now().isoformat()

    dt = datetime.fromisoformat(posted_at)

    entry = {
        "platform": platform,
        "title": title,
        "niche": niche,
        "posted_at": posted_at,
        "day_of_week": dt.strftime("%A"),
        "hour": dt.hour,
        "video_path": video_path,
        "url": url,
        "metrics": {
            "views_1h": 0,
            "views_24h": 0,
            "views_7d": 0,
            "likes": 0,
            "comments": 0,
            "shares": 0,
        },
    }

    analytics = _load_analytics()
    analytics["posts"].append(entry)
    _save_analytics(analytics)

    info(f" => Post logged: {platform} - {title} at {dt.strftime('%A %H:%M')}")
    return entry


def update_metrics(post_index: int, metrics: dict):
    """
    Updates metrics for a logged post.

    Args:
        post_index: Index of the post in the analytics list
        metrics: Dict of metric updates
    """
    analytics = _load_analytics()
    if 0 <= post_index < len(analytics["posts"]):
        analytics["posts"][post_index]["metrics"].update(metrics)
        _save_analytics(analytics)


def get_best_posting_times(platform: str = None, top_n: int = 5) -> List[dict]:
    """
    Analyzes past posts to find the best posting times.

    Args:
        platform: Filter by platform (None for all)
        top_n: Number of top time slots to return

    Returns:
        List of time slot dicts sorted by average performance
    """
    analytics = _load_analytics()
    posts = analytics.get("posts", [])

    if platform:
        posts = [p for p in posts if p["platform"] == platform]

    if len(posts) < 3:
        info(" => Not enough data for analysis (need at least 3 posts)")
        return _get_default_times()

    # Group by day+hour
    time_slots = defaultdict(list)
    for post in posts:
        key = f"{post['day_of_week']}_{post['hour']}"
        views = post["metrics"].get("views_24h", 0)
        time_slots[key].append(views)

    # Calculate averages
    results = []
    for key, views_list in time_slots.items():
        day, hour = key.rsplit("_", 1)
        avg_views = sum(views_list) / len(views_list)
        results.append({
            "day": day,
            "hour": int(hour),
            "avg_views_24h": avg_views,
            "sample_size": len(views_list),
            "formatted": f"{day} at {int(hour):02d}:00",
        })

    results.sort(key=lambda x: x["avg_views_24h"], reverse=True)

    if results:
        success(f" => Best time: {results[0]['formatted']} (avg {results[0]['avg_views_24h']:.0f} views)")

    return results[:top_n]


def get_best_niche_performance() -> List[dict]:
    """
    Analyzes which niches/topics perform best.

    Returns:
        List of niche performance dicts
    """
    analytics = _load_analytics()
    posts = analytics.get("posts", [])

    niche_data = defaultdict(list)
    for post in posts:
        niche = post.get("niche", "unknown")
        views = post["metrics"].get("views_24h", 0)
        niche_data[niche].append(views)

    results = []
    for niche, views_list in niche_data.items():
        results.append({
            "niche": niche,
            "avg_views": sum(views_list) / len(views_list),
            "total_posts": len(views_list),
            "best_views": max(views_list),
        })

    results.sort(key=lambda x: x["avg_views"], reverse=True)
    return results


def get_posting_summary() -> dict:
    """
    Returns a summary of all posting activity.

    Returns:
        Summary dict with total posts, platforms, time range, etc.
    """
    analytics = _load_analytics()
    posts = analytics.get("posts", [])

    if not posts:
        return {"total_posts": 0, "message": "No posts tracked yet"}

    platforms = defaultdict(int)
    total_views = 0
    for post in posts:
        platforms[post["platform"]] += 1
        total_views += post["metrics"].get("views_24h", 0)

    return {
        "total_posts": len(posts),
        "platforms": dict(platforms),
        "total_views_tracked": total_views,
        "avg_views_per_post": total_views / len(posts) if posts else 0,
        "first_post": posts[0]["posted_at"] if posts else None,
        "last_post": posts[-1]["posted_at"] if posts else None,
    }


def _get_default_times() -> List[dict]:
    """Returns default best posting times based on general YouTube data."""
    return [
        {"day": "Friday", "hour": 17, "formatted": "Friday at 17:00", "avg_views_24h": 0, "sample_size": 0},
        {"day": "Saturday", "hour": 11, "formatted": "Saturday at 11:00", "avg_views_24h": 0, "sample_size": 0},
        {"day": "Wednesday", "hour": 18, "formatted": "Wednesday at 18:00", "avg_views_24h": 0, "sample_size": 0},
        {"day": "Thursday", "hour": 15, "formatted": "Thursday at 15:00", "avg_views_24h": 0, "sample_size": 0},
        {"day": "Tuesday", "hour": 14, "formatted": "Tuesday at 14:00", "avg_views_24h": 0, "sample_size": 0},
    ]
