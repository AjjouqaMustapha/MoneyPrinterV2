import requests
from config import _load_config
from status import info, warning


def send_discord_webhook(message: str, title: str = "MoneyPrinterV2") -> bool:
    """
    Sends a notification to a Discord channel via webhook.

    Args:
        message: The notification message
        title: Embed title

    Returns:
        True if successful
    """
    url = _load_config().get("discord_webhook_url", "")
    if not url:
        return False

    payload = {
        "embeds": [{
            "title": title,
            "description": message,
            "color": 5814783,  # Blue
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        warning(f"Discord webhook failed: {e}")
        return False


def send_telegram_notification(message: str) -> bool:
    """
    Sends a notification via Telegram bot.

    Args:
        message: The notification message

    Returns:
        True if successful
    """
    config = _load_config()
    bot_token = config.get("telegram_bot_token", "")
    chat_id = config.get("telegram_chat_id", "")

    if not bot_token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"*MoneyPrinterV2*\n\n{message}",
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        warning(f"Telegram notification failed: {e}")
        return False


def notify(message: str, title: str = "MoneyPrinterV2") -> None:
    """
    Sends notification to all configured channels.

    Args:
        message: Notification message
        title: Notification title
    """
    sent = False

    if send_discord_webhook(message, title):
        sent = True

    if send_telegram_notification(message):
        sent = True

    if sent:
        info(f" => Notification sent: {message[:50]}...")
