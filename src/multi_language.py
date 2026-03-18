"""
Multi-Language Dubbing Module
Generates the same video in multiple languages using LLM translation + Edge-TTS.
One video → 5+ languages = 5x the audience.
"""

import os
import asyncio
from uuid import uuid4
from config import ROOT_DIR, get_verbose
from llm_provider import generate_text
from status import info, success, warning, error

try:
    import edge_tts
except ImportError:
    edge_tts = None

# Supported languages with Edge-TTS voice mapping
LANGUAGE_VOICES = {
    "english": {"code": "en", "voice_m": "en-US-GuyNeural", "voice_f": "en-US-JennyNeural"},
    "spanish": {"code": "es", "voice_m": "es-ES-AlvaroNeural", "voice_f": "es-ES-ElviraNeural"},
    "french": {"code": "fr", "voice_m": "fr-FR-HenriNeural", "voice_f": "fr-FR-DeniseNeural"},
    "german": {"code": "de", "voice_m": "de-DE-ConradNeural", "voice_f": "de-DE-KatjaNeural"},
    "portuguese": {"code": "pt", "voice_m": "pt-BR-AntonioNeural", "voice_f": "pt-BR-FranciscaNeural"},
    "italian": {"code": "it", "voice_m": "it-IT-DiegoNeural", "voice_f": "it-IT-ElsaNeural"},
    "arabic": {"code": "ar", "voice_m": "ar-SA-HamedNeural", "voice_f": "ar-SA-ZariyahNeural"},
    "hindi": {"code": "hi", "voice_m": "hi-IN-MadhurNeural", "voice_f": "hi-IN-SwaraNeural"},
    "japanese": {"code": "ja", "voice_m": "ja-JP-KeitaNeural", "voice_f": "ja-JP-NanamiNeural"},
    "chinese": {"code": "zh", "voice_m": "zh-CN-YunxiNeural", "voice_f": "zh-CN-XiaoxiaoNeural"},
    "korean": {"code": "ko", "voice_m": "ko-KR-InJoonNeural", "voice_f": "ko-KR-SunHiNeural"},
    "russian": {"code": "ru", "voice_m": "ru-RU-DmitryNeural", "voice_f": "ru-RU-SvetlanaNeural"},
    "turkish": {"code": "tr", "voice_m": "tr-TR-AhmetNeural", "voice_f": "tr-TR-EmelNeural"},
    "dutch": {"code": "nl", "voice_m": "nl-NL-MaartenNeural", "voice_f": "nl-NL-ColetteNeural"},
    "polish": {"code": "pl", "voice_m": "pl-PL-MarekNeural", "voice_f": "pl-PL-ZofiaNeural"},
    "indonesian": {"code": "id", "voice_m": "id-ID-ArdiNeural", "voice_f": "id-ID-GadisNeural"},
    "thai": {"code": "th", "voice_m": "th-TH-NiwatNeural", "voice_f": "th-TH-PremwadeeNeural"},
    "vietnamese": {"code": "vi", "voice_m": "vi-VN-NamMinhNeural", "voice_f": "vi-VN-HoaiMyNeural"},
}


def translate_script(script: str, target_language: str) -> str:
    """
    Translates a video script to another language using LLM.

    Args:
        script: Original script text
        target_language: Target language name (e.g., "spanish")

    Returns:
        Translated script text
    """
    prompt = f"""Translate this YouTube Short script to {target_language}.
Keep the same tone, energy, and emotional impact.
Keep it natural - not a literal translation.
Adapt cultural references if needed.
Keep it the same length (don't make it longer).

Original script:
{script}

Return ONLY the translated text, nothing else."""

    try:
        translated = generate_text(prompt)
        if get_verbose():
            info(f" => Translated to {target_language}: {len(translated)} chars")
        return translated.strip()
    except Exception as e:
        warning(f"Translation to {target_language} failed: {e}")
        return ""


