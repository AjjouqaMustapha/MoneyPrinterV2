import re
import time
import json
import os
from datetime import datetime
from typing import List
from config import ROOT_DIR, get_headless, get_verbose
from llm_provider import generate_text, generate_structured
from status import info, success, warning, error

ANALYSIS_CACHE = os.path.join(ROOT_DIR, ".mp", "competitor_analysis.json")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options
    from webdriver_manager.firefox import GeckoDriverManager
except ImportError:
    pass


def scrape_channel_videos(channel_url: str, firefox_profile: str, max_videos: int = 20) -> List[dict]:
    """
    Scrapes video titles, views, and dates from a YouTube channel.

    Args:
        channel_url: YouTube channel URL (e.g., https://youtube.com/@channelname)
        firefox_profile: Path to Firefox profile
        max_videos: Max videos to scrape

    Returns:
        List of video dicts with title, views, date, url
    """
    options = Options()
    if get_headless():
        options.add_argument("--headless")
    options.add_argument("-profile")
    options.add_argument(firefox_profile)

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)

    videos = []

    try:
        # Navigate to channel's shorts tab
        shorts_url = channel_url.rstrip("/") + "/shorts"
        driver.get(shorts_url)
        time.sleep(5)

        # Scroll to load more videos
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(2)

        # Extract video data
        video_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-rich-item-renderer")

        for elem in video_elements[:max_videos]:
            try:
                title_el = elem.find_element(By.CSS_SELECTOR, "#video-title")
                title = title_el.text.strip()
                url = title_el.get_attribute("href") or ""

                # Try to get view count
                metadata = elem.find_elements(By.CSS_SELECTOR, "#metadata-line span")
                views = metadata[0].text if metadata else "N/A"

                if title:
                    videos.append({
                        "title": title,
                        "views": views,
                        "url": url,
                    })
            except Exception:
                continue

        info(f" => Scraped {len(videos)} videos from {channel_url}")

    except Exception as e:
        warning(f"Failed to scrape channel: {e}")
    finally:
        driver.quit()

    return videos


def analyze_competitor(channel_url: str, firefox_profile: str, niche: str) -> dict:
    """
    Performs a full competitor analysis on a YouTube channel.

    Args:
        channel_url: YouTube channel URL
        firefox_profile: Firefox profile path
        niche: Your channel's niche for comparison

    Returns:
        Analysis dict with top videos, patterns, and suggestions
    """
    videos = scrape_channel_videos(channel_url, firefox_profile)

    if not videos:
        return {"error": "No videos found"}

    # Extract titles for LLM analysis
    titles = [v["title"] for v in videos[:15]]
    titles_str = "\n".join(f"- {t}" for t in titles)

    prompt = f"""Analyze these YouTube Short titles from a competitor channel in the "{niche}" niche:

{titles_str}

Return a JSON object with:
- "patterns": array of 3-5 content patterns/themes they use repeatedly
- "title_strategies": array of 3 title writing strategies they use
- "content_gaps": array of 3 topics they HAVEN'T covered that you could
- "viral_elements": array of 3 elements that make their top videos work
- "suggestions": array of 5 specific video ideas to compete with them

YOU MUST ONLY RETURN VALID JSON."""

    try:
        analysis = generate_structured(prompt)
        analysis["channel_url"] = channel_url
        analysis["videos_analyzed"] = len(videos)
        analysis["top_videos"] = videos[:5]
        analysis["analyzed_at"] = datetime.now().isoformat()

        # Save to cache
        _save_analysis(analysis)

        success(f" => Competitor analysis complete: {len(videos)} videos analyzed")
        return analysis
    except Exception as e:
        warning(f"LLM analysis failed: {e}")
        return {"videos": videos, "error": str(e)}


def get_competitor_suggestions(niche: str, competitor_count: int = 1) -> List[str]:
    """
    Returns video suggestions based on past competitor analyses.
    """
    analyses = _load_analyses()
    if not analyses:
        return []

    all_suggestions = []
    for a in analyses[-competitor_count:]:
        suggestions = a.get("suggestions", [])
        all_suggestions.extend(suggestions)

    return all_suggestions


def _load_analyses() -> list:
    if not os.path.exists(ANALYSIS_CACHE):
        return []
    with open(ANALYSIS_CACHE, "r") as f:
        return json.load(f)


def _save_analysis(analysis: dict):
    analyses = _load_analyses()
    analyses.append(analysis)
    with open(ANALYSIS_CACHE, "w") as f:
        json.dump(analyses, f, indent=2)
