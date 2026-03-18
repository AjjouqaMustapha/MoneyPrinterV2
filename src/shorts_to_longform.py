"""
Shorts to Longform Module
Combines multiple related short videos into a 10+ minute compilation.
Adds intro, transitions, and outro for a polished longform video.
"""

import os
from uuid import uuid4
from typing import List
from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, AudioFileClip, ColorClip
)
from config import ROOT_DIR, get_fonts_dir, get_font
from status import info, success, warning


def create_intro_clip(title: str, duration: float = 4.0) -> CompositeVideoClip:
    """
    Creates an intro title card.

    Args:
        title: Compilation title
        duration: Intro duration in seconds

    Returns:
        CompositeVideoClip for the intro
    """
    font_path = os.path.join(get_fonts_dir(), get_font())

    bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(duration)

    title_clip = (
        TextClip(
            title,
            font=font_path,
            fontsize=60,
            color="white",
            stroke_color="gray",
            stroke_width=2,
            method="caption",
            size=(900, None),
            align="center",
        )
        .set_duration(duration)
        .set_position("center")
        .crossfadein(1.0)
    )

    return CompositeVideoClip([bg, title_clip])


def create_transition_clip(text: str = "", duration: float = 1.5) -> CompositeVideoClip:
    """
    Creates a simple transition between shorts.

    Args:
        text: Optional transition text (e.g., "Next...")
        duration: Transition duration

    Returns:
        CompositeVideoClip for the transition
    """
    bg = ColorClip(size=(1080, 1920), color=(15, 15, 15)).set_duration(duration)

    if text:
        font_path = os.path.join(get_fonts_dir(), get_font())
        txt = (
            TextClip(
                text,
                font=font_path,
                fontsize=40,
                color="white",
                method="label",
            )
            .set_duration(duration)
            .set_position("center")
        )
        return CompositeVideoClip([bg, txt])

    return bg


def create_outro_clip(
    channel_name: str,
    subscribe_text: str = "Subscribe for more!",
    duration: float = 5.0,
) -> CompositeVideoClip:
    """
    Creates an outro card with subscribe CTA.

    Args:
        channel_name: Channel name to display
        subscribe_text: CTA text
        duration: Outro duration

    Returns:
        CompositeVideoClip for the outro
    """
    font_path = os.path.join(get_fonts_dir(), get_font())

    bg = ColorClip(size=(1080, 1920), color=(0, 0, 0)).set_duration(duration)

    channel_clip = (
        TextClip(
            channel_name,
            font=font_path,
            fontsize=70,
            color="white",
            stroke_width=2,
            stroke_color="gray",
            method="label",
        )
        .set_duration(duration)
        .set_position(("center", 800))
    )

    cta_clip = (
        TextClip(
            subscribe_text,
            font=font_path,
            fontsize=45,
            color="red",
            method="label",
        )
        .set_duration(duration)
        .set_position(("center", 1000))
        .crossfadein(1.0)
    )

    return CompositeVideoClip([bg, channel_clip, cta_clip])


def compile_shorts_to_longform(
    video_paths: List[str],
    title: str = "Compilation",
    channel_name: str = "",
    add_transitions: bool = True,
    add_intro: bool = True,
    add_outro: bool = True,
    output_path: str = None,
) -> str:
    """
    Combines multiple short videos into one longform compilation.

    Args:
        video_paths: List of short video file paths
        title: Compilation title
        channel_name: Channel name for outro
        add_transitions: Add transitions between clips
        add_intro: Add intro title card
        add_outro: Add outro with subscribe CTA
        output_path: Output file path

    Returns:
        Path to the compiled longform video
    """
    if not video_paths:
        warning("No videos provided for compilation")
        return None

    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", f"compilation_{uuid4().hex[:8]}.mp4")

    clips = []

    # Add intro
    if add_intro:
        intro = create_intro_clip(title)
        clips.append(intro)
        info(" => Added intro card")

    # Add each short with transitions
    for i, path in enumerate(video_paths):
        if not os.path.exists(path):
            warning(f"Video not found: {path}, skipping")
            continue

        try:
            clip = VideoFileClip(path)

            # Resize to 1080x1920 if needed
            if clip.size != [1080, 1920]:
                clip = clip.resize((1080, 1920))

            clips.append(clip)
            info(f" => Added short {i+1}/{len(video_paths)}: {os.path.basename(path)}")

            # Add transition between clips (not after last one)
            if add_transitions and i < len(video_paths) - 1:
                transition = create_transition_clip(f"#{i+2}")
                clips.append(transition)

        except Exception as e:
            warning(f"Failed to load {path}: {e}")
            continue

    # Add outro
    if add_outro and channel_name:
        outro = create_outro_clip(channel_name)
        clips.append(outro)
        info(" => Added outro card")

    if len(clips) < 2:
        warning("Not enough clips to compile")
        return None

    # Concatenate everything
    info(" => Compiling longform video...")
    final = concatenate_videoclips(clips, method="compose")

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        logger=None,
    )

    # Clean up
    for clip in clips:
        try:
            clip.close()
        except Exception:
            pass

    total_duration = final.duration
    success(f" => Compilation complete: {total_duration:.0f}s ({total_duration/60:.1f}min) → {output_path}")
    return output_path
