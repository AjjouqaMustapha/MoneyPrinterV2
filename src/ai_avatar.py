"""
AI Avatar Module (Stub)
Integration point for adding AI talking avatars to videos.
Supports D-ID, HeyGen, and SadTalker free tiers.

Note: Actual avatar generation requires external API keys or local model setup.
This module provides the interface and will work when configured.
"""

import os
import requests
from uuid import uuid4
from config import ROOT_DIR, _load_config
from status import info, success, warning, error

AVATAR_DIR = os.path.join(ROOT_DIR, ".mp", "avatars")


def ensure_avatar_dir():
    if not os.path.exists(AVATAR_DIR):
        os.makedirs(AVATAR_DIR)


def generate_avatar_video_did(
    audio_path: str,
    image_path: str = None,
    output_path: str = None,
) -> str:
    """
    Generates a talking avatar video using D-ID API.
    Requires a D-ID API key in config.json ("did_api_key").

    Free tier: 5 minutes of video per month.

    Args:
        audio_path: Path to the voiceover audio file
        image_path: Path to the avatar face image (uses default if None)
        output_path: Output video path

    Returns:
        Path to the generated avatar video, or None if failed
    """
    config = _load_config()
    api_key = config.get("did_api_key", "")

    if not api_key:
        warning("D-ID API key not configured. Set 'did_api_key' in config.json")
        warning("Get a free key at: https://www.d-id.com/")
        return None

    if output_path is None:
        ensure_avatar_dir()
        output_path = os.path.join(AVATAR_DIR, f"avatar_{uuid4().hex[:8]}.mp4")

    info(" => Generating D-ID avatar video...")

    try:
        # Step 1: Upload audio
        upload_url = "https://api.d-id.com/audios"
        headers = {
            "Authorization": f"Basic {api_key}",
        }

        with open(audio_path, "rb") as f:
            upload_resp = requests.post(
                upload_url,
                headers=headers,
                files={"audio": f},
                timeout=60,
            )
            upload_resp.raise_for_status()
            audio_url = upload_resp.json().get("url")

        # Step 2: Create talk video
        talk_url = "https://api.d-id.com/talks"
        payload = {
            "script": {
                "type": "audio",
                "audio_url": audio_url,
            },
            "config": {
                "result_format": "mp4",
            },
        }

        if image_path:
            # Upload source image
            with open(image_path, "rb") as f:
                img_resp = requests.post(
                    "https://api.d-id.com/images",
                    headers=headers,
                    files={"image": f},
                    timeout=60,
                )
                img_resp.raise_for_status()
                payload["source_url"] = img_resp.json().get("url")

        talk_resp = requests.post(
            talk_url,
            headers={**headers, "Content-Type": "application/json"},
            json=payload,
            timeout=60,
        )
        talk_resp.raise_for_status()
        talk_id = talk_resp.json().get("id")

        # Step 3: Poll for result
        import time
        result_url = f"{talk_url}/{talk_id}"
        for _ in range(30):
            time.sleep(5)
            result_resp = requests.get(result_url, headers=headers, timeout=30)
            result_data = result_resp.json()

            if result_data.get("status") == "done":
                video_url = result_data.get("result_url")
                if video_url:
                    # Download the video
                    video_resp = requests.get(video_url, timeout=120)
                    with open(output_path, "wb") as f:
                        f.write(video_resp.content)
                    success(f" => Avatar video generated: {output_path}")
                    return output_path

            elif result_data.get("status") == "error":
                error(f"D-ID error: {result_data.get('error', 'Unknown')}")
                return None

        warning("D-ID generation timed out")
        return None

    except Exception as e:
        warning(f"D-ID avatar generation failed: {e}")
        return None


