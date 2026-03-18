from llm_provider import generate_structured
from status import info, success, warning


def generate_hooks(subject: str, count: int = 3) -> dict:
    """
    Generates multiple attention-grabbing opening hooks and picks the best one.

    Args:
        subject: The video subject/topic
        count: Number of hooks to generate

    Returns:
        dict with 'hooks' (list), 'best_index' (int), 'best_hook' (str)
    """
    prompt = f"""Generate {count} different attention-grabbing opening hooks for a YouTube Short about: {subject}.
Each hook should be one sentence, designed to stop viewers from scrolling.
Use techniques like: surprising facts, questions, bold claims, or emotional triggers.

Return a JSON object with:
- "hooks": an array of {count} hook strings
- "best_index": the index (0-{count-1}) of the most engaging hook

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)
        hooks = result.get("hooks", [])
        best_idx = result.get("best_index", 0)

        if not hooks:
            return {"hooks": [], "best_index": 0, "best_hook": ""}

        best_idx = min(best_idx, len(hooks) - 1)
        result["best_hook"] = hooks[best_idx]

        success(f"Generated {len(hooks)} hooks. Best: #{best_idx + 1}")
        return result
    except Exception as e:
        warning(f"Hook generation failed: {e}")
        return {"hooks": [], "best_index": 0, "best_hook": ""}


def apply_hook_to_script(script: str, hook: str) -> str:
    """
    Replaces the first sentence of the script with the hook.

    Args:
        script: Original video script
        hook: The hook to prepend

    Returns:
        Modified script with the hook as the opening
    """
    import re
    sentences = re.split(r'(?<=[.!?])\s+', script.strip())
    if sentences:
        sentences[0] = hook
    return " ".join(sentences)
