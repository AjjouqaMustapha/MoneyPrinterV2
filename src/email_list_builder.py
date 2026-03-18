import os
import json
from datetime import datetime
from config import ROOT_DIR, _load_config
from llm_provider import generate_text
from status import info, success, warning

EMAIL_LIST_PATH = os.path.join(ROOT_DIR, ".mp", "email_list.json")


def generate_cta(niche: str, video_title: str) -> str:
    """
    Generates a Call-To-Action text for video descriptions to build an email list.

    Args:
        niche: Channel niche
        video_title: Video title for context

    Returns:
        CTA text to include in video description
    """
    prompt = f"""Write a short Call-To-Action (CTA) for a YouTube video description.
The CTA should encourage viewers to subscribe or follow for more content.

Niche: {niche}
Video: {video_title}

Requirements:
- 2-3 lines max
- Include a compelling reason to subscribe
- Use line breaks for readability
- Include relevant emojis sparingly
- Do NOT include fake links or placeholder URLs

Only return the CTA text, nothing else."""

    try:
        return generate_text(prompt)
    except Exception as e:
        warning(f"CTA generation failed: {e}")
        return f"Subscribe for more {niche} content! New videos daily."


def generate_description_with_cta(description: str, niche: str, video_title: str,
                                   links: dict = None) -> str:
    """
    Enhances a video description with CTA, links, and engagement hooks.

    Args:
        description: Original video description
        niche: Channel niche
        video_title: Video title
        links: Optional dict of links (e.g., {"website": "...", "twitter": "..."})

    Returns:
        Enhanced description with CTA
    """
    cta = generate_cta(niche, video_title)

    enhanced = description.strip()
    enhanced += "\n\n---\n"
    enhanced += cta

    if links:
        enhanced += "\n\n"
        for label, url in links.items():
            enhanced += f"{label}: {url}\n"

    enhanced += "\n\n#Shorts"

    return enhanced


def track_subscriber(source: str, platform: str = "youtube") -> None:
    """
    Tracks a subscriber/signup for analytics.

    Args:
        source: Where the subscriber came from (video URL or title)
        platform: Platform (youtube, tiktok, etc.)
    """
    data = _load_list()

    data["subscribers"].append({
        "source": source,
        "platform": platform,
        "timestamp": datetime.now().isoformat(),
    })
    data["total"] = len(data["subscribers"])

    _save_list(data)


def get_list_stats() -> dict:
    """Returns email list / subscriber stats."""
    data = _load_list()
    return {
        "total": data.get("total", 0),
        "by_platform": _count_by_key(data.get("subscribers", []), "platform"),
        "recent": data.get("subscribers", [])[-5:],
    }


def _count_by_key(items: list, key: str) -> dict:
    counts = {}
    for item in items:
        val = item.get(key, "unknown")
        counts[val] = counts.get(val, 0) + 1
    return counts


def _load_list() -> dict:
    if not os.path.exists(EMAIL_LIST_PATH):
        return {"subscribers": [], "total": 0}
    with open(EMAIL_LIST_PATH, "r") as f:
        return json.load(f)


def _save_list(data: dict):
    with open(EMAIL_LIST_PATH, "w") as f:
        json.dump(data, f, indent=2)
