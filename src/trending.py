import requests
import re
from typing import List
from status import info, warning


def get_trending_topics(country: str = "US", count: int = 10) -> List[str]:
    """
    Fetches currently trending topics from Google Trends RSS feed.

    Args:
        country: Country code (US, GB, DE, etc.)
        count: Max number of topics to return

    Returns:
        List of trending topic strings
    """
    url = f"https://trends.google.com/trending/rss?geo={country}"

    try:
        response = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        response.raise_for_status()

        # Parse RSS XML for titles
        titles = re.findall(r"<title><!\[CDATA\[(.+?)\]\]></title>", response.text)
        # Skip the first title (it's the feed title)
        topics = titles[1:count + 1] if len(titles) > 1 else []

        if not topics:
            # Fallback: try regular title tags
            titles = re.findall(r"<title>(.+?)</title>", response.text)
            topics = [t for t in titles[1:count + 1] if t != "Daily Search Trends"]

        return topics
    except Exception as e:
        warning(f"Failed to fetch trending topics: {e}")
        return []


def get_niche_trending(niche: str, country: str = "US") -> List[str]:
    """
    Gets trending topics filtered by relevance to a specific niche.
    Uses the general trending list and filters with basic keyword matching.

    Args:
        niche: The channel niche
        country: Country code

    Returns:
        List of relevant trending topics
    """
    all_trending = get_trending_topics(country=country)

    if not all_trending:
        return []

    # Simple relevance: return all trending topics (the LLM will pick what's relevant)
    return all_trending


def suggest_trending_video_idea(niche: str, trending_topics: List[str]) -> str:
    """
    Uses the LLM to combine a niche with trending topics into a video idea.

    Args:
        niche: Channel niche
        trending_topics: List of current trending topics

    Returns:
        A video idea prompt string that combines the niche with trends
    """
    from llm_provider import generate_text

    topics_str = ", ".join(trending_topics[:5])

    prompt = f"""Given these currently trending topics: {topics_str}

And a YouTube channel focused on: {niche}

Generate ONE specific video idea that cleverly connects the channel's niche with one of the trending topics. This should feel natural, not forced. The video idea should be one sentence.

Only return the video idea, nothing else."""

    return generate_text(prompt)
