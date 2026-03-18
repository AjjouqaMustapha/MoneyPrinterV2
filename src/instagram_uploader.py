import os
import time
from status import info, success, warning, error
from config import get_headless

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


class InstagramUploader:
    """
    Uploads Reels to Instagram via Selenium browser automation.
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

    def upload_reel(self, video_path: str, caption: str) -> bool:
        """
        Uploads a video as an Instagram Reel.

        Args:
            video_path: Path to the video file
            caption: Reel caption

        Returns:
            True if upload was successful
        """
        driver = self.browser

        try:
            # Navigate to Instagram
            driver.get("https://www.instagram.com/")
            time.sleep(5)

            # Click the create/new post button
            create_selectors = [
                (By.XPATH, "//span[text()='Create']//ancestor::a"),
                (By.XPATH, "//*[@aria-label='New post']"),
                (By.CSS_SELECTOR, "svg[aria-label='New post']"),
            ]

            for selector in create_selectors:
                try:
                    create_btn = self.wait.until(EC.element_to_be_clickable(selector))
                    create_btn.click()
                    break
                except Exception:
                    continue

            time.sleep(3)

            # Select file input
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_input.send_keys(os.path.abspath(video_path))

            info(" => Video file selected, waiting for processing...")
            time.sleep(10)

            # Click through steps (crop, filters, etc.)
            next_selectors = [
                (By.XPATH, "//button[text()='Next']"),
                (By.XPATH, "//div[text()='Next']"),
            ]

            # Click Next twice (crop -> filters -> caption)
            for _ in range(2):
                time.sleep(2)
                for selector in next_selectors:
                    try:
                        next_btn = self.wait.until(EC.element_to_be_clickable(selector))
                        next_btn.click()
                        break
                    except Exception:
                        continue

            time.sleep(3)

            # Enter caption
            caption_box = driver.find_element(By.CSS_SELECTOR, "textarea[aria-label='Write a caption...']")
            caption_box.send_keys(caption)

            time.sleep(2)

            # Click Share
            share_selectors = [
                (By.XPATH, "//button[text()='Share']"),
                (By.XPATH, "//div[text()='Share']"),
            ]

            for selector in share_selectors:
                try:
                    share_btn = self.wait.until(EC.element_to_be_clickable(selector))
                    share_btn.click()
                    break
                except Exception:
                    continue

            time.sleep(10)
            success(" => Reel uploaded to Instagram!")
            return True

        except Exception as e:
            error(f"Instagram upload failed: {e}")
            return False
        finally:
            driver.quit()
