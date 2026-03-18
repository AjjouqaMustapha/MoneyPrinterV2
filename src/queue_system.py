import os
import json
from uuid import uuid4
from datetime import datetime
from config import ROOT_DIR
from status import info, success, warning, error

QUEUE_PATH = os.path.join(ROOT_DIR, ".mp", "queue.json")


def _load_queue() -> list:
    if not os.path.exists(QUEUE_PATH):
        return []
    with open(QUEUE_PATH, "r") as f:
        return json.load(f)


def _save_queue(queue: list) -> None:
    with open(QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2)


def add_to_queue(platform: str, account_id: str, niche: str = "", language: str = "", topic: str = "") -> str:
    """
    Adds a video/post generation task to the queue.

    Args:
        platform: "youtube" or "twitter"
        account_id: Account UUID
        niche: Channel niche (for youtube)
        language: Content language
        topic: Specific topic (optional)

    Returns:
        task_id: UUID of the queued task
    """
    queue = _load_queue()
    task_id = str(uuid4())

    queue.append({
        "id": task_id,
        "platform": platform,
        "account_id": account_id,
        "niche": niche,
        "language": language,
        "topic": topic,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "started_at": None,
        "completed_at": None,
        "error": None,
        "result": None,
    })

    _save_queue(queue)
    success(f"Added task {task_id[:8]} to queue ({platform})")
    return task_id


def get_next_task() -> dict:
    """
    Gets the next pending task from the queue.

    Returns:
        task dict or None if queue is empty
    """
    queue = _load_queue()
    for task in queue:
        if task["status"] == "pending":
            return task
    return None


def update_task_status(task_id: str, status: str, result: str = None, error_msg: str = None) -> None:
    """
    Updates the status of a queued task.

    Args:
        task_id: Task UUID
        status: "pending", "in_progress", "completed", "failed"
        result: Result data (e.g., video path or URL)
        error_msg: Error message if failed
    """
    queue = _load_queue()

    for task in queue:
        if task["id"] == task_id:
            task["status"] = status
            if status == "in_progress":
                task["started_at"] = datetime.now().isoformat()
            elif status in ("completed", "failed"):
                task["completed_at"] = datetime.now().isoformat()
            if result:
                task["result"] = result
            if error_msg:
                task["error"] = error_msg
            break

    _save_queue(queue)


def get_queue_status() -> dict:
    """
    Returns queue statistics.
    """
    queue = _load_queue()

    stats = {"pending": 0, "in_progress": 0, "completed": 0, "failed": 0, "total": len(queue)}
    for task in queue:
        status = task.get("status", "pending")
        stats[status] = stats.get(status, 0) + 1

    return stats


def clear_completed() -> int:
    """
    Removes completed and failed tasks from the queue.

    Returns:
        Number of tasks removed
    """
    queue = _load_queue()
    original_len = len(queue)
    queue = [t for t in queue if t["status"] in ("pending", "in_progress")]
    _save_queue(queue)
    removed = original_len - len(queue)
    if removed:
        info(f" => Cleared {removed} completed/failed tasks from queue")
    return removed


def process_queue(youtube_factory, twitter_factory, tts_instance) -> None:
    """
    Processes all pending tasks in the queue sequentially.

    Args:
        youtube_factory: Callable that creates a YouTube instance given account data
        twitter_factory: Callable that creates a Twitter instance given account data
        tts_instance: TTS instance for video generation
    """
    from cache import get_accounts

    while True:
        task = get_next_task()
        if not task:
            info("Queue is empty. All tasks processed.")
            break

        task_id = task["id"]
        update_task_status(task_id, "in_progress")
        info(f"Processing task {task_id[:8]} ({task['platform']})...")

        try:
            if task["platform"] == "youtube":
                accounts = get_accounts("youtube")
                account = next((a for a in accounts if a["id"] == task["account_id"]), None)

                if not account:
                    raise ValueError(f"Account {task['account_id']} not found")

                youtube = youtube_factory(account)
                path = youtube.generate_video(tts_instance)
                update_task_status(task_id, "completed", result=path)
                success(f"Task {task_id[:8]} completed: {path}")

            elif task["platform"] == "twitter":
                accounts = get_accounts("twitter")
                account = next((a for a in accounts if a["id"] == task["account_id"]), None)

                if not account:
                    raise ValueError(f"Account {task['account_id']} not found")

                twitter = twitter_factory(account)
                twitter.post()
                update_task_status(task_id, "completed", result="posted")
                success(f"Task {task_id[:8]} completed: tweet posted")

        except Exception as e:
            error(f"Task {task_id[:8]} failed: {e}")
            update_task_status(task_id, "failed", error_msg=str(e))
