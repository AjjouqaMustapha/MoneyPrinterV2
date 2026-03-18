"""
Reddit Content Scraper Module
Scrapes top posts from subreddits as content source for video ideas.
Uses Reddit's public JSON API (no authentication needed).
"""

import requests
import json
import os
import time
from datetime import datetime
from config import ROOT_DIR, get_verbose
from status import info, success, warning

REDDIT_CACHE = os.path.join(ROOT_DIR, ".mp", "reddit_cache.json")

# Popular subreddits mapped to content niches
NICHE_SUBREDDITS = {
    "facts": ["todayilearned", "Damnthatsinteresting", "interestingasfuck", "mildlyinteresting"],
    "scary": ["nosleep", "creepypasta", "LetsNotMeet", "TwoSentenceHorror", "shortscarystories"],
    "motivation": ["GetMotivated", "selfimprovement", "Stoicism", "DecidingToBeBetter"],
    "psychology": ["psychology", "coolguides", "LifeProTips", "socialskills"],
    "tech": ["technology", "Futurology", "gadgets", "programming"],
    "science": ["science", "space", "EverythingScience", "askscience"],
    "finance": ["personalfinance", "financialindependence", "investing", "wallstreetbets"],
    "cooking": ["Cooking", "recipes", "foodhacks", "MealPrepSunday"],
    "history": ["history", "HistoryMemes", "todayilearned", "AskHistorians"],
    "relationship": ["relationship_advice", "AskMen", "AskWomen", "dating_advice"],
    "funny": ["AskReddit", "Showerthoughts", "unpopularopinion", "memes"],
    "health": ["Health", "Fitness", "nutrition", "loseit"],
    "travel": ["travel", "solotravel", "backpacking", "EarthPorn"],
    "gaming": ["gaming", "Games", "pcgaming", "truegaming"],
    "business": ["Entrepreneur", "startups", "smallbusiness", "SideProject"],
}

HEADERS = {
    "User-Agent": "MoneyPrinterV2/1.0 (Content Research Bot)"
}


def scrape_subreddit(
    subreddit: str,
    sort: str = "top",
    time_filter: str = "week",
    limit: int = 25,
) -> list:
    """
    Scrapes posts from a subreddit using Reddit's public JSON API.

    Args:
        subreddit: Subreddit name (without r/)
        sort: Sort by: hot, top, new, rising
        time_filter: Time filter for 'top': hour, day, week, month, year, all
        limit: Max posts to fetch (max 100)

    Returns:
        List of post dicts with title, text, score, url, comments
    """
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json"
    params = {"limit": min(limit, 100), "t": time_filter}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        posts = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            posts.append({
                "title": post.get("title", ""),
                "text": post.get("selftext", "")[:500],
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "url": f"https://reddit.com{post.get('permalink', '')}",
                "subreddit": subreddit,
                "created": datetime.fromtimestamp(post.get("created_utc", 0)).isoformat(),
                "is_video_worthy": post.get("score", 0) > 100,
            })

        info(f" => Scraped {len(posts)} posts from r/{subreddit}")
        return posts

    except Exception as e:
        warning(f"Failed to scrape r/{subreddit}: {e}")
        return []


def get_trending_posts(niche: str, limit: int = 10) -> list:
    """
    Gets trending posts from subreddits relevant to a niche.

    Args:
        niche: Content niche
        limit: Posts per subreddit

    Returns:
        List of top posts sorted by score
    """
    niche_lower = niche.lower()

    # Find matching subreddits
    subreddits = []
    for key, subs in NICHE_SUBREDDITS.items():
        if key in niche_lower or niche_lower in key:
            subreddits.extend(subs)

    if not subreddits:
        # Default to general interest
        subreddits = ["todayilearned", "Damnthatsinteresting", "Showerthoughts"]

    all_posts = []
    for sub in subreddits[:4]:  # Limit to 4 subreddits to avoid rate limits
        posts = scrape_subreddit(sub, sort="top", time_filter="week", limit=limit)
        all_posts.extend(posts)
        time.sleep(1)  # Be respectful of Reddit rate limits

    # Sort by score
    all_posts.sort(key=lambda x: x["score"], reverse=True)

    # Cache results
    _cache_results(all_posts)

    success(f" => Found {len(all_posts)} trending posts for niche: {niche}")
    return all_posts


def get_video_ideas_from_reddit(niche: str, count: int = 5) -> list:
    """
    Extracts video ideas from top Reddit posts.

    Args:
        niche: Content niche
        count: Number of ideas to return

    Returns:
        List of dicts with 'topic', 'title', 'source' keys
    """
    posts = get_trending_posts(niche, limit=20)

    # Filter for video-worthy posts
    worthy = [p for p in posts if p.get("is_video_worthy", False)]
    if not worthy:
        worthy = posts[:count]

    ideas = []
    for post in worthy[:count]:
        ideas.append({
            "topic": post["title"],
            "title": post["title"][:100],
            "source": post["url"],
            "score": post["score"],
            "subreddit": post["subreddit"],
        })

    info(f" => Extracted {len(ideas)} video ideas from Reddit")
    return ideas


def search_reddit(query: str, limit: int = 10) -> list:
    """
    Searches all of Reddit for posts matching a query.

    Args:
        query: Search query string
        limit: Max results

    Returns:
        List of post dicts
    """
    url = "https://www.reddit.com/search.json"
    params = {"q": query, "limit": min(limit, 100), "sort": "relevance", "t": "month"}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        posts = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            posts.append({
                "title": post.get("title", ""),
                "text": post.get("selftext", "")[:500],
                "score": post.get("score", 0),
                "subreddit": post.get("subreddit", ""),
                "url": f"https://reddit.com{post.get('permalink', '')}",
            })

        return posts
    except Exception as e:
        warning(f"Reddit search failed: {e}")
        return []


def _cache_results(posts: list):
    """Caches results for offline use."""
    try:
        cache = {"posts": posts, "cached_at": datetime.now().isoformat()}
        os.makedirs(os.path.dirname(REDDIT_CACHE), exist_ok=True)
        with open(REDDIT_CACHE, "w") as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass


def load_cached_results() -> list:
    """Loads cached Reddit results."""
    if not os.path.exists(REDDIT_CACHE):
        return []
    try:
        with open(REDDIT_CACHE, "r") as f:
            return json.load(f).get("posts", [])
    except Exception:
        return []
