import os
import sys
import platform
import subprocess
from status import info, warning


def preview_video(video_path: str) -> bool:
    """
    Opens the generated video in the system's default media player for preview.

    Args:
        video_path: Path to the video file

    Returns:
        True if the video was opened successfully
    """
    if not os.path.exists(video_path):
        warning(f"Video file not found: {video_path}")
        return False

    info(f" => Opening video preview: {video_path}")

    try:
        system = platform.system()

        if system == "Windows":
            os.startfile(video_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", video_path], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", video_path], check=True)

        return True
    except Exception as e:
        warning(f"Failed to open video preview: {e}")
        warning(f"Video is saved at: {video_path}")
        return False


def get_video_info(video_path: str) -> dict:
    """
    Gets basic info about a video file.

    Args:
        video_path: Path to the video file

    Returns:
        Dict with file size, duration estimate, etc.
    """
    if not os.path.exists(video_path):
        return {}

    size_bytes = os.path.getsize(video_path)
    size_mb = round(size_bytes / (1024 * 1024), 2)

    info_dict = {
        "path": video_path,
        "size_bytes": size_bytes,
        "size_mb": size_mb,
        "filename": os.path.basename(video_path),
    }

    # Try to get duration using moviepy
    try:
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(video_path)
        info_dict["duration_seconds"] = round(clip.duration, 2)
        info_dict["resolution"] = f"{clip.w}x{clip.h}"
        info_dict["fps"] = clip.fps
        clip.close()
    except Exception:
        pass

    return info_dict
