import os
import json
from datetime import datetime
from config import ROOT_DIR
from status import info, warning, success


ANALYTICS_PATH = os.path.join(ROOT_DIR, ".mp", "analytics.json")


def track_video(video_data: dict) -> None:
    """
    Tracks a generated/uploaded video for analytics.

    Args:
        video_data: Dict with title, description, niche, url, etc.
    """
    analytics = _load_analytics()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "title": video_data.get("title", ""),
        "niche": video_data.get("niche", ""),
        "url": video_data.get("url", ""),
        "platform": video_data.get("platform", "youtube"),
        "views": 0,
        "likes": 0,
        "comments": 0,
        "estimated_revenue": 0.0,
    }

    analytics["videos"].append(entry)
    analytics["total_videos"] = len(analytics["videos"])

    _save_analytics(analytics)
    info(f" => Tracked video: {entry['title'][:50]}")


def get_analytics_summary() -> dict:
    """
    Returns a summary of all tracked videos.
    """
    analytics = _load_analytics()
    videos = analytics.get("videos", [])

    if not videos:
        return {"total_videos": 0, "niches": {}, "platforms": {}}

    niches = {}
    platforms = {}

    for v in videos:
        niche = v.get("niche", "unknown")
        platform = v.get("platform", "youtube")

        niches[niche] = niches.get(niche, 0) + 1
        platforms[platform] = platforms.get(platform, 0) + 1

    return {
        "total_videos": len(videos),
        "niches": niches,
        "platforms": platforms,
        "total_views": sum(v.get("views", 0) for v in videos),
        "total_likes": sum(v.get("likes", 0) for v in videos),
        "estimated_total_revenue": sum(v.get("estimated_revenue", 0) for v in videos),
    }


def update_video_stats(video_url: str, views: int = 0, likes: int = 0, comments: int = 0, revenue: float = 0.0) -> None:
    """
    Updates stats for a tracked video (for manual or API-based updates).
    """
    analytics = _load_analytics()

    for video in analytics["videos"]:
        if video.get("url") == video_url:
            video["views"] = views
            video["likes"] = likes
            video["comments"] = comments
            video["estimated_revenue"] = revenue
            break

    _save_analytics(analytics)


def estimate_revenue(views: int, cpm: float = 2.0) -> float:
    """
    Estimates revenue based on views and CPM.
    Default CPM is $2.00 (conservative estimate for YouTube Shorts).

    Args:
        views: Number of video views
        cpm: Cost per mille (per 1000 views)

    Returns:
        Estimated revenue in USD
    """
    return round((views / 1000) * cpm, 2)


def _load_analytics() -> dict:
    if not os.path.exists(ANALYTICS_PATH):
        return {"videos": [], "total_videos": 0}
    with open(ANALYTICS_PATH, "r") as f:
        return json.load(f)


def _save_analytics(analytics: dict) -> None:
    with open(ANALYTICS_PATH, "w") as f:
        json.dump(analytics, f, indent=2)
