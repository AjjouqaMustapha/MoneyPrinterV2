"""
Caption Styles Module
Multiple subtitle animation styles: karaoke, bounce, typewriter, fade, highlight.
Creates more engaging subtitles than static text.
"""

import os
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from config import ROOT_DIR, get_fonts_dir, get_font
from status import info, success, warning


def create_karaoke_subtitle(
    text: str,
    video_size: tuple,
    start_time: float,
    duration: float,
    fontsize: int = 50,
    color: str = "white",
    highlight_color: str = "yellow",
    font: str = None,
) -> list:
    """
    Creates a karaoke-style subtitle where words light up one by one.

    Args:
        text: Subtitle text
        video_size: (width, height) of the video
        start_time: When subtitle appears
        duration: How long it stays
        fontsize: Font size
        color: Base text color
        highlight_color: Color for highlighted/active word
        font: Font path

    Returns:
        List of MoviePy clips
    """
    if font is None:
        font = os.path.join(get_fonts_dir(), get_font())

    words = text.split()
    if not words:
        return []

    time_per_word = duration / len(words)
    clips = []

    for i, word in enumerate(words):
        # Create highlighted version of the word
        word_start = start_time + (i * time_per_word)
        word_end = start_time + ((i + 1) * time_per_word)

        # Full text with current word highlighted
        before = " ".join(words[:i])
        current = words[i]
        after = " ".join(words[i+1:])

        # Base text (dimmed)
        base_clip = (
            TextClip(
                text,
                font=font,
                fontsize=fontsize,
                color="gray",
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(video_size[0] - 40, None),
                align="center",
            )
            .set_start(word_start)
            .set_duration(time_per_word)
            .set_position(("center", video_size[1] - 200))
        )
        clips.append(base_clip)

        # Highlighted word overlay
        highlight_clip = (
            TextClip(
                current,
                font=font,
                fontsize=fontsize + 5,
                color=highlight_color,
                stroke_color="black",
                stroke_width=3,
                method="label",
            )
            .set_start(word_start)
            .set_duration(time_per_word)
            .set_position(("center", video_size[1] - 200))
        )
        clips.append(highlight_clip)

    return clips


def create_bounce_subtitle(
    text: str,
    video_size: tuple,
    start_time: float,
    duration: float,
    fontsize: int = 50,
    color: str = "white",
    font: str = None,
) -> list:
    """
    Creates a bounce-in subtitle animation (text pops in with scale effect).

    Args:
        text: Subtitle text
        video_size: Video dimensions
        start_time: Start time
        duration: Duration
        fontsize: Font size
        color: Text color
        font: Font path

    Returns:
        List of MoviePy clips
    """
    if font is None:
        font = os.path.join(get_fonts_dir(), get_font())

    words = text.split()
    if not words:
        return []

    clips = []
    time_per_word = min(0.3, duration / len(words))

    for i, word in enumerate(words):
        word_start = start_time + (i * time_per_word)
        word_duration = duration - (i * time_per_word)

        if word_duration <= 0:
            break

        clip = (
            TextClip(
                " ".join(words[:i+1]),
                font=font,
                fontsize=fontsize,
                color=color,
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(video_size[0] - 40, None),
                align="center",
            )
            .set_start(word_start)
            .set_duration(word_duration)
            .set_position(("center", video_size[1] - 200))
        )
        clips.append(clip)

    return clips


