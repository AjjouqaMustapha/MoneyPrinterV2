import os
import sys
import json
from typing import List, Optional

import srt_equalizer
from termcolor import colored

ROOT_DIR = os.path.dirname(sys.path[0])

# ---------------------------------------------------------------------------
# Config caching
# ---------------------------------------------------------------------------

_cached_config: Optional[dict] = None


def _load_config() -> dict:
    """
    Loads config.json from disk on first call, then returns the cached dict
    on subsequent calls.

    Returns:
        config (dict): The parsed config.json contents
    """
    global _cached_config
    if _cached_config is None:
        with open(os.path.join(ROOT_DIR, "config.json"), "r") as file:
            _cached_config = json.load(file)
    return _cached_config


def reload_config() -> dict:
    """
    Forces a re-read of config.json from disk, updating the cache.

    Returns:
        config (dict): The freshly parsed config.json contents
    """
    global _cached_config
    _cached_config = None
    return _load_config()


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_config() -> List[str]:
    """
    Validates the current configuration and returns a list of warning strings
    for any issues found.

    Returns:
        warnings (List[str]): A list of human-readable warning messages.
                              Empty list means everything looks good.
    """
    warnings: List[str] = []

    # Check config.json exists
    config_path = os.path.join(ROOT_DIR, "config.json")
    if not os.path.exists(config_path):
        warnings.append(f"config.json not found at {config_path}")
        return warnings  # Cannot validate further without the file

    cfg = _load_config()

    # OpenRouter API key
    openrouter_key = cfg.get("openrouter_api_key", "") or os.environ.get("OPENROUTER_API_KEY", "")
    if not openrouter_key:
        warnings.append("openrouter_api_key is not set in config.json or OPENROUTER_API_KEY environment variable")

    # Nano Banana 2 API key
    nb2_key = cfg.get("nanobanana2_api_key", "") or os.environ.get("GEMINI_API_KEY", "")
    if not nb2_key:
        warnings.append("nanobanana2_api_key is not set in config.json or GEMINI_API_KEY environment variable")

    # ImageMagick path
    imagemagick = cfg.get("imagemagick_path", "")
    if not imagemagick:
        warnings.append("imagemagick_path is not set in config.json")
    elif not os.path.isfile(imagemagick):
        warnings.append(f"imagemagick_path does not point to an existing file: {imagemagick}")

    # Firefox profile (only warn if the key is set but the directory is invalid)
    firefox_profile = cfg.get("firefox_profile", "")
    if firefox_profile and not os.path.isdir(firefox_profile):
        warnings.append(f"firefox_profile is not a valid directory: {firefox_profile}")

    return warnings


# ---------------------------------------------------------------------------
# Folder structure helpers
# ---------------------------------------------------------------------------

def assert_folder_structure() -> None:
    """
    Make sure that the nessecary folder structure is present.

    Returns:
        None
    """
    if not os.path.exists(os.path.join(ROOT_DIR, ".mp")):
        if get_verbose():
            print(colored(f"=> Creating .mp folder at {os.path.join(ROOT_DIR, '.mp')}", "green"))
        os.makedirs(os.path.join(ROOT_DIR, ".mp"))


def get_first_time_running() -> bool:
    """
    Checks if the program is running for the first time by checking if .mp folder exists.

    Returns:
        exists (bool): True if the program is running for the first time, False otherwise
    """
    return not os.path.exists(os.path.join(ROOT_DIR, ".mp"))


# ---------------------------------------------------------------------------
# Existing getters (now reading from cached config)
# ---------------------------------------------------------------------------

def get_email_credentials() -> dict:
    """
    Gets the email credentials from the config file.

    Returns:
        credentials (dict): The email credentials
    """
    return _load_config()["email"]


def get_verbose() -> bool:
    """
    Gets the verbose flag from the config file.

    Returns:
        verbose (bool): The verbose flag
    """
    return _load_config()["verbose"]


def get_firefox_profile_path() -> str:
    """
    Gets the path to the Firefox profile.

    Returns:
        path (str): The path to the Firefox profile
    """
    return _load_config()["firefox_profile"]


