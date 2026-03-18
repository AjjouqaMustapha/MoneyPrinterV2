import schedule
import subprocess
import os
from datetime import datetime, timezone, timedelta
from config import ROOT_DIR, _load_config
from status import info, success, warning


# Timezone offset mapping (common ones)
TIMEZONE_OFFSETS = {
    "UTC": 0,
    "US/Eastern": -5, "US/Central": -6, "US/Mountain": -7, "US/Pacific": -8,
    "Europe/London": 0, "Europe/Berlin": 1, "Europe/Paris": 1, "Europe/Moscow": 3,
    "Asia/Tokyo": 9, "Asia/Shanghai": 8, "Asia/Dubai": 4, "Asia/Kolkata": 5.5,
    "Australia/Sydney": 11,
    "America/Sao_Paulo": -3,
}

# Optimal posting times by platform (in local time)
OPTIMAL_TIMES = {
    "youtube": ["09:00", "12:00", "17:00", "20:00"],
    "twitter": ["08:00", "12:00", "17:00", "19:00"],
    "tiktok": ["07:00", "10:00", "14:00", "19:00"],
    "instagram": ["09:00", "12:00", "15:00", "21:00"],
}


def get_configured_timezone() -> str:
    """
    Gets the timezone from config.

    Returns:
        Timezone string (e.g., "US/Eastern")
    """
    return _load_config().get("timezone", "UTC")


def get_utc_offset(tz_name: str) -> float:
    """
    Gets the UTC offset for a timezone name.
    """
    return TIMEZONE_OFFSETS.get(tz_name, 0)


def local_to_utc(local_time: str, tz_name: str) -> str:
    """
    Converts a local time string (HH:MM) to UTC.

    Args:
        local_time: Time in HH:MM format
        tz_name: Timezone name

    Returns:
        UTC time in HH:MM format
    """
    offset = get_utc_offset(tz_name)
    hours, minutes = map(int, local_time.split(":"))

    utc_hours = (hours - offset) % 24
    return f"{int(utc_hours):02d}:{minutes:02d}"


def get_optimal_times(platform: str) -> list:
    """
    Gets optimal posting times for a platform in the user's timezone.

    Args:
        platform: "youtube", "twitter", "tiktok", "instagram"

    Returns:
        List of time strings in HH:MM format (UTC)
    """
    tz = get_configured_timezone()
    local_times = OPTIMAL_TIMES.get(platform, ["12:00"])

    utc_times = [local_to_utc(t, tz) for t in local_times]
    return utc_times


def schedule_with_timezone(platform: str, account_id: str, frequency: int = 1) -> None:
    """
    Schedules posts/uploads with timezone-aware optimal timing.

    Args:
        platform: "youtube" or "twitter"
        account_id: Account UUID
        frequency: Number of posts per day (1, 2, or 3)
    """
    optimal = get_optimal_times(platform)
    tz = get_configured_timezone()

    # Pick times based on frequency
    times_to_use = optimal[:frequency]

    cron_script_path = os.path.join(ROOT_DIR, "src", "cron.py")
    command = ["python", cron_script_path, platform, account_id]

    def job():
        subprocess.run(command)

    for t in times_to_use:
        schedule.every().day.at(t).do(job)
        info(f" => Scheduled {platform} post at {t} UTC (timezone: {tz})")

    success(f"Set up {frequency} daily {platform} job(s) with timezone: {tz}")
