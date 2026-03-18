from llm_provider import generate_structured
from status import info, success, warning


def predict_viral_score(topic: str, title: str, niche: str) -> dict:
    """
    Predicts the viral potential of a video idea BEFORE generating it.
    Helps save API calls by filtering out bad ideas early.

    Args:
        topic: Video topic/idea
        title: Proposed title
        niche: Channel niche

    Returns:
        Dict with scores and recommendation
    """
    prompt = f"""You are a YouTube Shorts viral content expert. Rate this video idea:

Topic: {topic}
Title: {title}
Niche: {niche}

Score each factor from 1-10:
- "curiosity": How likely are people to click? (thumbnail/title appeal)
- "shareability": How likely are viewers to share this?
- "watch_time": How likely are viewers to watch till the end?
- "trend_relevance": How relevant is this to current trends?
- "uniqueness": How different is this from existing content?
- "overall_viral_score": Overall viral potential (weighted average)

Also provide:
- "go_or_no_go": "GO" if overall_viral_score >= 7, "NO_GO" if below
- "improvement_tip": One sentence on how to make it more viral
- "estimated_view_range": Estimated view range like "1K-5K" or "10K-50K"

Return valid JSON only."""

    try:
        result = generate_structured(prompt)

        score = result.get("overall_viral_score", 5)
        verdict = result.get("go_or_no_go", "GO" if score >= 7 else "NO_GO")

        if verdict == "GO":
            success(f" => Viral score: {score}/10 - GO! {result.get('estimated_view_range', '')}")
        else:
            warning(f" => Viral score: {score}/10 - NO GO. {result.get('improvement_tip', '')}")

        return result
    except Exception as e:
        warning(f"Viral prediction failed: {e}")
        return {
            "overall_viral_score": 5,
            "go_or_no_go": "GO",
            "improvement_tip": "Prediction unavailable",
            "estimated_view_range": "Unknown",
        }


def filter_best_idea(ideas: list, niche: str, min_score: int = 7) -> dict:
    """
    Takes multiple video ideas and returns the one with the highest viral score.

    Args:
        ideas: List of dicts with 'topic' and 'title' keys
        niche: Channel niche
        min_score: Minimum acceptable score

    Returns:
        Best idea dict with viral prediction attached, or None if all below threshold
    """
    best = None
    best_score = 0

    for idea in ideas:
        prediction = predict_viral_score(
            topic=idea.get("topic", ""),
            title=idea.get("title", ""),
            niche=niche,
        )

        score = prediction.get("overall_viral_score", 0)
        idea["viral_prediction"] = prediction

        if score > best_score:
            best_score = score
            best = idea

    if best and best_score >= min_score:
        success(f" => Best idea selected with viral score: {best_score}/10")
        return best

    if best:
        warning(f" => Best idea only scored {best_score}/10 (below {min_score} threshold)")
        return best  # Return it anyway, let the caller decide

    return None


def generate_viral_ideas(niche: str, count: int = 5) -> list:
    """
    Generates multiple video ideas and ranks them by viral potential.

    Args:
        niche: Channel niche
        count: Number of ideas to generate

    Returns:
        List of ideas sorted by viral score (highest first)
    """
    prompt = f"""Generate {count} YouTube Short video ideas for the niche: {niche}.
Each idea should have high viral potential.
Use techniques like: shocking facts, contrarian takes, emotional hooks, trending topics.

Return a JSON object with:
- "ideas": array of objects, each with "topic" (string) and "title" (string under 100 chars)

YOU MUST ONLY RETURN VALID JSON."""

    try:
        result = generate_structured(prompt)
        ideas = result.get("ideas", [])

        # Score each idea
        scored = []
        for idea in ideas:
            prediction = predict_viral_score(idea["topic"], idea["title"], niche)
            idea["viral_score"] = prediction.get("overall_viral_score", 0)
            idea["prediction"] = prediction
            scored.append(idea)

        # Sort by score descending
        scored.sort(key=lambda x: x["viral_score"], reverse=True)

        info(f" => Generated and ranked {len(scored)} viral ideas")
        return scored
    except Exception as e:
        warning(f"Viral idea generation failed: {e}")
        return []
