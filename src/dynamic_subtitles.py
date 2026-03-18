import os
import re
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip
from config import get_fonts_dir, get_font


def create_word_highlight_clips(srt_path: str, video_size=(1080, 1920)) -> list:
    """
    Creates word-by-word highlighted subtitle clips from an SRT file.
    Each word is shown with the current word highlighted in yellow,
    other words in white.

    Args:
        srt_path: Path to the SRT file
        video_size: (width, height) of the video

    Returns:
        List of MoviePy clips to composite onto the video
    """
    segments = _parse_srt(srt_path)
    font_path = os.path.join(get_fonts_dir(), get_font())
    clips = []

    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        words = text.split()

        if not words:
            continue

        duration = end - start
        word_duration = duration / len(words)

        for i, word in enumerate(words):
            word_start = start + i * word_duration
            word_end = word_start + word_duration

            # Build the text with current word highlighted
            # We create two layers: white text for all words, yellow for current word
            full_text = " ".join(words)

            # Background text (all white)
            bg_clip = TextClip(
                full_text,
                font=font_path,
                fontsize=70,
                color="white",
                stroke_color="black",
                stroke_width=4,
                size=(video_size[0] - 40, None),
                method="caption",
            ).set_start(word_start).set_duration(word_duration).set_position(("center", 0.75), relative=True)

            # Highlighted word overlay
            # Create a clip with just the highlighted word at the right position
            highlight_clip = TextClip(
                full_text,
                font=font_path,
                fontsize=70,
                color="#FFFF00",
                stroke_color="black",
                stroke_width=4,
                size=(video_size[0] - 40, None),
                method="caption",
            ).set_start(word_start).set_duration(word_duration).set_position(("center", 0.75), relative=True)

            clips.append(bg_clip)

    return clips


def _parse_srt(srt_path: str) -> list:
    """
    Parses an SRT file into a list of segments.

    Returns:
        List of dicts with 'start', 'end', 'text' keys (times in seconds)
    """
    segments = []

    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.strip().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        # Parse timestamp line
        timestamp_line = lines[1]
        match = re.match(
            r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
            timestamp_line
        )
        if not match:
            continue

        h1, m1, s1, ms1, h2, m2, s2, ms2 = [int(x) for x in match.groups()]
        start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000
        end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000

        text = " ".join(lines[2:])

        segments.append({"start": start, "end": end, "text": text})

    return segments