def generate_avatar_local_sadtalker(
    audio_path: str,
    image_path: str,
    output_path: str = None,
) -> str:
    """
    Generates a talking avatar using SadTalker (local, free, open-source).
    Requires SadTalker to be installed separately.

    Args:
        audio_path: Path to the audio file
        image_path: Path to the face image
        output_path: Output video path

    Returns:
        Path to the generated video, or None if SadTalker is not installed
    """
    if output_path is None:
        ensure_avatar_dir()
        output_path = os.path.join(AVATAR_DIR, f"sadtalker_{uuid4().hex[:8]}.mp4")

    config = _load_config()
    sadtalker_path = config.get("sadtalker_path", "")

    if not sadtalker_path or not os.path.exists(sadtalker_path):
        warning("SadTalker not configured. Set 'sadtalker_path' in config.json")
        warning("Install from: https://github.com/OpenTalker/SadTalker")
        return None

    import subprocess

    try:
        cmd = [
            "python",
            os.path.join(sadtalker_path, "inference.py"),
            "--driven_audio", audio_path,
            "--source_image", image_path,
            "--result_dir", os.path.dirname(output_path),
            "--still",
            "--preprocess", "crop",
        ]

        info(" => Running SadTalker inference...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            success(f" => SadTalker avatar generated: {output_path}")
            return output_path
        else:
            warning(f"SadTalker failed: {result.stderr[:200]}")
            return None

    except FileNotFoundError:
        warning("Python or SadTalker not found in PATH")
        return None
    except Exception as e:
        warning(f"SadTalker error: {e}")
        return None


def overlay_avatar_on_video(
    base_video_path: str,
    avatar_video_path: str,
    position: str = "bottom-left",
    size: float = 0.25,
    output_path: str = None,
) -> str:
    """
    Overlays a talking avatar video onto the main video.

    Args:
        base_video_path: Main video path
        avatar_video_path: Avatar video path
        position: Where to place avatar (bottom-left, bottom-right, etc.)
        size: Relative size of avatar (0.25 = 25% of video width)
        output_path: Output path

    Returns:
        Path to the combined video
    """
    from moviepy.editor import VideoFileClip, CompositeVideoClip

    if output_path is None:
        base, ext = os.path.splitext(base_video_path)
        output_path = f"{base}_avatar{ext}"

    try:
        base = VideoFileClip(base_video_path)
        avatar = VideoFileClip(avatar_video_path)

        # Resize avatar
        avatar_width = int(base.w * size)
        avatar = avatar.resize(width=avatar_width)

        # Trim avatar to match base video length
        if avatar.duration > base.duration:
            avatar = avatar.subclip(0, base.duration)

        # Position mapping
        margin = 20
        pos_map = {
            "bottom-left": (margin, base.h - avatar.h - margin),
            "bottom-right": (base.w - avatar.w - margin, base.h - avatar.h - margin),
            "top-left": (margin, margin),
            "top-right": (base.w - avatar.w - margin, margin),
        }
        pos = pos_map.get(position, pos_map["bottom-left"])

        avatar = avatar.set_position(pos)
        final = CompositeVideoClip([base, avatar])

        final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        base.close()
        avatar.close()

        success(f" => Avatar overlaid: {output_path}")
        return output_path

    except Exception as e:
        warning(f"Avatar overlay failed: {e}")
        return base_video_path


def get_avatar_options() -> dict:
    """
    Returns available avatar generation options and their status.

    Returns:
        Dict describing available options
    """
    config = _load_config()

    options = {
        "d-id": {
            "name": "D-ID (Cloud API)",
            "configured": bool(config.get("did_api_key")),
            "free_tier": "5 min/month",
            "quality": "High",
            "url": "https://www.d-id.com/",
        },
        "sadtalker": {
            "name": "SadTalker (Local, Open Source)",
            "configured": bool(config.get("sadtalker_path")) and os.path.exists(config.get("sadtalker_path", "")),
            "free_tier": "Unlimited (local GPU needed)",
            "quality": "Good",
            "url": "https://github.com/OpenTalker/SadTalker",
        },
    }

    return options
