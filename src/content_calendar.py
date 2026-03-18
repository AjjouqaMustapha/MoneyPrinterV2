import json
import os
import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from config import ROOT_DIR, assert_folder_structure
from llm_provider import generate_structured
from prompt_loader import load_prompt

CALENDAR_PATH = os.path.join(ROOT_DIR, ".mp", "calendar.json")


def _load_calendar_data() -> List[dict]:
    """Loads the calendar entries from disk."""
    if not os.path.exists(CALENDAR_PATH):
        return []
    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_calendar_data(entries: List[dict]) -> None:
    """Persists the calendar entries to disk."""
    assert_folder_structure()
    with open(CALENDAR_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def generate_weekly_plan(niche: str, language: str, count: int = 7) -> List[dict]:
    """
    Generates a list of planned topics with dates using the LLM.

    Args:
        niche: The content niche (e.g. "scary stories and urban legends").
        language: The language for the topics.
        count: Number of topics to generate (default 7).

    Returns:
        A list of calendar entry dicts that were added.
    """
    existing = _load_calendar_data()
    used_topics = [e["topic"] for e in existing if e["used"]]

    prompt = (
        f"Generate {count} unique YouTube Short video ideas for the niche: {niche}.\n"
        f"Each idea should be different and cover various aspects of the niche.\n"
        f"Do not repeat topics that have already been used: {used_topics}\n"
        f"Language: {language}\n"
        f'Return a JSON object with: "topics": an array of {count} topic strings'
    )

    result = generate_structured(prompt)
    topics = result.get("topics", [])

    now = datetime.utcnow()
    new_entries: List[dict] = []
    for i, topic in enumerate(topics):
        entry = {
            "id": str(uuid.uuid4()),
            "topic": topic,
            "planned_date": (now + timedelta(days=i)).strftime("%Y-%m-%d"),
            "used": False,
            "created_at": now.isoformat(),
        }
        new_entries.append(entry)

    existing.extend(new_entries)
    _save_calendar_data(existing)
    return new_entries


def get_next_topic(niche: str, language: str) -> str:
    """
    Gets the next unused topic from the calendar.
    Generates a new weekly plan if no unused topics remain.

    Args:
        niche: The content niche.
        language: The language for topics.

    Returns:
        The next topic string.
    """
    entries = _load_calendar_data()
    unused = [e for e in entries if not e["used"]]

    if not unused:
        new_entries = generate_weekly_plan(niche, language)
        unused = new_entries

    # Sort by planned_date to pick the earliest one
    unused.sort(key=lambda e: e["planned_date"])
    return unused[0]["topic"]


def mark_topic_used(topic_id: str) -> None:
    """
    Marks a topic as used by its id.

    Args:
        topic_id: The UUID of the calendar entry.
    """
    entries = _load_calendar_data()
    for entry in entries:
        if entry["id"] == topic_id:
            entry["used"] = True
            break
    _save_calendar_data(entries)


def get_calendar() -> List[dict]:
    """
    Returns the full calendar.

    Returns:
        A list of all calendar entry dicts.
    """
    return _load_calendar_data()


def clear_calendar() -> None:
    """Clears the calendar by removing all entries."""
    _save_calendar_data([])
