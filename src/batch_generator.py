import os
import json
from uuid import uuid4
from datetime import datetime
from config import ROOT_DIR, get_verbose
from status import info, success, warning, error

BATCH_LOG_PATH = os.path.join(ROOT_DIR, ".mp", "batch_log.json")


def generate_batch(
    youtube_factory,
    tts_instance,
    account: dict,
    count: int = 10,
    upload: bool = False,
    platform: str = "youtube",
) -> list:
    """
    Generates multiple videos in batch mode.

    Args:
        youtube_factory: Callable that creates a YouTube instance from account data
        tts_instance: TTS instance
        account: Account dict with id, nickname, firefox_profile, niche, language
        count: Number of videos to generate
        upload: Whether to upload each video after generation
        platform: Upload platform ("youtube", "tiktok", "instagram")

    Returns:
        List of dicts with video info (path, title, status)
    """
    results = []

    info(f" => Starting batch generation: {count} videos for '{account['nickname']}'")

    for i in range(count):
        info(f"\n{'='*50}")
        info(f" => Generating video {i+1}/{count}...")
        info(f"{'='*50}\n")

        try:
            youtube = youtube_factory(account)
            path = youtube.generate_video(tts_instance)

            result = {
                "id": str(uuid4()),
                "index": i + 1,
                "path": path,
                "title": youtube.metadata.get("title", "Untitled"),
                "description": youtube.metadata.get("description", ""),
                "status": "generated",
                "platform": platform,
                "timestamp": datetime.now().isoformat(),
                "uploaded": False,
                "error": None,
            }

            if upload:
                try:
                    if platform == "youtube":
                        uploaded = youtube.upload_video()
                        result["uploaded"] = uploaded
                        result["status"] = "uploaded" if uploaded else "upload_failed"
                    elif platform == "tiktok":
                        from tiktok_uploader import TikTokUploader
                        uploader = TikTokUploader(account["firefox_profile"])
                        uploaded = uploader.upload(path, result["description"][:150])
                        result["uploaded"] = uploaded
                        result["status"] = "uploaded" if uploaded else "upload_failed"
                except Exception as e:
                    result["status"] = "upload_failed"
                    result["error"] = str(e)
                    warning(f" => Upload failed for video {i+1}: {e}")

            results.append(result)
            success(f" => Video {i+1}/{count} complete: {result['status']}")

            # Send notification if webhooks configured
            try:
                from webhooks import notify
                notify(f"Video {i+1}/{count} generated: {result['title'][:50]}")
            except Exception:
                pass

        except Exception as e:
            error(f" => Video {i+1}/{count} failed: {e}")
            results.append({
                "id": str(uuid4()),
                "index": i + 1,
                "path": None,
                "title": None,
                "status": "failed",
                "platform": platform,
                "timestamp": datetime.now().isoformat(),
                "uploaded": False,
                "error": str(e),
            })

    # Save batch log
    _save_batch_log(results)

    # Summary
    generated = sum(1 for r in results if r["status"] in ("generated", "uploaded"))
    uploaded = sum(1 for r in results if r["uploaded"])
    failed = sum(1 for r in results if r["status"] == "failed")

    info(f"\n{'='*50}")
    success(f" => Batch complete: {generated} generated, {uploaded} uploaded, {failed} failed")
    info(f"{'='*50}")

    return results


def get_batch_log() -> list:
    """Returns the batch generation history."""
    if not os.path.exists(BATCH_LOG_PATH):
        return []
    with open(BATCH_LOG_PATH, "r") as f:
        return json.load(f)


def _save_batch_log(results: list):
    existing = get_batch_log()
    existing.extend(results)
    with open(BATCH_LOG_PATH, "w") as f:
        json.dump(existing, f, indent=2)


def get_batch_summary() -> dict:
    """Returns summary stats of all batch generations."""
    log = get_batch_log()
    if not log:
        return {"total": 0}

    return {
        "total": len(log),
        "generated": sum(1 for r in log if r["status"] in ("generated", "uploaded")),
        "uploaded": sum(1 for r in log if r.get("uploaded")),
        "failed": sum(1 for r in log if r["status"] == "failed"),
        "platforms": {},
    }
