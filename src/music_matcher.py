import os
import random
from config import ROOT_DIR, _load_config, get_verbose
from llm_provider import generate_structured
from status import info, success, warning

MUSIC_DIR = os.path.join(ROOT_DIR, "Songs")

# Music mood categories
MOOD_KEYWORDS = {
    "chill": ["lofi", "chill", "relax", "calm", "ambient", "peaceful"],
    "hype": ["energetic", "upbeat", "exciting", "fast", "pump", "intense"],
    "sad": ["sad", "emotional", "melancholy", "piano", "slow"],
    "dark": ["dark", "suspense", "horror", "creepy", "tense", "eerie"],
    "happy": ["happy", "cheerful", "fun", "positive", "bright"],
    "epic": ["epic", "cinematic", "dramatic", "powerful", "orchestral"],
    "romantic": ["romantic", "love", "soft", "gentle"],
}


def detect_content_mood(script: str, niche: str) -> str:
    """
    Uses LLM to detect the mood of content for music matching.

    Args:
        script: Video script text
        niche: Channel niche

    Returns:
        Mood string (one of: chill, hype, sad, dark, happy, epic, romantic)
    """
    prompt = f"""Analyze the mood of this video script and niche.

Script: {script[:500]}
Niche: {niche}

What is the primary mood? Choose exactly ONE from:
chill, hype, sad, dark, happy, epic, romantic

Return a JSON object with:
- "mood": the mood string
- "reason": one sentence explaining why

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)
        mood = result.get("mood", "chill").lower()

        # Validate mood
        if mood not in MOOD_KEYWORDS:
            mood = "chill"

        if get_verbose():
            info(f" => Detected content mood: {mood} ({result.get('reason', '')})")

        return mood
    except Exception as e:
        warning(f"Mood detection failed: {e}")
        return "chill"


def match_song_to_mood(mood: str) -> str:
    """
    Selects a song from the Songs directory that matches the mood.
    Falls back to random selection if no mood-matched songs are found.

    Args:
        mood: Mood string

    Returns:
        Path to the selected song, or None if no songs available
    """
    if not os.path.exists(MUSIC_DIR):
        warning("Songs directory not found")
        return None

    songs = [
        f for f in os.listdir(MUSIC_DIR)
        if os.path.isfile(os.path.join(MUSIC_DIR, f))
        and f.lower().endswith((".mp3", ".wav", ".m4a", ".aac", ".ogg"))
    ]

    if not songs:
        warning("No songs found in Songs directory")
        return None

    # Try to match by filename keywords
    mood_keywords = MOOD_KEYWORDS.get(mood, [])
    matched = []

    for song in songs:
        song_lower = song.lower()
        for keyword in mood_keywords:
            if keyword in song_lower:
                matched.append(song)
                break

    if matched:
        selected = random.choice(matched)
        info(f" => Mood-matched song: {selected} (mood: {mood})")
    else:
        selected = random.choice(songs)
        info(f" => Random song (no mood match): {selected}")

    return os.path.join(MUSIC_DIR, selected)


def get_music_for_content(script: str, niche: str) -> str:
    """
    Full pipeline: detect mood → match song.

    Args:
        script: Video script
        niche: Channel niche

    Returns:
        Path to the selected song, or None
    """
    mood = detect_content_mood(script, niche)
    return match_song_to_mood(mood)
