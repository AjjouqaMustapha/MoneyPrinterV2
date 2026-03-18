from llm_provider import generate_structured
from status import info, success, warning


def score_script(script: str, subject: str) -> dict:
    """
    Rates a video script on multiple dimensions and optionally provides improvements.

    Args:
        script: The video script to evaluate
        subject: The video subject/topic

    Returns:
        dict with scores (engagement, clarity, hook, overall), feedback, and optional improved_script
    """
    prompt = f"""Rate the following YouTube Short script on a scale of 1-10 for:
- engagement: how likely viewers will watch till the end
- clarity: how clear and easy to understand
- hook: how strong the opening line is
- overall: overall quality score

Script: {script}
Topic: {subject}

If the overall score is below 7, also provide an "improved_script" with a better version.

Return a JSON object with:
- "engagement": number 1-10
- "clarity": number 1-10
- "hook": number 1-10
- "overall": number 1-10
- "improved_script": string (only if overall < 7, otherwise null)
- "feedback": one sentence explaining the score

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)

        overall = result.get("overall", 5)
        info(f" => Script score: {overall}/10 - {result.get('feedback', 'No feedback')}")

        return result
    except Exception as e:
        warning(f"Script scoring failed: {e}")
        return {
            "engagement": 5,
            "clarity": 5,
            "hook": 5,
            "overall": 5,
            "improved_script": None,
            "feedback": "Scoring unavailable"
        }


def auto_improve_script(script: str, subject: str, min_score: int = 7) -> str:
    """
    Scores a script and automatically improves it if below the minimum score.

    Args:
        script: Original script
        subject: Video subject
        min_score: Minimum acceptable overall score

    Returns:
        The original or improved script
    """
    result = score_script(script, subject)

    if result["overall"] >= min_score:
        success(f" => Script passed quality check ({result['overall']}/10)")
        return script

    if result.get("improved_script"):
        warning(f" => Script scored {result['overall']}/10, using improved version")
        return result["improved_script"]

    return script
