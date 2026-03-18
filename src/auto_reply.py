import time
import re
from status import info, success, warning, error
from llm_provider import generate_text
from config import get_headless, get_verbose

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


class AutoReplyBot:
    """
    Automatically replies to comments on YouTube videos to boost engagement.
    Uses LLM to generate contextual, natural-sounding replies.
    """

    def __init__(self, firefox_profile_path: str) -> None:
        self.options = Options()
        if get_headless():
            self.options.add_argument("--headless")
        self.options.add_argument("-profile")
        self.options.add_argument(firefox_profile_path)
        self.service = Service(GeckoDriverManager().install())
        self.browser = webdriver.Firefox(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.browser, 20)

    def get_comments(self, video_url: str, max_comments: int = 20) -> list:
        """
        Fetches comments from a YouTube video.

        Args:
            video_url: YouTube video URL
            max_comments: Maximum number of comments to fetch

        Returns:
            List of dicts with 'author', 'text', 'element' keys
        """
        driver = self.browser
        driver.get(video_url)
        time.sleep(5)

        # Scroll down to load comments
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(2)

        comments = []
        try:
            comment_elements = driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")

            for elem in comment_elements[:max_comments]:
                try:
                    author = elem.find_element(By.CSS_SELECTOR, "#author-text span").text.strip()
                    text = elem.find_element(By.CSS_SELECTOR, "#content-text").text.strip()
                    if author and text:
                        comments.append({
                            "author": author,
                            "text": text,
                            "element": elem,
                        })
                except Exception:
                    continue
        except Exception as e:
            warning(f"Failed to fetch comments: {e}")

        info(f" => Found {len(comments)} comments")
        return comments

    def generate_reply(self, comment_text: str, video_title: str, channel_niche: str) -> str:
        """
        Generates a natural reply to a comment using LLM.

        Args:
            comment_text: The comment to reply to
            video_title: Title of the video
            channel_niche: Channel niche for context

        Returns:
            Reply text string
        """
        prompt = f"""Write a short, friendly reply to this YouTube comment.
The reply should:
- Be 1-2 sentences max
- Feel genuine and personal (NOT like a bot)
- Add value or acknowledge the commenter
- NOT use excessive emojis or exclamation marks
- NOT be generic like "Thanks for watching!"

Video title: {video_title}
Channel niche: {channel_niche}
Comment: "{comment_text}"

Only return the reply text, nothing else."""

        try:
            reply = generate_text(prompt)
            # Clean up
            reply = reply.strip().strip('"').strip("'")
            return reply
        except Exception as e:
            warning(f"Failed to generate reply: {e}")
            return ""

    def reply_to_comment(self, comment_element, reply_text: str) -> bool:
        """
        Posts a reply to a specific comment using Selenium.

        Args:
            comment_element: The Selenium element of the comment
            reply_text: The reply text to post

        Returns:
            True if successful
        """
        try:
            # Click reply button
            reply_btn = comment_element.find_element(By.CSS_SELECTOR, "#reply-button-end button")
            reply_btn.click()
            time.sleep(2)

            # Find reply text box
            reply_box = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#contenteditable-root"))
            )
            reply_box.click()
            reply_box.send_keys(reply_text)
            time.sleep(1)

            # Click submit
            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit-button"))
            )
            submit_btn.click()
            time.sleep(2)

            return True
        except Exception as e:
            warning(f"Failed to post reply: {e}")
            return False

    def auto_reply(self, video_url: str, video_title: str, channel_niche: str,
                   max_replies: int = 5, skip_own: bool = True) -> int:
        """
        Automatically replies to comments on a video.

        Args:
            video_url: YouTube video URL
            video_title: Video title for context
            channel_niche: Channel niche
            max_replies: Maximum replies to post
            skip_own: Skip comments from the channel owner

        Returns:
            Number of replies posted
        """
        comments = self.get_comments(video_url)
        replies_posted = 0

        for comment in comments:
            if replies_posted >= max_replies:
                break

            if not comment["text"] or len(comment["text"]) < 5:
                continue

            reply = self.generate_reply(comment["text"], video_title, channel_niche)
            if not reply:
                continue

            if get_verbose():
                info(f' => Replying to "{comment["text"][:50]}..." with: "{reply[:50]}..."')

            if self.reply_to_comment(comment["element"], reply):
                replies_posted += 1
                success(f" => Reply {replies_posted}/{max_replies} posted")
                time.sleep(3)  # Delay between replies to look natural

        success(f" => Auto-reply complete: {replies_posted} replies posted")
        return replies_posted

    def close(self):
        """Closes the browser."""
        self.browser.quit()
