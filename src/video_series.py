"""
Video Series Module
Generates connected multi-part video series (e.g., "Part 1 of 5...").
Maintains narrative continuity across episodes.
"""

import os
import json
from uuid import uuid4
from typing import List
from config import ROOT_DIR, _load_config
from llm_provider import generate_structured, generate_text
from status import info, success, warning

SERIES_DIR = os.path.join(ROOT_DIR, ".mp", "series")


def ensure_series_dir():
    if not os.path.exists(SERIES_DIR):
        os.makedirs(SERIES_DIR)


def plan_series(topic: str, niche: str, num_parts: int = 5) -> dict:
    """
    Plans a multi-part video series with connected narratives.

    Args:
        topic: Overall series topic
        niche: Channel niche
        num_parts: Number of parts (default 5)

    Returns:
        Series plan dict with id, topic, parts list
    """
    prompt = f"""Plan a {num_parts}-part YouTube Shorts video series about: {topic}
Niche: {niche}

Each part should:
- Be self-contained but connect to the larger narrative
- End with a cliffhanger or hook for the next part
- Have a catchy title with "Part X" in it
- Be 4-6 sentences long when scripted

Return a JSON object with:
- "series_title": overall series title
- "series_hook": one-line hook that appears at the start of each video
- "parts": array of objects, each with:
  - "part_number": integer
  - "title": part title (include "Part X/Y" format)
  - "synopsis": 2-sentence summary of what this part covers
  - "cliffhanger": the hook/cliffhanger at the end of this part
  - "script": full 4-6 sentence script for this part

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)

        series_id = uuid4().hex[:8]
        series = {
            "id": series_id,
            "topic": topic,
            "niche": niche,
            "series_title": result.get("series_title", topic),
            "series_hook": result.get("series_hook", ""),
            "num_parts": num_parts,
            "parts": result.get("parts", []),
            "completed_parts": [],
            "status": "planned",
        }

        # Save series plan
        _save_series(series)

        success(f" => Series planned: '{series['series_title']}' ({num_parts} parts)")
        return series
    except Exception as e:
        warning(f"Series planning failed: {e}")
        return None


def get_next_part(series_id: str) -> dict:
    """
    Gets the next unrecorded part from a series.

    Args:
        series_id: Series ID

    Returns:
        Next part dict, or None if series is complete
    """
    series = _load_series(series_id)
    if not series:
        warning(f"Series not found: {series_id}")
        return None

    completed = set(series.get("completed_parts", []))
    parts = series.get("parts", [])

    for part in parts:
        if part["part_number"] not in completed:
            info(f" => Next part: {part['title']}")
            return part

    info(" => Series complete! All parts generated.")
    return None


def mark_part_complete(series_id: str, part_number: int, video_path: str = None):
    """
    Marks a series part as completed.

    Args:
        series_id: Series ID
        part_number: Part number that was completed
        video_path: Path to the generated video
    """
    series = _load_series(series_id)
    if not series:
        return

    if part_number not in series["completed_parts"]:
        series["completed_parts"].append(part_number)

    if video_path:
        for part in series["parts"]:
            if part["part_number"] == part_number:
                part["video_path"] = video_path
                break

    if len(series["completed_parts"]) >= series["num_parts"]:
        series["status"] = "completed"
        success(f" => Series '{series['series_title']}' fully completed!")
    else:
        remaining = series["num_parts"] - len(series["completed_parts"])
        info(f" => Part {part_number} done. {remaining} parts remaining.")

    _save_series(series)


def list_series() -> List[dict]:
    """Lists all planned/in-progress series."""
    ensure_series_dir()
    series_list = []
    for f in os.listdir(SERIES_DIR):
        if f.endswith(".json"):
            path = os.path.join(SERIES_DIR, f)
            with open(path, "r") as fh:
                series_list.append(json.load(fh))
    return series_list


def _save_series(series: dict):
    ensure_series_dir()
    path = os.path.join(SERIES_DIR, f"{series['id']}.json")
    with open(path, "w") as f:
        json.dump(series, f, indent=2)


def _load_series(series_id: str) -> dict:
    path = os.path.join(SERIES_DIR, f"{series_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)
