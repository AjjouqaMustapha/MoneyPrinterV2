from status import info, success, warning, error
from llm_provider import generate_structured

# Platform monetization requirements
REQUIREMENTS = {
    "youtube": {
        "name": "YouTube Partner Program (Shorts)",
        "subscribers": 500,
        "watch_hours": 3000,  # or 3M Shorts views in 90 days
        "shorts_views_90d": 3_000_000,
        "min_age_days": 30,
        "requirements": [
            "500+ subscribers",
            "3,000 watch hours in last 12 months OR 3M Shorts views in 90 days",
            "Channel must be at least 30 days old",
            "No active Community Guidelines strikes",
            "2-step verification enabled",
            "AdSense account linked",
        ],
    },
    "tiktok": {
        "name": "TikTok Creator Fund / Creativity Program",
        "followers": 10_000,
        "views_30d": 100_000,
        "min_age_days": 30,
        "min_user_age": 18,
        "requirements": [
            "10,000+ followers",
            "100,000+ views in last 30 days",
            "Account at least 30 days old",
            "Must be 18+ years old",
            "Based in eligible country (US, UK, DE, FR, ES, IT)",
            "Follow Community Guidelines",
        ],
    },
    "instagram": {
        "name": "Instagram Reels Bonus / Subscriptions",
        "followers": 10_000,
        "requirements": [
            "10,000+ followers (for some features)",
            "Professional or Creator account",
            "Follow Instagram Partner Monetization Policies",
            "Based in eligible country",
            "Must be 18+ years old",
        ],
    },
}


def check_monetization_status(
    platform: str,
    subscribers: int = 0,
    views_30d: int = 0,
    watch_hours: int = 0,
    account_age_days: int = 0,
) -> dict:
    """
    Checks if a channel meets monetization requirements.

    Args:
        platform: "youtube", "tiktok", or "instagram"
        subscribers: Current subscriber/follower count
        views_30d: Views in last 30 days
        watch_hours: Watch hours in last 12 months (YouTube only)
        account_age_days: Account age in days

    Returns:
        Dict with eligibility status, progress, and missing requirements
    """
    if platform not in REQUIREMENTS:
        return {"error": f"Unknown platform: {platform}"}

    reqs = REQUIREMENTS[platform]
    checks = []
    passed = 0
    total = 0

    if platform == "youtube":
        total = 3
        # Subscribers
        sub_req = reqs["subscribers"]
        sub_met = subscribers >= sub_req
        checks.append({
            "requirement": f"{sub_req}+ subscribers",
            "current": subscribers,
            "target": sub_req,
            "met": sub_met,
            "progress": min(100, round(subscribers / sub_req * 100, 1)),
        })
        if sub_met:
            passed += 1

        # Watch hours or Shorts views
        wh_met = watch_hours >= reqs["watch_hours"]
        checks.append({
            "requirement": f"{reqs['watch_hours']}+ watch hours",
            "current": watch_hours,
            "target": reqs["watch_hours"],
            "met": wh_met,
            "progress": min(100, round(watch_hours / reqs["watch_hours"] * 100, 1)),
        })
        if wh_met:
            passed += 1

        # Account age
        age_met = account_age_days >= reqs["min_age_days"]
        checks.append({
            "requirement": f"{reqs['min_age_days']}+ days old",
            "current": account_age_days,
            "target": reqs["min_age_days"],
            "met": age_met,
            "progress": min(100, round(account_age_days / reqs["min_age_days"] * 100, 1)),
        })
        if age_met:
            passed += 1

    elif platform == "tiktok":
        total = 3
        # Followers
        fol_req = reqs["followers"]
        fol_met = subscribers >= fol_req
        checks.append({
            "requirement": f"{fol_req}+ followers",
            "current": subscribers,
            "target": fol_req,
            "met": fol_met,
            "progress": min(100, round(subscribers / fol_req * 100, 1)),
        })
        if fol_met:
            passed += 1

        # Views
        view_req = reqs["views_30d"]
        view_met = views_30d >= view_req
        checks.append({
            "requirement": f"{view_req:,}+ views in 30 days",
            "current": views_30d,
            "target": view_req,
            "met": view_met,
            "progress": min(100, round(views_30d / view_req * 100, 1)),
        })
        if view_met:
            passed += 1

        # Age
        age_met = account_age_days >= reqs["min_age_days"]
        checks.append({
            "requirement": f"{reqs['min_age_days']}+ days old",
            "current": account_age_days,
            "target": reqs["min_age_days"],
            "met": age_met,
            "progress": min(100, round(account_age_days / reqs["min_age_days"] * 100, 1)),
        })
        if age_met:
            passed += 1

    elif platform == "instagram":
        total = 1
        fol_req = reqs["followers"]
        fol_met = subscribers >= fol_req
        checks.append({
            "requirement": f"{fol_req}+ followers",
            "current": subscribers,
            "target": fol_req,
            "met": fol_met,
            "progress": min(100, round(subscribers / fol_req * 100, 1)) if fol_req else 100,
        })
        if fol_met:
            passed += 1

    eligible = passed == total

    result = {
        "platform": platform,
        "program_name": reqs["name"],
        "eligible": eligible,
        "checks_passed": passed,
        "checks_total": total,
        "checks": checks,
        "all_requirements": reqs["requirements"],
    }

    if eligible:
        success(f" => {platform}: Eligible for monetization!")
    else:
        warning(f" => {platform}: {passed}/{total} requirements met")
        for c in checks:
            if not c["met"]:
                info(f"    - {c['requirement']}: {c['progress']}% ({c['current']}/{c['target']})")

    return result


def estimate_time_to_monetization(
    platform: str,
    current_subscribers: int,
    daily_subscriber_growth: int,
    current_views_30d: int = 0,
    daily_view_growth: int = 0,
) -> dict:
    """
    Estimates how long until monetization requirements are met.

    Args:
        platform: Platform name
        current_subscribers: Current count
        daily_subscriber_growth: Average daily new subscribers
        current_views_30d: Current 30-day views
        daily_view_growth: Average daily view increase

    Returns:
        Dict with estimated days and date for each requirement
    """
    reqs = REQUIREMENTS.get(platform, {})
    estimates = []

    if platform == "youtube":
        sub_target = reqs.get("subscribers", 500)
        if current_subscribers < sub_target and daily_subscriber_growth > 0:
            days = (sub_target - current_subscribers) / daily_subscriber_growth
            estimates.append({
                "requirement": f"{sub_target} subscribers",
                "days_remaining": round(days),
                "current_rate": f"{daily_subscriber_growth}/day",
            })
        elif current_subscribers >= sub_target:
            estimates.append({"requirement": f"{sub_target} subscribers", "days_remaining": 0})

    elif platform == "tiktok":
        fol_target = reqs.get("followers", 10000)
        if current_subscribers < fol_target and daily_subscriber_growth > 0:
            days = (fol_target - current_subscribers) / daily_subscriber_growth
            estimates.append({
                "requirement": f"{fol_target} followers",
                "days_remaining": round(days),
                "current_rate": f"{daily_subscriber_growth}/day",
            })

    max_days = max((e.get("days_remaining", 0) for e in estimates), default=0)

    return {
        "platform": platform,
        "estimates": estimates,
        "estimated_total_days": max_days,
        "tip": "Consistency is key! Post daily to maintain growth rate.",
    }
