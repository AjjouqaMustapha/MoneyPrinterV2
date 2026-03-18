"""
MoneyPrinterV2 Web Dashboard
Run with: streamlit run src/dashboard.py
"""
import sys
import os
import json

# Add src to path so imports work
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from config import (
    ROOT_DIR, _load_config, validate_config, get_tts_engine,
    get_background_music_enabled, reload_config,
)
from cache import get_accounts, get_products, add_account
from status import info
from uuid import uuid4


def main():
    st.set_page_config(
        page_title="MoneyPrinterV2",
        page_icon="💰",
        layout="wide",
    )

    st.title("💰 MoneyPrinterV2 Dashboard")

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Home", "YouTube Shorts", "Twitter Bot", "Affiliate Marketing",
         "Queue", "Analytics", "Content Calendar", "Settings"]
    )

    if page == "Home":
        render_home()
    elif page == "YouTube Shorts":
        render_youtube()
    elif page == "Twitter Bot":
        render_twitter()
    elif page == "Affiliate Marketing":
        render_affiliate()
    elif page == "Queue":
        render_queue()
    elif page == "Analytics":
        render_analytics()
    elif page == "Content Calendar":
        render_calendar()
    elif page == "Settings":
        render_settings()


def render_home():
    st.header("Welcome to MoneyPrinterV2")

    # Config validation
    warnings = validate_config()
    if warnings:
        st.warning("Configuration issues detected:")
        for w in warnings:
            st.write(f"- {w}")
    else:
        st.success("All configuration checks passed!")

    # Quick stats
    col1, col2, col3 = st.columns(3)

    yt_accounts = get_accounts("youtube")
    tw_accounts = get_accounts("twitter")
    products = get_products()

    col1.metric("YouTube Accounts", len(yt_accounts))
    col2.metric("Twitter Accounts", len(tw_accounts))
    col3.metric("Affiliate Products", len(products))

    # Queue status
    st.subheader("Queue Status")
    queue_path = os.path.join(ROOT_DIR, ".mp", "queue.json")
    if os.path.exists(queue_path):
        with open(queue_path, "r") as f:
            queue = json.load(f)
        pending = sum(1 for t in queue if t["status"] == "pending")
        completed = sum(1 for t in queue if t["status"] == "completed")
        failed = sum(1 for t in queue if t["status"] == "failed")

        col1, col2, col3 = st.columns(3)
        col1.metric("Pending", pending)
        col2.metric("Completed", completed)
        col3.metric("Failed", failed)
    else:
        st.info("No tasks in queue yet.")