def create_typewriter_subtitle(
    text: str,
    video_size: tuple,
    start_time: float,
    duration: float,
    fontsize: int = 50,
    color: str = "white",
    font: str = None,
    chars_per_step: int = 1,
) -> list:
    """
    Creates a typewriter-effect subtitle (characters appear one by one).

    Args:
        text: Subtitle text
        video_size: Video dimensions
        start_time: Start time
        duration: Duration
        fontsize: Font size
        color: Text color
        font: Font path
        chars_per_step: Characters revealed per step

    Returns:
        List of MoviePy clips
    """
    if font is None:
        font = os.path.join(get_fonts_dir(), get_font())

    if not text:
        return []

    clips = []
    total_steps = len(text) // chars_per_step
    type_duration = min(duration * 0.7, total_steps * 0.05)
    time_per_step = type_duration / max(total_steps, 1)

    for i in range(1, len(text) + 1, chars_per_step):
        partial = text[:i]
        step_start = start_time + ((i // chars_per_step) * time_per_step)

        if i + chars_per_step >= len(text):
            step_duration = (start_time + duration) - step_start
        else:
            step_duration = time_per_step

        if step_duration <= 0:
            break

        clip = (
            TextClip(
                partial,
                font=font,
                fontsize=fontsize,
                color=color,
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(video_size[0] - 40, None),
                align="center",
            )
            .set_start(step_start)
            .set_duration(step_duration)
            .set_position(("center", video_size[1] - 200))
        )
        clips.append(clip)

    return clips


def create_fade_subtitle(
    text: str,
    video_size: tuple,
    start_time: float,
    duration: float,
    fontsize: int = 50,
    color: str = "white",
    font: str = None,
    fade_duration: float = 0.3,
) -> list:
    """
    Creates a fade-in/fade-out subtitle.

    Args:
        text: Subtitle text
        video_size: Video dimensions
        start_time: Start time
        duration: Duration
        fontsize: Font size
        color: Text color
        font: Font path
        fade_duration: Fade in/out duration

    Returns:
        List of MoviePy clips
    """
    if font is None:
        font = os.path.join(get_fonts_dir(), get_font())

    clip = (
        TextClip(
            text,
            font=font,
            fontsize=fontsize,
            color=color,
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(video_size[0] - 40, None),
            align="center",
        )
        .set_start(start_time)
        .set_duration(duration)
        .set_position(("center", video_size[1] - 200))
        .crossfadein(fade_duration)
        .crossfadeout(fade_duration)
    )

    return [clip]


def create_highlight_box_subtitle(
    text: str,
    video_size: tuple,
    start_time: float,
    duration: float,
    fontsize: int = 50,
    color: str = "white",
    bg_color: tuple = (0, 0, 0),
    bg_opacity: float = 0.7,
    font: str = None,
) -> list:
    """
    Creates a subtitle with a colored background box (like news tickers).

    Args:
        text: Subtitle text
        video_size: Video dimensions
        start_time: Start time
        duration: Duration
        fontsize: Font size
        color: Text color
        bg_color: Background box color (RGB tuple)
        bg_opacity: Background opacity
        font: Font path

    Returns:
        List of MoviePy clips
    """
    if font is None:
        font = os.path.join(get_fonts_dir(), get_font())

    # Create text clip to measure size
    txt_clip = TextClip(
        text,
        font=font,
        fontsize=fontsize,
        color=color,
        method="caption",
        size=(video_size[0] - 80, None),
        align="center",
    )

    # Create background box
    padding = 20
    bg_width = min(txt_clip.w + padding * 2, video_size[0])
    bg_height = txt_clip.h + padding * 2

    bg_clip = (
        ColorClip(size=(bg_width, bg_height), color=bg_color)
        .set_opacity(bg_opacity)
        .set_start(start_time)
        .set_duration(duration)
        .set_position(("center", video_size[1] - 200 - padding))
    )

    txt_clip = (
        txt_clip
        .set_start(start_time)
        .set_duration(duration)
        .set_position(("center", video_size[1] - 200))
    )

    return [bg_clip, txt_clip]


# Style registry for easy selection
CAPTION_STYLES = {
    "karaoke": create_karaoke_subtitle,
    "bounce": create_bounce_subtitle,
    "typewriter": create_typewriter_subtitle,
    "fade": create_fade_subtitle,
    "highlight": create_highlight_box_subtitle,
}


def get_available_styles() -> list:
    """Returns list of available caption style names."""
    return list(CAPTION_STYLES.keys())


def create_styled_subtitle(style: str, **kwargs) -> list:
    """
    Creates a subtitle using the specified style.

    Args:
        style: Style name (karaoke, bounce, typewriter, fade, highlight)
        **kwargs: Arguments for the specific style function

    Returns:
        List of MoviePy clips
    """
    func = CAPTION_STYLES.get(style)
    if not func:
        warning(f"Unknown caption style: {style}. Using 'fade'.")
        func = create_fade_subtitle

    return func(**kwargs)