def translate_metadata(title: str, description: str, target_language: str) -> dict:
    """
    Translates video title and description.

    Args:
        title: Original title
        description: Original description
        target_language: Target language

    Returns:
        Dict with 'title' and 'description' keys
    """
    prompt = f"""Translate this YouTube video title and description to {target_language}.
Make the title catchy and optimized for {target_language}-speaking audience.
Keep the description SEO-friendly.

Title: {title}
Description: {description}

Return ONLY a JSON object with "title" and "description" keys.
YOU MUST ONLY RETURN VALID JSON."""

    try:
        import json
        result = generate_text(prompt)
        # Try to parse JSON
        result = result.strip()
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        return json.loads(result)
    except Exception as e:
        warning(f"Metadata translation failed: {e}")
        return {"title": title, "description": description}


def generate_dubbed_audio(text: str, language: str, gender: str = "male", output_path: str = None) -> str:
    """
    Generates TTS audio in the target language.

    Args:
        text: Script text in the target language
        language: Language name
        gender: "male" or "female"
        output_path: Output path

    Returns:
        Path to the audio file
    """
    if edge_tts is None:
        error("edge-tts not installed. Run: pip install edge-tts")
        return None

    if output_path is None:
        output_path = os.path.join(ROOT_DIR, ".mp", f"dub_{language}_{uuid4().hex[:6]}.mp3")

    lang_config = LANGUAGE_VOICES.get(language.lower())
    if not lang_config:
        warning(f"Language '{language}' not supported for TTS")
        return None

    voice = lang_config[f"voice_{gender[0]}"]

    try:
        communicate = edge_tts.Communicate(text, voice)
        asyncio.run(communicate.save(output_path))
        success(f" => Generated {language} audio: {output_path}")
        return output_path
    except Exception as e:
        error(f"TTS generation failed for {language}: {e}")
        return None


def create_multi_language_versions(
    script: str,
    title: str,
    description: str,
    languages: list = None,
    gender: str = "male",
) -> list:
    """
    Creates translated scripts and audio for multiple languages.

    Args:
        script: Original script
        title: Original title
        description: Original description
        languages: List of language names (default: top 5)
        gender: Voice gender preference

    Returns:
        List of dicts with language, script, title, description, audio_path
    """
    if languages is None:
        languages = ["spanish", "french", "german", "portuguese", "hindi"]

    results = []

    for lang in languages:
        info(f" => Processing {lang}...")

        # Translate script
        translated_script = translate_script(script, lang)
        if not translated_script:
            continue

        # Translate metadata
        metadata = translate_metadata(title, description, lang)

        # Generate audio
        audio_path = generate_dubbed_audio(translated_script, lang, gender)

        results.append({
            "language": lang,
            "language_code": LANGUAGE_VOICES.get(lang.lower(), {}).get("code", ""),
            "script": translated_script,
            "title": metadata.get("title", title),
            "description": metadata.get("description", description),
            "audio_path": audio_path,
        })

        success(f" => {lang.capitalize()} version ready")

    success(f" => Multi-language dub complete: {len(results)} languages")
    return results


def get_supported_languages() -> list:
    """Returns list of all supported language names."""
    return list(LANGUAGE_VOICES.keys())


def get_top_languages_for_niche(niche: str) -> list:
    """
    Suggests the best languages to target for a given niche.

    Args:
        niche: Content niche

    Returns:
        List of recommended language names
    """
    niche_lower = niche.lower()

    # General high-reach languages
    default = ["spanish", "portuguese", "hindi", "arabic", "french"]

    niche_lang_map = {
        "tech": ["hindi", "japanese", "korean", "chinese", "german"],
        "gaming": ["japanese", "korean", "spanish", "portuguese", "russian"],
        "cooking": ["spanish", "italian", "french", "portuguese", "turkish"],
        "finance": ["hindi", "spanish", "portuguese", "german", "chinese"],
        "motivat": ["hindi", "spanish", "arabic", "portuguese", "turkish"],
        "scary": ["spanish", "portuguese", "russian", "turkish", "arabic"],
        "science": ["hindi", "chinese", "japanese", "german", "spanish"],
        "fitness": ["spanish", "portuguese", "hindi", "german", "korean"],
    }

    for keyword, langs in niche_lang_map.items():
        if keyword in niche_lower:
            return langs

    return default
