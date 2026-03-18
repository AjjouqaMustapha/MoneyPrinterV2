import logging

from llm_provider import generate_structured
from prompt_loader import load_prompt

logger = logging.getLogger(__name__)


def optimize_metadata(subject: str, title: str, description: str) -> dict:
    """
    Uses the seo_tags prompt template to generate SEO-optimized metadata.

    Args:
        subject: The video subject / topic.
        title: The current video title.
        description: The current video description.

    Returns:
        A dict with keys:
            - "tags": list of SEO tag strings
            - "optimized_title": SEO-optimized title (under 100 chars)
            - "optimized_description": SEO-optimized description
    """
    prompt = load_prompt(
        "seo_tags",
        subject=subject,
        title=title,
        description=description,
    )

    result = generate_structured(prompt)

    # Ensure expected keys exist with sensible defaults
    return {
        "tags": result.get("tags", []),
        "optimized_title": result.get("optimized_title", title),
        "optimized_description": result.get("optimized_description", description),
    }
