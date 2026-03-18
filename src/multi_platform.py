import os
from typing import List
from status import info, success, warning, error
from config import _load_config


def upload_to_platforms(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    platforms: List[str] = None,
    firefox_profiles: dict = None,
) -> dict:
    """
    Uploads a video to multiple platforms simultaneously.

    Args:
        video_path: Path to the video file
        title: Video title
        description: Video description
        tags: List of tags
        platforms: List of platform names ("youtube", "tiktok", "instagram")
        firefox_profiles: Dict mapping platform -> firefox profile path

    Returns:
        Dict of platform -> success boolean
    """
    if platforms is None:
        platforms = _load_config().get("upload_platforms", ["youtube"])

    if tags is None:
        tags = []

    if firefox_profiles is None:
        firefox_profiles = {}

    results = {}

    for platform in platforms:
        info(f" => Uploading to {platform}...")

        try:
            if platform == "youtube":
                results["youtube"] = _upload_youtube(video_path, title, description, tags)

            elif platform == "tiktok":
                profile = firefox_profiles.get("tiktok", "")
                if not profile:
                    warning("No Firefox profile configured for TikTok. Skipping.")
                    results["tiktok"] = False
                    continue
                results["tiktok"] = _upload_tiktok(video_path, description, tags, profile)

            elif platform == "instagram":
                profile = firefox_profiles.get("instagram", "")
                if not profile:
                    warning("No Firefox profile configured for Instagram. Skipping.")
                    results["instagram"] = False
                    continue
                results["instagram"] = _upload_instagram(video_path, description, profile)

            else:
                warning(f"Unknown platform: {platform}")
                results[platform] = False

        except Exception as e:
            error(f"Failed to upload to {platform}: {e}")
            results[platform] = False

    # Summary
    succeeded = [p for p, ok in results.items() if ok]
    failed = [p for p, ok in results.items() if not ok]

    if succeeded:
        success(f" => Successfully uploaded to: {', '.join(succeeded)}")
    if failed:
        warning(f" => Failed to upload to: {', '.join(failed)}")

    return results


def _upload_youtube(video_path: str, title: str, description: str, tags: list) -> bool:
    """Upload to YouTube via API (preferred) or Selenium."""
    try:
        from youtube_api import upload_video_api
        video_id = upload_video_api(video_path, title, description, tags)
        return video_id is not None
    except Exception:
        warning("YouTube API upload not available. Use Selenium upload instead.")
        return False


def _upload_tiktok(video_path: str, description: str, tags: list, profile: str) -> bool:
    """Upload to TikTok via Selenium."""
    try:
        from tiktok_uploader import TikTokUploader
        uploader = TikTokUploader(profile)
        return uploader.upload(video_path, description, tags)
    except Exception as e:
        error(f"TikTok upload error: {e}")
        return False


def _upload_instagram(video_path: str, caption: str, profile: str) -> bool:
    """Upload to Instagram via Selenium."""
    try:
        from instagram_uploader import InstagramUploader
        uploader = InstagramUploader(profile)
        return uploader.upload_reel(video_path, caption)
    except Exception as e:
        error(f"Instagram upload error: {e}")
        return False