def get_headless() -> bool:
    """
    Gets the headless flag from the config file.

    Returns:
        headless (bool): The headless flag
    """
    return _load_config()["headless"]


def get_ollama_base_url() -> str:
    """
    Gets the Ollama base URL.

    Returns:
        url (str): The Ollama base URL
    """
    return _load_config().get("ollama_base_url", "http://127.0.0.1:11434")


def get_ollama_model() -> str:
    """
    Gets the Ollama model name from the config file.

    Returns:
        model (str): The Ollama model name, or empty string if not set.
    """
    return _load_config().get("ollama_model", "")


def get_twitter_language() -> str:
    """
    Gets the Twitter language from the config file.

    Returns:
        language (str): The Twitter language
    """
    return _load_config()["twitter_language"]


def get_nanobanana2_api_base_url() -> str:
    """
    Gets the Nano Banana 2 (Gemini image) API base URL.

    Returns:
        url (str): API base URL
    """
    return _load_config().get(
        "nanobanana2_api_base_url",
        "https://generativelanguage.googleapis.com/v1beta",
    )


def get_nanobanana2_api_key() -> str:
    """
    Gets the Nano Banana 2 API key.

    Returns:
        key (str): API key
    """
    configured = _load_config().get("nanobanana2_api_key", "")
    return configured or os.environ.get("GEMINI_API_KEY", "")


def get_nanobanana2_model() -> str:
    """
    Gets the Nano Banana 2 model name.

    Returns:
        model (str): Model name
    """
    return _load_config().get("nanobanana2_model", "gemini-3.1-flash-image-preview")


def get_nanobanana2_aspect_ratio() -> str:
    """
    Gets the aspect ratio for Nano Banana 2 image generation.

    Returns:
        ratio (str): Aspect ratio
    """
    return _load_config().get("nanobanana2_aspect_ratio", "9:16")


def get_threads() -> int:
    """
    Gets the amount of threads to use for example when writing to a file with MoviePy.

    Returns:
        threads (int): Amount of threads
    """
    return _load_config()["threads"]


def get_zip_url() -> str:
    """
    Gets the URL to the zip file containing the songs.

    Returns:
        url (str): The URL to the zip file
    """
    return _load_config()["zip_url"]


def get_is_for_kids() -> bool:
    """
    Gets the is for kids flag from the config file.

    Returns:
        is_for_kids (bool): The is for kids flag
    """
    return _load_config()["is_for_kids"]


def get_google_maps_scraper_zip_url() -> str:
    """
    Gets the URL to the zip file containing the Google Maps scraper.

    Returns:
        url (str): The URL to the zip file
    """
    return _load_config()["google_maps_scraper"]


def get_google_maps_scraper_niche() -> str:
    """
    Gets the niche for the Google Maps scraper.

    Returns:
        niche (str): The niche
    """
    return _load_config()["google_maps_scraper_niche"]


def get_scraper_timeout() -> int:
    """
    Gets the timeout for the scraper.

    Returns:
        timeout (int): The timeout
    """
    return _load_config()["scraper_timeout"] or 300


def get_outreach_message_subject() -> str:
    """
    Gets the outreach message subject.

    Returns:
        subject (str): The outreach message subject
    """
    return _load_config()["outreach_message_subject"]


def get_outreach_message_body_file() -> str:
    """
    Gets the outreach message body file.

    Returns:
        file (str): The outreach message body file
    """
    return _load_config()["outreach_message_body_file"]


def get_tts_voice() -> str:
    """
    Gets the TTS voice from the config file.

    Returns:
        voice (str): The TTS voice
    """
    return _load_config().get("tts_voice", "Jasper")


def get_assemblyai_api_key() -> str:
    """
    Gets the AssemblyAI API key.

    Returns:
        key (str): The AssemblyAI API key
    """
    return _load_config()["assembly_ai_api_key"]


def get_stt_provider() -> str:
    """
    Gets the configured STT provider.

    Returns:
        provider (str): The STT provider
    """
    return _load_config().get("stt_provider", "local_whisper")


