import os
import requests
from uuid import uuid4
from config import ROOT_DIR, get_pexels_api_key
from status import info, warning, error

PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"
PEXELS_IMAGE_URL = "https://api.pexels.com/v1/search"


def search_stock_videos(query: str, count: int = 5, orientation: str = "portrait") -> list:
    """
    Searches Pexels for stock videos.

    Args:
        query: Search query
        count: Number of results
        orientation: "portrait" or "landscape"

    Returns:
        List of video dicts with 'url', 'download_url', 'width', 'height'
    """
    api_key = get_pexels_api_key()
    if not api_key:
        warning("Pexels API key not configured. Set pexels_api_key in config.json")
        return []

    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "per_page": count,
        "orientation": orientation,
    }

    try:
        response = requests.get(PEXELS_VIDEO_URL, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = []
        for video in data.get("videos", []):
            # Get the HD file
            for file in video.get("video_files", []):
                if file.get("quality") == "hd" and file.get("width", 0) >= 720:
                    results.append({
                        "id": video["id"],
                        "url": video["url"],
                        "download_url": file["link"],
                        "width": file["width"],
                        "height": file["height"],
                    })
                    break
        return results
    except Exception as e:
        warning(f"Failed to search Pexels videos: {e}")
        return []


def search_stock_images(query: str, count: int = 5, orientation: str = "portrait") -> list:
    """
    Searches Pexels for stock images.
    """
    api_key = get_pexels_api_key()
    if not api_key:
        warning("Pexels API key not configured.")
        return []

    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "per_page": count,
        "orientation": orientation,
    }

    try:
        response = requests.get(PEXELS_IMAGE_URL, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = []
        for photo in data.get("photos", []):
            results.append({
                "id": photo["id"],
                "url": photo["url"],
                "download_url": photo["src"]["large2x"],
                "width": photo["width"],
                "height": photo["height"],
            })
        return results
    except Exception as e:
        warning(f"Failed to search Pexels images: {e}")
        return []


def download_stock_video(url: str) -> str:
    """
    Downloads a stock video and saves it to .mp directory.

    Returns:
        Path to the downloaded video file
    """
    output_path = os.path.join(ROOT_DIR, ".mp", f"stock_{uuid4()}.mp4")

    try:
        response = requests.get(url, timeout=120, stream=True)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        info(f" => Downloaded stock video to {output_path}")
        return output_path
    except Exception as e:
        warning(f"Failed to download stock video: {e}")
        return None


def download_stock_image(url: str) -> str:
    """
    Downloads a stock image and saves it to .mp directory.

    Returns:
        Path to the downloaded image file
    """
    output_path = os.path.join(ROOT_DIR, ".mp", f"stock_{uuid4()}.png")

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        info(f" => Downloaded stock image to {output_path}")
        return output_path
    except Exception as e:
        warning(f"Failed to download stock image: {e}")
        return None
