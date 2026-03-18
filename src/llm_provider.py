import json
import logging
import time

import requests

from config import get_openrouter_api_key, get_openrouter_model

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

_MAX_RETRIES = 3
_INITIAL_BACKOFF = 2  # seconds


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {get_openrouter_api_key()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/FujiwaraChoki/MoneyPrinterV2",
    }


def _request_with_retry(payload: dict) -> dict:
    """
    Sends a POST request to OpenRouter with exponential backoff.

    On HTTP 429 (rate limit), respects the Retry-After header if present.
    Retries up to _MAX_RETRIES times, starting at _INITIAL_BACKOFF seconds
    and doubling each attempt.

    Returns:
        The parsed JSON response body.

    Raises:
        requests.HTTPError: After all retries are exhausted.
    """
    backoff = _INITIAL_BACKOFF

    for attempt in range(_MAX_RETRIES + 1):
        response = requests.post(
            OPENROUTER_API_URL,
            headers=_headers(),
            json=payload,
            timeout=120,
        )

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429 and attempt < _MAX_RETRIES:
            retry_after = response.headers.get("Retry-After")
            if retry_after is not None:
                wait = float(retry_after)
            else:
                wait = backoff
            logger.warning(
                "Rate limited (429). Retrying in %.1f seconds (attempt %d/%d).",
                wait,
                attempt + 1,
                _MAX_RETRIES,
            )
            time.sleep(wait)
            backoff *= 2
            continue

        if response.status_code >= 500 and attempt < _MAX_RETRIES:
            logger.warning(
                "Server error (%d). Retrying in %.1f seconds (attempt %d/%d).",
                response.status_code,
                backoff,
                attempt + 1,
                _MAX_RETRIES,
            )
            time.sleep(backoff)
            backoff *= 2
            continue

        # Non-retryable error or retries exhausted
        response.raise_for_status()

    # Final attempt failed
    response.raise_for_status()


def generate_text(prompt: str, model_name: str = None) -> str:
    """
    Generates text using the OpenRouter API.

    Args:
        prompt (str): User prompt.
        model_name (str): Optional model name override. Falls back to config.

    Returns:
        response (str): Generated text.
    """
    model = model_name or get_openrouter_model()

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    data = _request_with_retry(payload)
    return data["choices"][0]["message"]["content"].strip()


def generate_structured(prompt: str, model_name: str = None) -> dict:
    """
    Generates a JSON response using the OpenRouter API.

    Sends a system message requesting valid JSON and sets response_format
    to json_object. Parses the response and returns a Python dict.

    Args:
        prompt (str): User prompt describing the desired JSON output.
        model_name (str): Optional model name override. Falls back to config.

    Returns:
        result (dict): Parsed JSON from the model response.
    """
    model = model_name or get_openrouter_model()

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Return valid JSON. Do not include any text outside the JSON object.",
            },
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }

    data = _request_with_retry(payload)
    content = data["choices"][0]["message"]["content"].strip()
    return json.loads(content)
