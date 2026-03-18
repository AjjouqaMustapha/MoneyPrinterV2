import os
import json
from uuid import uuid4
from datetime import datetime
from config import ROOT_DIR
from llm_provider import generate_structured
from status import info, success, warning


AB_TESTS_PATH = os.path.join(ROOT_DIR, ".mp", "ab_tests.json")


def generate_title_variants(subject: str, count: int = 3) -> list:
    """
    Generates multiple title variants for A/B testing.

    Args:
        subject: Video subject
        count: Number of variants

    Returns:
        List of title strings
    """
    prompt = f"""Generate {count} different YouTube video title options for a video about: {subject}.
Each title should use a different strategy:
1. Curiosity-driven (make viewers curious)
2. Number/list-based (e.g., "3 Things You Didn't Know About...")
3. Emotional/bold claim (e.g., "This Will Change How You Think About...")

Each title must be under 100 characters and include relevant hashtags.

Return a JSON object with:
- "titles": an array of {count} title strings
- "strategies": an array of {count} strategy labels

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)
        titles = result.get("titles", [])
        success(f"Generated {len(titles)} title variants for A/B testing")
        return titles
    except Exception as e:
        warning(f"A/B title generation failed: {e}")
        return []


def save_ab_test(video_id: str, titles: list, selected_index: int) -> None:
    """
    Saves an A/B test record for future analysis.
    """
    tests = _load_tests()

    tests.append({
        "id": str(uuid4()),
        "video_id": video_id,
        "titles": titles,
        "selected_index": selected_index,
        "created_at": datetime.now().isoformat(),
        "performance": None  # To be filled later with analytics
    })

    _save_tests(tests)


def _load_tests() -> list:
    if not os.path.exists(AB_TESTS_PATH):
        return []
    with open(AB_TESTS_PATH, "r") as f:
        return json.load(f)


def _save_tests(tests: list) -> None:
    with open(AB_TESTS_PATH, "w") as f:
        json.dump(tests, f, indent=2)
