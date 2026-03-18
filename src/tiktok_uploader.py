import os
import time
from status import info, success, warning, error
from config import get_headless, _load_config

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.firefox import GeckoDriverManager
except ImportError:
    pass


class TikTokUploader:
    """
    Uploads videos to TikTok via Selenium browser automation.
    Requires a pre-logged-in Firefox profile.
    """

    def __init__(self, firefox_profile_path: str) -> None:
        self.options = Options()

        if get_headless():
            self.options.add_argument("--headless")

        if not os.path.isdir(firefox_profile_path):
            raise ValueError(f"Firefox profile path does not exist: {firefox_profile_path}")

        self.options.add_argument("-profile")
        self.options.add_argument(firefox_profile_path)

        self.service = Service(GeckoDriverManager().install())
        self.browser = webdriver.Firefox(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.browser, 30)

    def upload(self, video_path: str, description: str, tags: list = None) -> bool:
        """
        Uploads a video to TikTok.

        Args:
            video_path: Path to the video file
            description: Video description/caption
            tags: List of hashtags (without #)

        Returns:
            True if upload was successful
        """
        driver = self.browser

        try:
            # Navigate to TikTok upload page
            driver.get("https://www.tiktok.com/upload")
            time.sleep(5)

            # Find file input and send video
            file_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(os.path.abspath(video_path))

            info(" => Video file selected, waiting for upload...")
            time.sleep(10)

            # Find caption/description input
            caption_selectors = [
                (By.CSS_SELECTOR, "div[contenteditable='true']"),
                (By.XPATH, "//div[@data-placeholder]//div[@contenteditable='true']"),
                (By.XPATH, "//div[@role='textbox']"),
            ]

            caption_box = None
            for selector in caption_selectors:
                try:
                    caption_box = self.wait.until(EC.element_to_be_clickable(selector))
                    break
                except Exception:
                    continue

            if caption_box:
                caption_box.clear()

                # Build caption with tags
                full_caption = description
                if tags:
                    hashtags = " ".join(f"#{tag}" for tag in tags)
                    full_caption = f"{description} {hashtags}"

                caption_box.send_keys(full_caption)

            time.sleep(3)

            # Click post button
            post_selectors = [
                (By.XPATH, "//button[contains(text(), 'Post')]"),
                (By.XPATH, "//button[@data-e2e='upload-btn']"),
                (By.CSS_SELECTOR, "button.tiktok-btn-pc-primary"),
            ]

            for selector in post_selectors:
                try:
                    post_btn = self.wait.until(EC.element_to_be_clickable(selector))
                    post_btn.click()
                    break
                except Exception:
                    continue

            time.sleep(5)
            success(" => Video uploaded to TikTok!")
            return True

        except Exception as e:
            error(f"TikTok upload failed: {e}")
            return False
        finally:
            driver.quit()
