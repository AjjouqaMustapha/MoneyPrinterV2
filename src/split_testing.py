"""
Split Testing Module
Upload the same video with different titles/thumbnails.
Track which variation performs better over time.
"""

import os
import json
import time
from uuid import uuid4
from datetime import datetime
from typing import List
from config import ROOT_DIR, _load_config
from llm_provider import generate_structured
from status import info, success, warning

TESTS_DIR = os.path.join(ROOT_DIR, ".mp", "split_tests")


def ensure_tests_dir():
    if not os.path.exists(TESTS_DIR):
        os.makedirs(TESTS_DIR)


def generate_title_variations(base_title: str, niche: str, count: int = 3) -> List[str]:
    """
    Generates title variations for A/B testing.

    Args:
        base_title: Original video title
        niche: Content niche
        count: Number of variations to generate

    Returns:
        List of title strings (including original)
    """
    prompt = f"""Generate {count} alternative YouTube Short titles for this video.
Each title should use a DIFFERENT psychological strategy.

Original title: {base_title}
Niche: {niche}

Strategies to use:
- Curiosity gap ("You won't believe...")
- Number-based ("3 things that...")
- Contrarian ("Why everyone is wrong about...")
- Emotional ("This broke me...")
- Question ("What happens when...")

Return a JSON object with:
- "variations": array of objects, each with:
  - "title": the alternative title (under 100 chars)
  - "strategy": which psychological strategy it uses

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)
        variations = [base_title]  # Always include original
        for v in result.get("variations", []):
            title = v.get("title", "")
            if title and title != base_title:
                variations.append(title)
        return variations[:count + 1]
    except Exception as e:
        warning(f"Title variation generation failed: {e}")
        return [base_title]


def create_split_test(
    video_path: str,
    base_title: str,
    niche: str,
    platform: str = "youtube",
    variations_count: int = 2,
) -> dict:
    """
    Creates a new split test experiment.

    Args:
        video_path: Path to the video file
        base_title: Original video title
        niche: Content niche
        platform: Target platform
        variations_count: Number of title variations

    Returns:
        Test plan dict
    """
    ensure_tests_dir()

    titles = generate_title_variations(base_title, niche, variations_count)

    test_id = uuid4().hex[:8]
    test = {
        "id": test_id,
        "video_path": video_path,
        "base_title": base_title,
        "niche": niche,
        "platform": platform,
        "created_at": datetime.now().isoformat(),
        "status": "planned",
        "variations": [],
    }

    for i, title in enumerate(titles):
        variation = {
            "variant_id": f"{test_id}_v{i}",
            "title": title,
            "is_original": (i == 0),
            "uploaded": False,
            "upload_url": None,
            "metrics": {
                "views": 0,
                "likes": 0,
                "comments": 0,
                "watch_time_avg": 0,
                "ctr": 0,
            },
            "last_checked": None,
        }
        test["variations"].append(variation)

    _save_test(test)
    success(f" => Split test created: {len(titles)} variations")
    return test


def record_metrics(test_id: str, variant_id: str, metrics: dict):
    """
    Records performance metrics for a test variation.

    Args:
        test_id: Split test ID
        variant_id: Variation ID
        metrics: Dict with views, likes, comments, etc.
    """
    test = _load_test(test_id)
    if not test:
        warning(f"Test not found: {test_id}")
        return

    for var in test["variations"]:
        if var["variant_id"] == variant_id:
            var["metrics"].update(metrics)
            var["last_checked"] = datetime.now().isoformat()
            break

    _save_test(test)
    info(f" => Metrics recorded for {variant_id}")


def get_winner(test_id: str) -> dict:
    """
    Determines the winning variation based on performance.

    Args:
        test_id: Split test ID

    Returns:
        Winning variation dict, or None if insufficient data
    """
    test = _load_test(test_id)
    if not test:
        return None

    best = None
    best_score = -1

    for var in test["variations"]:
        m = var["metrics"]
        # Composite score: views * CTR * engagement rate
        views = m.get("views", 0)
        likes = m.get("likes", 0)
        comments = m.get("comments", 0)

        if views == 0:
            continue

        engagement = (likes + comments * 2) / views
        score = views * engagement

        if score > best_score:
            best_score = score
            best = var

    if best:
        success(f" => Winner: '{best['title']}' (score: {best_score:.2f})")
    return best


def list_tests() -> List[dict]:
    """Lists all split tests."""
    ensure_tests_dir()
    tests = []
    for f in os.listdir(TESTS_DIR):
        if f.endswith(".json"):
            path = os.path.join(TESTS_DIR, f)
            with open(path, "r") as fh:
                tests.append(json.load(fh))
    return tests


def _save_test(test: dict):
    ensure_tests_dir()
    path = os.path.join(TESTS_DIR, f"{test['id']}.json")
    with open(path, "w") as f:
        json.dump(test, f, indent=2)


def _load_test(test_id: str) -> dict:
    path = os.path.join(TESTS_DIR, f"{test_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)
