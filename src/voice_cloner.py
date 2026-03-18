import os
import asyncio
from uuid import uuid4
from config import ROOT_DIR, _load_config, get_verbose
from status import info, success, warning, error

CLONED_VOICES_DIR = os.path.join(ROOT_DIR, "voices")


def ensure_voices_dir():
    """Creates the voices directory if needed."""
    if not os.path.exists(CLONED_VOICES_DIR):
        os.makedirs(CLONED_VOICES_DIR)


def list_voice_samples() -> list:
    """
    Lists available voice samples for cloning.

    Returns:
        List of file paths to voice samples
    """
    ensure_voices_dir()
    return [
        os.path.join(CLONED_VOICES_DIR, f)
        for f in os.listdir(CLONED_VOICES_DIR)
        if f.lower().endswith((".wav", ".mp3", ".m4a", ".ogg"))
    ]


def clone_voice_with_edge_tts(text: str, voice: str, output_path: str = None) -> str:
    """
    Uses Edge-TTS with a specific voice style as a simple 'cloning' alternative.
    While not true cloning, Edge-TTS offers many distinct voices that can match
    different content styles.

    Args:
        text: Text to synthesize
        voice: Edge-TTS voice name (e.g., 'en-US-GuyNeural')
        output_path: Output audio path

    Returns:
        Path to the generated audio file
    """
    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", f"voice_{uuid4().hex[:8]}.mp3")

    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        asyncio.run(communicate.save(output_path))
        success(f" => Generated voice audio: {output_path}")
        return output_path
    except ImportError:
        error("edge-tts not installed. Run: pip install edge-tts")
        return None
    except Exception as e:
        error(f"Voice generation failed: {e}")
        return None


def get_voice_styles() -> dict:
    """
    Returns recommended Edge-TTS voice styles for different content types.

    Returns:
        Dict mapping content type to voice name
    """
    return {
        # English voices
        "narrator_male": "en-US-GuyNeural",
        "narrator_female": "en-US-JennyNeural",
        "dramatic_male": "en-US-DavisNeural",
        "dramatic_female": "en-US-AriaNeural",
        "young_male": "en-US-JasonNeural",
        "young_female": "en-US-SaraNeural",
        "deep_male": "en-US-ChristopherNeural",
        "british_male": "en-GB-RyanNeural",
        "british_female": "en-GB-SoniaNeural",
        "australian_male": "en-AU-WilliamNeural",
        "australian_female": "en-AU-NatashaNeural",
        # Scary/horror
        "horror": "en-US-GuyNeural",
        # Motivational
        "motivational": "en-US-ChristopherNeural",
        # Fun/casual
        "casual": "en-US-JasonNeural",
        # Professional/business
        "professional": "en-US-DavisNeural",
        # Non-English
        "german_male": "de-DE-ConradNeural",
        "german_female": "de-DE-KatjaNeural",
        "french_male": "fr-FR-HenriNeural",
        "french_female": "fr-FR-DeniseNeural",
        "spanish_male": "es-ES-AlvaroNeural",
        "spanish_female": "es-ES-ElviraNeural",
        "arabic_male": "ar-SA-HamedNeural",
        "arabic_female": "ar-SA-ZariyahNeural",
        "japanese_male": "ja-JP-KeitaNeural",
        "japanese_female": "ja-JP-NanamiNeural",
        "chinese_male": "zh-CN-YunxiNeural",
        "chinese_female": "zh-CN-XiaoxiaoNeural",
        "hindi_male": "hi-IN-MadhurNeural",
        "hindi_female": "hi-IN-SwaraNeural",
        "portuguese_male": "pt-BR-AntonioNeural",
        "portuguese_female": "pt-BR-FranciscaNeural",
    }


def get_voice_for_niche(niche: str) -> str:
    """
    Automatically selects the best voice for a given niche.

    Args:
        niche: Channel niche

    Returns:
        Edge-TTS voice name
    """
    niche_lower = niche.lower()
    styles = get_voice_styles()

    niche_voice_map = {
        "scary": "horror",
        "horror": "horror",
        "dark": "horror",
        "creepy": "horror",
        "motivat": "motivational",
        "self-improvement": "motivational",
        "mindset": "motivational",
        "tech": "professional",
        "business": "professional",
        "finance": "professional",
        "fun": "casual",
        "fact": "casual",
        "comedy": "casual",
        "cooking": "casual",
        "food": "casual",
    }

    for keyword, style_key in niche_voice_map.items():
        if keyword in niche_lower:
            return styles.get(style_key, styles["narrator_male"])

    return styles["narrator_male"]  # Default


def list_all_edge_voices() -> list:
    """
    Lists all available Edge-TTS voices.

    Returns:
        List of voice dicts with name, gender, language
    """
    try:
        import edge_tts
        voices = asyncio.run(edge_tts.list_voices())
        return [
            {
                "name": v["ShortName"],
                "gender": v["Gender"],
                "language": v["Locale"],
            }
            for v in voices
        ]
    except Exception as e:
        warning(f"Failed to list voices: {e}")
        return []
