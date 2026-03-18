import os
import json
import http.client
import httplib2
from config import ROOT_DIR, _load_config
from status import info, success, warning, error

# YouTube API upload scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

CREDENTIALS_PATH = os.path.join(ROOT_DIR, "client_secrets.json")
TOKEN_PATH = os.path.join(ROOT_DIR, ".mp", "youtube_token.json")


def get_authenticated_service():
    """
    Gets an authenticated YouTube API service.
    Requires client_secrets.json in the project root.

    Returns:
        YouTube API service object
    """
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        error("YouTube API dependencies not installed. Run: pip install google-api-python-client google-auth-oauthlib")
        return None

    credentials = None

    # Load saved token
    if os.path.exists(TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If no valid credentials, authenticate
    if not credentials or not credentials.valid:
        if not os.path.exists(CREDENTIALS_PATH):
            warning(
                f"client_secrets.json not found at {CREDENTIALS_PATH}. "
                "Download it from Google Cloud Console > APIs > Credentials > OAuth 2.0 Client ID"
            )
            return None

        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        credentials = flow.run_local_server(port=0)

        # Save credentials
        with open(TOKEN_PATH, "w") as f:
            f.write(credentials.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def upload_video_api(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    privacy: str = "unlisted",
    is_short: bool = True,
) -> str:
    """
    Uploads a video to YouTube using the official Data API v3.

    Args:
        video_path: Path to the video file
        title: Video title
        description: Video description
        tags: List of tags
        privacy: "public", "unlisted", or "private"
        is_short: Whether this is a YouTube Short

    Returns:
        video_id: The uploaded video ID, or None on failure
    """
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        error("google-api-python-client not installed.")
        return None

    youtube = get_authenticated_service()
    if not youtube:
        return None

    if tags is None:
        tags = []

    # Add #Shorts tag if it's a short
    if is_short and "#Shorts" not in tags:
        tags.append("#Shorts")

    body = {
        "snippet": {
            "title": title,
            "description": description + ("\n\n#Shorts" if is_short else ""),
            "tags": tags,
            "categoryId": "22",  # People & Blogs
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)

    info(f" => Uploading video via YouTube API: {title[:50]}...")

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                info(f" => Upload progress: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        success(f" => Video uploaded: {video_url}")

        return video_id

    except Exception as e:
        error(f"YouTube API upload failed: {e}")
        return None
