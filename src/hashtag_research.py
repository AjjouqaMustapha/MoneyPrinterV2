"""
Auto-Hashtag Research Module
Researches and generates optimized hashtags for YouTube Shorts and TikTok.
Combines LLM-generated hashtags with trending data.
"""

import requests
import json
import os
import time
from typing import List
from config import ROOT_DIR, _load_config
from llm_provider import generate_structured
from status import info, success, warning

HASHTAG_CACHE = os.path.join(ROOT_DIR, ".mp", "hashtag_cache.json")

# Known high-performing hashtags by niche
NICHE_HASHTAGS = {
    "scary": ["#scary", "#horror", "#creepy", "#scarystory", "#fyp", "#viral", "#storytime", "#darkside"],
    "facts": ["#facts", "#didyouknow", "#interesting", "#mindblown", "#funfacts", "#viral", "#fyp", "#education"],
    "motivation": ["#motivation", "#mindset", "#success", "#grindset", "#entrepreneur", "#discipline", "#fyp"],
    "psychology": ["#psychology", "#darkpsychology", "#manipulation", "#mindgames", "#bodylanguage", "#fyp"],
    "tech": ["#tech", "#technology", "#coding", "#programming", "#ai", "#gadgets", "#innovation", "#fyp"],
    "finance": ["#finance", "#money", "#investing", "#wealth", "#passive", "#stocks", "#crypto", "#fyp"],
    "cooking": ["#cooking", "#recipe", "#food", "#foodtok", "#chef", "#easyrecipe", "#fyp", "#viral"],
    "fitness": ["#fitness", "#gym", "#workout", "#gains", "#health", "#transformation", "#fyp"],
    "gaming": ["#gaming", "#gamer", "#games", "#gameplay", "#twitch", "#esports", "#fyp"],
    "history": ["#history", "#historical", "#war", "#ancient", "#didyouknow", "#education", "#fyp"],
}


def get_base_hashtags(niche: str) -> List[str]:
    """
    Returns base hashtags for a niche from the known database.

    Args:
        niche: Content niche

    Returns:
        List of hashtag strings
    """
    niche_lower = niche.lower()
    for key, tags in NICHE_HASHTAGS.items():
        if key in niche_lower:
            return tags
    return ["#fyp", "#viral", "#shorts", "#trending"]


def generate_hashtags(title: str, script: str, niche: str, platform: str = "youtube") -> List[str]:
    """
    Generates optimized hashtags using LLM based on video content.

    Args:
        title: Video title
        script: Video script
        niche: Content niche
        platform: Target platform ("youtube" or "tiktok")

    Returns:
        List of hashtag strings (10-15 hashtags)
    """
    max_tags = 15 if platform == "tiktok" else 10

    prompt = f"""Generate {max_tags} optimized hashtags for this {platform} short video.

Title: {title}
Script preview: {script[:300]}
Niche: {niche}

Rules:
- Mix popular (high volume) and niche (less competition) hashtags
- Include 2-3 trending/viral hashtags (#fyp, #viral, etc.)
- Include 3-4 niche-specific hashtags
- Include 2-3 content-specific hashtags based on the actual video
- All hashtags must start with #
- No spaces within hashtags
- For TikTok: use more trending hashtags
- For YouTube: use more descriptive/search-friendly hashtags

Return a JSON object with:
- "hashtags": array of hashtag strings
- "primary": the single most important hashtag for discoverability
- "reasoning": one sentence about the strategy

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)
        hashtags = result.get("hashtags", [])

        # Ensure all start with #
        hashtags = [h if h.startswith("#") else f"#{h}" for h in hashtags]

        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for h in hashtags:
            h_lower = h.lower()
            if h_lower not in seen:
                seen.add(h_lower)
                unique.append(h)

        success(f" => Generated {len(unique)} hashtags for {platform}")
        return unique[:max_tags]

    except Exception as e:
        warning(f"Hashtag generation failed: {e}")
        return get_base_hashtags(niche)


def get_trending_hashtags(platform: str = "youtube") -> List[str]:
    """
    Returns currently trending hashtags.
    Uses cached data or LLM knowledge as proxy for trending data.

    Args:
        platform: "youtube" or "tiktok"

    Returns:
        List of trending hashtags
    """
    # Check cache first
    cache = _load_cache()
    cache_key = f"trending_{platform}"
    if cache_key in cache:
        age = time.time() - cache[cache_key].get("timestamp", 0)
        if age < 24 * 3600:  # 24 hour cache
            return cache[cache_key]["hashtags"]

    prompt = f"""What are the top 20 trending hashtags on {platform} Shorts right now?
Focus on hashtags that are currently viral and getting millions of views.
Include a mix of evergreen viral hashtags and recent trending ones.

Return a JSON object with:
- "hashtags": array of 20 hashtag strings

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)
        hashtags = result.get("hashtags", [])

        # Cache the results
        cache[cache_key] = {
            "hashtags": hashtags,
            "timestamp": time.time(),
        }
        _save_cache(cache)

        return hashtags
    except Exception:
        return ["#fyp", "#viral", "#trending", "#shorts", "#foryou"]


def format_hashtag_string(hashtags: List[str], max_chars: int = 500) -> str:
    """
    Formats hashtags into a string suitable for video descriptions.

    Args:
        hashtags: List of hashtag strings
        max_chars: Maximum character limit

    Returns:
        Formatted hashtag string
    """
    result = " ".join(hashtags)
    if len(result) > max_chars:
        # Trim to fit
        trimmed = []
        current_len = 0
        for tag in hashtags:
            if current_len + len(tag) + 1 <= max_chars:
                trimmed.append(tag)
                current_len += len(tag) + 1
            else:
                break
        result = " ".join(trimmed)

    return result


def _load_cache() -> dict:
    if not os.path.exists(HASHTAG_CACHE):
        return {}
    try:
        with open(HASHTAG_CACHE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(data: dict):
    os.makedirs(os.path.dirname(HASHTAG_CACHE), exist_ok=True)
    with open(HASHTAG_CACHE, "w") as f:
        json.dump(data, f, indent=2)
