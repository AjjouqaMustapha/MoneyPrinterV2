"""
Watermark & Branding Overlay Module
Adds channel logo, name overlay, or custom watermark to every video.
"""

import os
from moviepy.editor import (
    VideoFileClip, ImageClip, TextClip, CompositeVideoClip
)
from uuid import uuid4
from config import ROOT_DIR, _load_config, get_verbose
from status import info, success, warning


WATERMARK_POSITIONS = {
    "top_left": ("left", "top"),
    "top_right": ("right", "top"),
    "bottom_left": ("left", "bottom"),
    "bottom_right": ("right", "bottom"),
    "center": ("center", "center"),
}


def add_logo_watermark(
    video_path: str,
    logo_path: str,
    position: str = "bottom_right",
    opacity: float = 0.6,
    size_ratio: float = 0.12,
    margin: int = 20,
    output_path: str = None,
) -> str:
    """
    Adds a logo image as watermark overlay on a video.

    Args:
        video_path: Path to input video
        logo_path: Path to logo image (PNG with transparency recommended)
        position: One of top_left, top_right, bottom_left, bottom_right, center
        opacity: Logo opacity (0.0 - 1.0)
        size_ratio: Logo size relative to video width (0.0 - 1.0)
        margin: Margin from edges in pixels
        output_path: Output path (auto-generated if None)

    Returns:
        Path to watermarked video
    """
    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", f"wm_{uuid4().hex[:8]}.mp4")

    if not os.path.exists(logo_path):
        warning(f"Logo not found: {logo_path}")
        return video_path

    video = VideoFileClip(video_path)

    # Load and resize logo
    logo = ImageClip(logo_path)
    target_width = int(video.w * size_ratio)
    logo = logo.resize(width=target_width)
    logo = logo.set_opacity(opacity)
    logo = logo.set_duration(video.duration)

    # Calculate position
    pos = WATERMARK_POSITIONS.get(position, ("right", "bottom"))
    if pos[0] == "left":
        x = margin
    elif pos[0] == "right":
        x = video.w - logo.w - margin
    else:
        x = (video.w - logo.w) // 2

    if pos[1] == "top":
        y = margin
    elif pos[1] == "bottom":
        y = video.h - logo.h - margin
    else:
        y = (video.h - logo.h) // 2

    logo = logo.set_position((x, y))

    final = CompositeVideoClip([video, logo])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

    video.close()
    success(f" => Logo watermark added: {output_path}")
    return output_path


def add_text_watermark(
    video_path: str,
    text: str,
    position: str = "bottom_right",
    fontsize: int = 24,
    color: str = "white",
    opacity: float = 0.5,
    font: str = "Arial",
    margin: int = 20,
    output_path: str = None,
) -> str:
    """
    Adds text overlay as branding watermark on a video.

    Args:
        video_path: Path to input video
        text: Watermark text (e.g., "@YourChannel")
        position: Position string
        fontsize: Font size
        color: Text color
        opacity: Text opacity
        font: Font name
        margin: Margin from edges
        output_path: Output path

    Returns:
        Path to watermarked video
    """
    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", f"wm_{uuid4().hex[:8]}.mp4")

    video = VideoFileClip(video_path)

    txt_clip = TextClip(
        text,
        fontsize=fontsize,
        color=color,
        font=font,
        stroke_color="black",
        stroke_width=1,
    )
    txt_clip = txt_clip.set_opacity(opacity)
    txt_clip = txt_clip.set_duration(video.duration)

    pos = WATERMARK_POSITIONS.get(position, ("right", "bottom"))
    if pos[0] == "left":
        x = margin
    elif pos[0] == "right":
        x = video.w - txt_clip.w - margin
    else:
        x = (video.w - txt_clip.w) // 2

    if pos[1] == "top":
        y = margin
    elif pos[1] == "bottom":
        y = video.h - txt_clip.h - margin
    else:
        y = (video.h - txt_clip.h) // 2

    txt_clip = txt_clip.set_position((x, y))

    final = CompositeVideoClip([video, txt_clip])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

    video.close()
    success(f" => Text watermark added: {output_path}")
    return output_path


def add_branding(video_path: str, output_path: str = None) -> str:
    """
    Adds branding based on config.json settings.
    Checks for watermark_logo_path and watermark_text in config.

    Args:
        video_path: Input video path
        output_path: Output path

    Returns:
        Path to branded video (or original if no branding configured)
    """
    config = _load_config()
    logo_path = config.get("watermark_logo_path", "")
    watermark_text = config.get("watermark_text", "")
    position = config.get("watermark_position", "bottom_right")
    opacity = config.get("watermark_opacity", 0.6)

    if logo_path and os.path.exists(logo_path):
        return add_logo_watermark(
            video_path, logo_path, position=position,
            opacity=opacity, output_path=output_path
        )
    elif watermark_text:
        return add_text_watermark(
            video_path, watermark_text, position=position,
            opacity=opacity, output_path=output_path
        )
    else:
        if get_verbose():
            info(" => No watermark configured, skipping branding")
        return video_path
