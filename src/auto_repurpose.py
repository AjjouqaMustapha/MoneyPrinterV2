import os
import math
from uuid import uuid4
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from config import ROOT_DIR, get_fonts_dir, get_font, get_verbose
from status import info, success, warning, error


def split_video_into_shorts(
    video_path: str,
    max_duration: int = 59,
    overlap: int = 2,
    output_dir: str = None,
) -> list:
    """
    Splits a long video into multiple short clips suitable for YouTube Shorts / TikTok.

    Args:
        video_path: Path to the source video
        max_duration: Maximum duration per short (default 59s for Shorts limit)
        overlap: Seconds of overlap between clips for continuity
        output_dir: Output directory (default .mp/)

    Returns:
        List of output file paths
    """
    if output_dir is None:
        output_dir = os.path.join(ROOT_DIR, ".mp")

    if not os.path.exists(video_path):
        error(f"Video not found: {video_path}")
        return []

    clip = VideoFileClip(video_path)
    total_duration = clip.duration

    if total_duration <= max_duration:
        info("Video is already short enough. No splitting needed.")
        clip.close()
        return [video_path]

    num_parts = math.ceil(total_duration / (max_duration - overlap))
    output_files = []

    info(f" => Splitting {total_duration:.0f}s video into {num_parts} shorts...")

    for i in range(num_parts):
        start = max(0, i * (max_duration - overlap))
        end = min(start + max_duration, total_duration)

        if end - start < 5:  # Skip very short remaining clips
            break

        subclip = clip.subclip(start, end)

        # Add part indicator
        part_text = f"Part {i + 1}/{num_parts}"
        txt_clip = TextClip(
            part_text,
            font=os.path.join(get_fonts_dir(), get_font()),
            fontsize=40,
            color="white",
            stroke_color="black",
            stroke_width=2,
        ).set_duration(3).set_position(("center", 50)).set_start(0)

        final = CompositeVideoClip([subclip, txt_clip])

        output_path = os.path.join(output_dir, f"short_{uuid4().hex[:8]}_part{i+1}.mp4")
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")
        output_files.append(output_path)

        if get_verbose():
            info(f" => Part {i+1}: {start:.0f}s - {end:.0f}s → {output_path}")

    clip.close()
    success(f" => Split into {len(output_files)} shorts")
    return output_files


def resize_to_vertical(video_path: str, output_path: str = None) -> str:
    """
    Resizes a horizontal (16:9) video to vertical (9:16) by cropping the center.

    Args:
        video_path: Path to the source video
        output_path: Output path (default: auto-generated)

    Returns:
        Path to the resized video
    """
    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", f"vertical_{uuid4().hex[:8]}.mp4")

    clip = VideoFileClip(video_path)

    # Calculate crop dimensions for 9:16
    target_ratio = 9 / 16
    current_ratio = clip.w / clip.h

    if current_ratio > target_ratio:
        # Video is wider than needed — crop sides
        new_width = int(clip.h * target_ratio)
        x_center = clip.w / 2
        from moviepy.video.fx.all import crop
        cropped = crop(clip, width=new_width, height=clip.h, x_center=x_center, y_center=clip.h/2)
    else:
        # Video is taller or equal — crop top/bottom
        new_height = int(clip.w / target_ratio)
        from moviepy.video.fx.all import crop
        cropped = crop(clip, width=clip.w, height=new_height, x_center=clip.w/2, y_center=clip.h/2)

    # Resize to 1080x1920
    resized = cropped.resize((1080, 1920))
    resized.write_videofile(output_path, codec="libx264", audio_codec="aac")

    clip.close()
    success(f" => Resized to vertical: {output_path}")
    return output_path


def repurpose_with_captions(video_path: str, transcript: str = None) -> list:
    """
    Full repurpose pipeline: resize → split → add captions.

    Args:
        video_path: Source video path
        transcript: Optional transcript text (for subtitle overlay)

    Returns:
        List of output short video paths
    """
    info(" => Starting repurpose pipeline...")

    # Step 1: Resize to vertical if needed
    clip = VideoFileClip(video_path)
    ratio = clip.w / clip.h
    clip.close()

    if ratio > 1:  # Horizontal video
        info(" => Resizing horizontal video to vertical...")
        video_path = resize_to_vertical(video_path)

    # Step 2: Split into shorts
    shorts = split_video_into_shorts(video_path)

    success(f" => Repurpose complete: {len(shorts)} shorts created")
    return shorts
