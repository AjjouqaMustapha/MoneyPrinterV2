import os
import requests
from uuid import uuid4
from config import ROOT_DIR, _load_config, get_verbose
from status import info, success, warning

BACKGROUNDS_DIR = os.path.join(ROOT_DIR, "backgrounds")

# Free stock video sources for common moods/themes
BACKGROUND_THEMES = {
    "rain": "rain drops window",
    "fire": "fireplace cozy flames",
    "space": "space stars galaxy timelapse",
    "ocean": "ocean waves aerial",
    "city": "city night lights timelapse",
    "nature": "forest trees aerial",
    "abstract": "abstract colorful gradient",
    "smoke": "smoke dark background",
    "clouds": "clouds sky timelapse",
    "neon": "neon lights cyberpunk city",
}


def ensure_backgrounds_dir():
    """Creates the backgrounds directory if it doesn't exist."""
    if not os.path.exists(BACKGROUNDS_DIR):
        os.makedirs(BACKGROUNDS_DIR)


def get_available_backgrounds() -> list:
    """
    Lists all downloaded background videos.

    Returns:
        List of file paths
    """
    ensure_backgrounds_dir()
    files = [
        os.path.join(BACKGROUNDS_DIR, f)
        for f in os.listdir(BACKGROUNDS_DIR)
        if f.lower().endswith((".mp4", ".webm", ".mov"))
    ]
    return files


def download_background_from_pexels(theme: str, count: int = 1) -> list:
    """
    Downloads background loop videos from Pexels API.

    Args:
        theme: Theme keyword (see BACKGROUND_THEMES) or custom search query
        count: Number of videos to download

    Returns:
        List of downloaded file paths
    """
    from stock_footage import search_stock_videos, download_stock_video

    query = BACKGROUND_THEMES.get(theme, theme)
    info(f" => Searching Pexels for background: '{query}'...")

    videos = search_stock_videos(query, count=count, orientation="portrait")

    downloaded = []
    ensure_backgrounds_dir()

    for video in videos:
        url = video.get("download_url")
        if not url:
            continue

        output_path = os.path.join(BACKGROUNDS_DIR, f"bg_{theme}_{uuid4().hex[:6]}.mp4")

        try:
            response = requests.get(url, timeout=120, stream=True)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            downloaded.append(output_path)
            success(f" => Downloaded background: {output_path}")
        except Exception as e:
            warning(f"Failed to download background: {e}")

    return downloaded


def get_background_for_niche(niche: str) -> str:
    """
    Selects the best background theme for a given niche.

    Args:
        niche: Channel niche

    Returns:
        Theme string
    """
    niche_lower = niche.lower()

    # Map niches to themes
    niche_theme_map = {
        "scary": "smoke",
        "horror": "smoke",
        "dark": "smoke",
        "creepy": "neon",
        "motivat": "nature",
        "self-improvement": "ocean",
        "mindset": "clouds",
        "tech": "neon",
        "science": "space",
        "space": "space",
        "cooking": "fire",
        "food": "fire",
        "recipe": "fire",
        "travel": "nature",
        "nature": "nature",
        "relax": "rain",
        "sleep": "rain",
        "asmr": "rain",
        "city": "city",
        "urban": "city",
        "finance": "city",
        "money": "abstract",
        "business": "city",
        "fact": "abstract",
        "history": "clouds",
    }

    for keyword, theme in niche_theme_map.items():
        if keyword in niche_lower:
            return theme

    return "abstract"  # Default fallback


def create_looped_background(video_path: str, target_duration: float, output_path: str = None) -> str:
    """
    Loops a background video to match a target duration.

    Args:
        video_path: Path to the background video
        target_duration: Desired duration in seconds
        output_path: Output path (auto-generated if None)

    Returns:
        Path to the looped video
    """
    from moviepy.editor import VideoFileClip, concatenate_videoclips

    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", f"bg_loop_{uuid4().hex[:8]}.mp4")

    clip = VideoFileClip(video_path)
    clip_duration = clip.duration

    if clip_duration >= target_duration:
        # Just trim
        final = clip.subclip(0, target_duration)
    else:
        # Loop the clip
        import math
        repeats = math.ceil(target_duration / clip_duration)
        clips = [clip] * repeats
        final = concatenate_videoclips(clips).subclip(0, target_duration)

    final = final.resize((1080, 1920))
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)

    clip.close()
    if get_verbose():
        info(f" => Created looped background: {output_path} ({target_duration:.1f}s)")
    return output_path
