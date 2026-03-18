import os
import json
from datetime import datetime
from config import ROOT_DIR
from status import info, success, warning

STATE_PATH = os.path.join(ROOT_DIR, ".mp", "pipeline_state.json")


def save_state(stage: str, data: dict) -> None:
    """
    Saves the current pipeline state for resume capability.

    Args:
        stage: Current pipeline stage name
        data: State data to persist
    """
    state = {
        "stage": stage,
        "data": data,
        "saved_at": datetime.now().isoformat(),
    }

    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

    info(f" => Pipeline state saved at stage: {stage}")


def load_state() -> dict:
    """
    Loads the last saved pipeline state.

    Returns:
        State dict with 'stage' and 'data' keys, or None if no state exists
    """
    if not os.path.exists(STATE_PATH):
        return None

    try:
        with open(STATE_PATH, "r") as f:
            state = json.load(f)
        info(f" => Found saved pipeline state at stage: {state.get('stage', 'unknown')}")
        return state
    except Exception:
        return None


def clear_state() -> None:
    """
    Clears the saved pipeline state (call after successful completion).
    """
    if os.path.exists(STATE_PATH):
        os.remove(STATE_PATH)


def get_stage_order() -> list:
    """
    Returns the ordered list of pipeline stages.
    """
    return [
        "content_generation",  # topic, script, metadata, image_prompts
        "image_generation",    # generate AI images
        "tts_generation",      # text-to-speech
        "video_composition",   # combine into video
        "upload",              # upload to platform
    ]


def should_skip_stage(stage: str, saved_state: dict) -> bool:
    """
    Determines if a stage should be skipped based on saved state.

    Args:
        stage: The stage to check
        saved_state: The loaded pipeline state

    Returns:
        True if this stage was already completed and should be skipped
    """
    if not saved_state:
        return False

    stages = get_stage_order()
    saved_stage = saved_state.get("stage", "")

    if saved_stage not in stages or stage not in stages:
        return False

    return stages.index(stage) < stages.index(saved_stage)
