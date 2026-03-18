from llm_provider import generate_text
from status import info, success, warning


def generate_promo_comment(video_title: str, video_url: str, niche: str) -> str:
    """
    Generates a natural-sounding promotional comment for cross-promotion.

    Args:
        video_title: Title of the video to promote
        video_url: URL of the video
        niche: Channel niche

    Returns:
        A promotional comment string
    """
    prompt = f"""Write a short, natural-sounding comment that promotes a YouTube video.
The comment should NOT look like spam. It should add value to the conversation.
Video title: {video_title}
Video URL: {video_url}
Niche: {niche}

The comment should:
- Be under 200 characters
- Feel like a genuine recommendation
- Include the video URL naturally
- Not use excessive emojis or caps

Only return the comment text, nothing else."""

    try:
        return generate_text(prompt)
    except Exception as e:
        warning(f"Failed to generate promo comment: {e}")
        return ""


def generate_promo_tweet(video_title: str, video_url: str, niche: str) -> str:
    """
    Generates a promotional tweet for a video.
    """
    prompt = f"""Write a tweet promoting this YouTube Short:
Title: {video_title}
URL: {video_url}
Niche: {niche}

The tweet should:
- Be under 250 characters
- Be engaging and shareable
- Include the URL
- Include 2-3 relevant hashtags

Only return the tweet text, nothing else."""

    try:
        return generate_text(prompt)
    except Exception as e:
        warning(f"Failed to generate promo tweet: {e}")
        return ""