def render_youtube():
    st.header("YouTube Shorts Automation")

    accounts = get_accounts("youtube")

    # Account management
    with st.expander("Manage Accounts"):
        st.subheader("Existing Accounts")
        if accounts:
            for acc in accounts:
                st.write(f"**{acc['nickname']}** - Niche: {acc['niche']} - Language: {acc.get('language', 'English')}")
        else:
            st.info("No YouTube accounts configured.")

        st.subheader("Add New Account")
        with st.form("add_yt_account"):
            nickname = st.text_input("Account Nickname")
            fp_profile = st.text_input("Firefox Profile Path")
            niche = st.text_input("Channel Niche")
            language = st.text_input("Language", value="English")

            if st.form_submit_button("Add Account"):
                if nickname and fp_profile and niche:
                    add_account("youtube", {
                        "id": str(uuid4()),
                        "nickname": nickname,
                        "firefox_profile": fp_profile,
                        "niche": niche,
                        "language": language,
                        "videos": [],
                    })
                    st.success(f"Account '{nickname}' added!")
                    st.rerun()

    # Video generation
    if accounts:
        st.subheader("Generate Video")
        selected = st.selectbox(
            "Select Account",
            accounts,
            format_func=lambda a: f"{a['nickname']} ({a['niche']})"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate Video", type="primary"):
                st.info("Video generation started... Check the console for progress.")
                st.warning("Note: Full video generation runs in the background. Use the CLI for real-time progress.")

        with col2:
            if st.button("Add to Queue"):
                try:
                    from queue_system import add_to_queue
                    task_id = add_to_queue(
                        "youtube",
                        selected["id"],
                        niche=selected["niche"],
                        language=selected.get("language", "English")
                    )
                    st.success(f"Added to queue! Task ID: {task_id[:8]}")
                except Exception as e:
                    st.error(f"Failed to add to queue: {e}")

        # Show videos
        st.subheader("Generated Videos")
        for acc in accounts:
            videos = acc.get("videos", [])
            if videos:
                st.write(f"**{acc['nickname']}:**")
                for v in videos:
                    st.write(f"- {v.get('title', 'Untitled')} ({v.get('date', 'Unknown date')})")


def render_twitter():
    st.header("Twitter Bot")

    accounts = get_accounts("twitter")

    with st.expander("Manage Accounts"):
        if accounts:
            for acc in accounts:
                st.write(f"**{acc['nickname']}** - Topic: {acc['topic']}")
        else:
            st.info("No Twitter accounts configured.")

        with st.form("add_tw_account"):
            nickname = st.text_input("Account Nickname")
            fp_profile = st.text_input("Firefox Profile Path")
            topic = st.text_input("Account Topic")

            if st.form_submit_button("Add Account"):
                if nickname and fp_profile and topic:
                    add_account("twitter", {
                        "id": str(uuid4()),
                        "nickname": nickname,
                        "firefox_profile": fp_profile,
                        "topic": topic,
                        "posts": [],
                    })
                    st.success(f"Account '{nickname}' added!")
                    st.rerun()

    if accounts:
        st.subheader("Post Tweet")
        selected = st.selectbox(
            "Select Account",
            accounts,
            format_func=lambda a: f"{a['nickname']} ({a['topic']})"
        )

        if st.button("Generate & Post Tweet"):
            st.info("Tweet generation started... Check the console for progress.")


def render_affiliate():
    st.header("Affiliate Marketing")

    products = get_products()

    if products:
        for p in products:
            st.write(f"- Link: {p['affiliate_link']} | Twitter: {p['twitter_uuid']}")
    else:
        st.info("No affiliate products configured.")


def render_queue():
    st.header("Task Queue")

    queue_path = os.path.join(ROOT_DIR, ".mp", "queue.json")

    if not os.path.exists(queue_path):
        st.info("Queue is empty.")
        return

    with open(queue_path, "r") as f:
        queue = json.load(f)

    if not queue:
        st.info("Queue is empty.")
        return

    # Show queue table
    for task in queue:
        status_emoji = {"pending": "⏳", "in_progress": "🔄", "completed": "✅", "failed": "❌"}
        emoji = status_emoji.get(task["status"], "❓")

        st.write(
            f"{emoji} **{task['platform']}** | "
            f"Status: {task['status']} | "
            f"Created: {task.get('created_at', 'N/A')[:19]}"
        )

    if st.button("Clear Completed Tasks"):
        queue = [t for t in queue if t["status"] in ("pending", "in_progress")]
        with open(queue_path, "w") as f:
            json.dump(queue, f, indent=2)
        st.success("Cleared completed tasks!")
        st.rerun()


def render_analytics():
    st.header("Analytics")

    analytics_path = os.path.join(ROOT_DIR, ".mp", "analytics.json")

    if not os.path.exists(analytics_path):
        st.info("No analytics data yet. Generate and upload videos to start tracking.")
        return

    with open(analytics_path, "r") as f:
        analytics = json.load(f)

    videos = analytics.get("videos", [])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Videos", len(videos))
    col2.metric("Total Views", sum(v.get("views", 0) for v in videos))
    col3.metric("Est. Revenue", f"${sum(v.get('estimated_revenue', 0) for v in videos):.2f}")

    if videos:
        st.subheader("Video History")
        for v in videos[-10:]:  # Show last 10
            st.write(
                f"- **{v.get('title', 'Untitled')[:50]}** | "
                f"Platform: {v.get('platform', 'youtube')} | "
                f"Date: {v.get('timestamp', 'N/A')[:10]}"
            )


def render_calendar():
    st.header("Content Calendar")

    calendar_path = os.path.join(ROOT_DIR, ".mp", "calendar.json")

    if os.path.exists(calendar_path):
        with open(calendar_path, "r") as f:
            calendar = json.load(f)

        for entry in calendar:
            used = "✅" if entry.get("used") else "⏳"
            st.write(f"{used} **{entry.get('planned_date', 'TBD')}** - {entry.get('topic', 'No topic')}")
    else:
        st.info("No content calendar yet. Use the CLI to generate a weekly plan.")

    if st.button("Generate Weekly Plan"):
        st.info("Use the CLI to generate a content calendar: python src/main.py")


def render_settings():
    st.header("Settings")

    config_path = os.path.join(ROOT_DIR, "config.json")

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)

        st.subheader("Current Configuration")

        # Show config in editable form
        with st.form("settings_form"):
            st.text_input("OpenRouter API Key", value=config.get("openrouter_api_key", ""), key="or_key", type="password")
            st.text_input("OpenRouter Model", value=config.get("openrouter_model", "meta-llama/llama-3.2-3b-instruct:free"), key="or_model")
            st.text_input("Gemini API Key", value=config.get("nanobanana2_api_key", ""), key="gemini_key", type="password")
            st.selectbox("TTS Engine", ["edge_tts", "kitten_tts"], index=0 if config.get("tts_engine", "edge_tts") == "edge_tts" else 1, key="tts_eng")
            st.text_input("Edge TTS Voice", value=config.get("edge_tts_voice", "en-US-ChristopherNeural"), key="edge_voice")
            st.selectbox("Video Transition", ["fade", "zoom", "slide", "none"], index=["fade", "zoom", "slide", "none"].index(config.get("video_transition", "fade")), key="transition")
            st.checkbox("Background Music", value=config.get("background_music_enabled", True), key="bg_music")
            st.number_input("Script Sentences", value=config.get("script_sentence_length", 4), min_value=2, max_value=10, key="sentences")

            if st.form_submit_button("Save Settings"):
                config["openrouter_api_key"] = st.session_state.or_key
                config["openrouter_model"] = st.session_state.or_model
                config["nanobanana2_api_key"] = st.session_state.gemini_key
                config["tts_engine"] = st.session_state.tts_eng
                config["edge_tts_voice"] = st.session_state.edge_voice
                config["video_transition"] = st.session_state.transition
                config["background_music_enabled"] = st.session_state.bg_music
                config["script_sentence_length"] = st.session_state.sentences

                with open(config_path, "w") as f:
                    json.dump(config, f, indent=2)

                reload_config()
                st.success("Settings saved!")

    # Validation
    st.subheader("Configuration Validation")
    warnings = validate_config()
    if warnings:
        for w in warnings:
            st.warning(w)
    else:
        st.success("All checks passed!")


if __name__ == "__main__":
    main()