def get_whisper_model() -> str:
    """
    Gets the local Whisper model name.

    Returns:
        model (str): Whisper model name
    """
    return _load_config().get("whisper_model", "base")


def get_whisper_device() -> str:
    """
    Gets the target device for Whisper inference.

    Returns:
        device (str): Whisper device
    """
    return _load_config().get("whisper_device", "auto")


def get_whisper_compute_type() -> str:
    """
    Gets the compute type for Whisper inference.

    Returns:
        compute_type (str): Whisper compute type
    """
    return _load_config().get("whisper_compute_type", "int8")


def get_font() -> str:
    """
    Gets the font from the config file.

    Returns:
        font (str): The font
    """
    return _load_config()["font"]


def get_fonts_dir() -> str:
    """
    Gets the fonts directory.

    Returns:
        dir (str): The fonts directory
    """
    return os.path.join(ROOT_DIR, "fonts")


def get_imagemagick_path() -> str:
    """
    Gets the path to ImageMagick.

    Returns:
        path (str): The path to ImageMagick
    """
    return _load_config()["imagemagick_path"]


def get_script_sentence_length() -> int:
    """
    Gets the forced script's sentence length.
    In case there is no sentence length in config, returns 4 when none

    Returns:
        length (int): Length of script's sentence
    """
    config_json = _load_config()
    if config_json.get("script_sentence_length") is not None:
        return config_json["script_sentence_length"]
    else:
        return 4


# ---------------------------------------------------------------------------
# Subtitle helper (unchanged)
# ---------------------------------------------------------------------------

def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
    """
    Equalizes the subtitles in a SRT file.

    Args:
        srt_path (str): The path to the SRT file
        max_chars (int): The maximum amount of characters in a subtitle

    Returns:
        None
    """
    srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)


# ---------------------------------------------------------------------------
# New getters: OpenRouter, Edge-TTS, video transitions
# ---------------------------------------------------------------------------

def get_openrouter_api_key() -> str:
    """
    Gets the OpenRouter API key from config or the OPENROUTER_API_KEY env var.

    Returns:
        key (str): The OpenRouter API key
    """
    configured = _load_config().get("openrouter_api_key", "")
    return configured or os.environ.get("OPENROUTER_API_KEY", "")


def get_openrouter_model() -> str:
    """
    Gets the OpenRouter model name.

    Returns:
        model (str): The OpenRouter model identifier
    """
    return _load_config().get("openrouter_model", "meta-llama/llama-3.2-3b-instruct:free")


def get_tts_engine() -> str:
    """
    Gets the TTS engine to use.

    Options: "edge_tts", "kitten_tts"

    Returns:
        engine (str): The TTS engine name
    """
    return _load_config().get("tts_engine", "edge_tts")


def get_edge_tts_voice() -> str:
    """
    Gets the Edge-TTS voice name.

    Returns:
        voice (str): The Edge-TTS voice identifier
    """
    return _load_config().get("edge_tts_voice", "en-US-ChristopherNeural")


def get_video_transition() -> str:
    """
    Gets the video transition style.

    Options: "none", "fade", "zoom", "slide"

    Returns:
        transition (str): The transition style name
    """
    return _load_config().get("video_transition", "fade")


def get_transition_duration() -> float:
    """
    Gets the duration of video transitions in seconds.

    Returns:
        duration (float): Transition duration in seconds
    """
    return float(_load_config().get("transition_duration", 0.5))


def get_background_music_enabled() -> bool:
    """
    Gets whether background music is enabled.

    Returns:
        enabled (bool): True if background music should be added
    """
    return _load_config().get("background_music_enabled", True)


def get_groq_api_key() -> str:
    configured = _load_config().get("groq_api_key", "")
    return configured or os.environ.get("GROQ_API_KEY", "")

def get_pexels_api_key() -> str:
    configured = _load_config().get("pexels_api_key", "")
    return configured or os.environ.get("PEXELS_API_KEY", "")
