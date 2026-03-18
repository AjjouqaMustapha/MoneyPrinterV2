# MoneyPrinter V2

> Fork of [FujiwaraChoki/MoneyPrinterV2](https://github.com/FujiwaraChoki/MoneyPrinterV2) — massively upgraded with 38+ new features.

[![GitHub license](https://img.shields.io/github/license/AjjouqaMustapha/MoneyPrinterV2?style=for-the-badge)](https://github.com/AjjouqaMustapha/MoneyPrinterV2/blob/main/LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](Dockerfile)

An application that automates the process of making money online — generate short-form videos, post to social media, and grow your channels on autopilot.

**No GPU required** — runs entirely on cloud APIs + lightweight CPU tasks.

## What's New in This Fork

This fork replaces the original Ollama (local LLM) dependency with **OpenRouter** (free cloud LLM), adds **Edge-TTS** (300+ voices), **TikTok/Instagram** support, a **Streamlit web dashboard**, and 38+ features total.

### Key Improvements

| Before (Original) | After (This Fork) |
|---|---|
| Requires GPU + Ollama | No GPU needed — uses OpenRouter (free) |
| 5 LLM calls per video | 1 combined call (saves API budget) |
| KittenTTS only (English) | Edge-TTS: 300+ voices, 70+ languages |
| YouTube only | YouTube + TikTok + Instagram |
| CLI only | CLI + Streamlit Web Dashboard |
| Sequential image generation | Parallel (3x faster) |
| Config re-read 30+ times | Cached in memory (1 read) |
| No error recovery | Retry with exponential backoff |
| No subtitles fallback | Local Whisper + AssemblyAI + Groq Whisper |

## Features

### Core Automation
- [x] **YouTube Shorts** — full pipeline: LLM script → images → TTS → video → upload
- [x] **TikTok Bot** — generate & upload short videos via Selenium
- [x] **Twitter/X Bot** — auto-generate and post tweets with CRON scheduling
- [x] **Instagram Reels** — upload videos as Instagram Reels
- [x] **Affiliate Marketing** — scrape Amazon products, generate pitches, share on Twitter
- [x] **Cold Outreach** — scrape Google Maps businesses, send cold emails via SMTP
- [x] **Multi-Platform Upload** — one video → YouTube + TikTok + Instagram simultaneously

### AI & Intelligence
- [x] **OpenRouter LLM** — free cloud models (Llama, Mixtral, etc.) with 1000 req/day
- [x] **Combined LLM Calls** — topic + script + metadata + image prompts in 1 API call
- [x] **Trending Topics** — auto-detect viral topics from Google Trends
- [x] **Hook Optimization** — generate multiple opening hooks, pick the most engaging
- [x] **Script Quality Scoring** — LLM rates scripts, auto-improves if below threshold
- [x] **SEO Optimization** — auto-generate optimized tags, titles, descriptions
- [x] **A/B Title Testing** — generate multiple title variants with different strategies
- [x] **Content Calendar** — plan a week of content, no topic repetition

### Video Production
- [x] **Edge-TTS** — 300+ voices, 70+ languages (free, no GPU)
- [x] **Video Transitions** — fade, zoom, slide effects between scenes
- [x] **Dynamic Subtitles** — word-by-word highlighting (CapCut style)
- [x] **Thumbnail Generation** — auto-generate thumbnails from images + title overlay
- [x] **B-Roll / Stock Footage** — Pexels API for stock videos and images
- [x] **Background Music** — optional, configurable (won't crash if disabled)
- [x] **3 STT Providers** — Local Whisper, AssemblyAI, or Groq Whisper API

### Infrastructure
- [x] **Web Dashboard** — Streamlit UI for account management, queue, analytics, settings
- [x] **Task Queue** — add videos to a queue, process sequentially
- [x] **Resume from Failure** — save pipeline state, continue where it stopped
- [x] **Webhook Notifications** — Discord and Telegram alerts
- [x] **Video Preview** — open video in system player before uploading
- [x] **Timezone Scheduling** — optimal posting times per platform and region
- [x] **YouTube API Upload** — official Data API v3 (alternative to Selenium)
- [x] **Docker Support** — Dockerfile + docker-compose for one-command setup
- [x] **Config Validation** — checks all API keys and paths on startup

### Monetization
- [x] **Faceless Channel Templates** — pre-built configs for 5 niches (scary stories, motivation, fun facts, cooking, tech tips)
- [x] **Prompt Templates** — 10 editable prompt files in `prompts/` directory
- [x] **Analytics Tracking** — track videos, views, revenue by niche/platform
- [x] **Revenue Estimation** — CPM-based revenue tracking
- [x] **Cross-Promotion** — generate natural promo comments and tweets

## Installation

### Prerequisites
- Python 3.12+
- Firefox (for Selenium automation)
- ImageMagick ([download](https://imagemagick.org/script/download.php))

### Quick Start

```bash
git clone https://github.com/AjjouqaMustapha/MoneyPrinterV2.git
cd MoneyPrinterV2

# Copy config and fill in your API keys
cp config.example.json config.json

# Create virtual environment
python -m venv venv

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Activate (Unix/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Docker

```bash
# Run the CLI
docker-compose up moneyprinter

# Run the web dashboard
docker-compose up dashboard
# Open http://localhost:8501
```

## Configuration

Edit `config.json` with your API keys:

```json
{
  "openrouter_api_key": "your-key-here",
  "nanobanana2_api_key": "your-gemini-key-here",
  "imagemagick_path": "C:\\Program Files\\ImageMagick\\magick.exe",
  "firefox_profile": "C:\\Users\\You\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xxx.default-release"
}
```

### Required Keys

| Key | Where to Get | Cost |
|-----|-------------|------|
| `openrouter_api_key` | [openrouter.ai/keys](https://openrouter.ai/keys) | Free (1000 req/day) |
| `nanobanana2_api_key` | [aistudio.google.com](https://aistudio.google.com) | Free tier |
| `imagemagick_path` | [imagemagick.org](https://imagemagick.org/script/download.php) | Free |

### Optional Keys

| Key | For | Cost |
|-----|-----|------|
| `groq_api_key` | Cloud subtitles (Groq Whisper) | Free |
| `pexels_api_key` | Stock footage / B-roll | Free |
| `discord_webhook_url` | Discord notifications | Free |
| `telegram_bot_token` | Telegram notifications | Free |

See [config.example.json](config.example.json) for all available options.

## Usage

### CLI Mode

```bash
python src/main.py
```

```
============ OPTIONS ============
 1. YouTube Shorts Automation
 2. Twitter Bot
 3. TikTok Bot
 4. Affiliate Marketing
 5. Outreach
 6. Quit
=================================
```

### Web Dashboard

```bash
streamlit run src/dashboard.py
```

Opens a browser UI at `http://localhost:8501` with pages for:
- Account management
- Video generation
- Task queue
- Analytics
- Content calendar
- Settings

## Project Structure

```
MoneyPrinterV2/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── dashboard.py            # Streamlit web UI
│   ├── config.py               # Cached config with validation
│   ├── llm_provider.py         # OpenRouter API with retry
│   ├── classes/
│   │   ├── YouTube.py          # Video pipeline + upload
│   │   ├── Twitter.py          # Tweet automation
│   │   ├── Tts.py              # Edge-TTS + KittenTTS
│   │   ├── AFM.py              # Affiliate marketing
│   │   └── Outreach.py         # Cold email outreach
│   ├── tiktok_uploader.py      # TikTok Selenium upload
│   ├── instagram_uploader.py   # Instagram Reels upload
│   ├── multi_platform.py       # Multi-platform orchestrator
│   ├── youtube_api.py          # YouTube Data API v3
│   ├── trending.py             # Google Trends detection
│   ├── hook_optimizer.py       # Opening hook generation
│   ├── script_scorer.py        # Script quality scoring
│   ├── seo.py                  # SEO optimization
│   ├── content_calendar.py     # Weekly content planning
│   ├── ab_testing.py           # A/B title testing
│   ├── analytics.py            # Video analytics + revenue
│   ├── queue_system.py         # Task queue
│   ├── pipeline_state.py       # Resume from failure
│   ├── webhooks.py             # Discord + Telegram
│   ├── thumbnail.py            # Thumbnail generation
│   ├── stock_footage.py        # Pexels API
│   ├── dynamic_subtitles.py    # Word-by-word subtitles
│   └── ...
├── prompts/                    # 10 editable prompt templates
├── templates/                  # 5 faceless channel configs
├── fonts/                      # Subtitle fonts
├── Dockerfile                  # Docker support
├── docker-compose.yml          # CLI + Dashboard services
├── config.example.json         # Config template
├── requirements.txt            # Python dependencies
└── CHECKLIST.md                # Full feature checklist
```

## Video Pipeline

Each video goes through this automated pipeline:

```
1. Generate Content (1 LLM call)
   → topic, script, title, description, image prompts

2. Generate Images (parallel, 3 workers)
   → Gemini API creates 9:16 images

3. Text-to-Speech
   → Edge-TTS converts script to audio

4. Generate Subtitles
   → Local Whisper / Groq / AssemblyAI

5. Compose Video
   → MoviePy: images + audio + subtitles + transitions + music

6. Upload
   → YouTube / TikTok / Instagram (or save locally)
```

**Output:** ~20-40 second vertical video (configurable via `script_sentence_length`)

## Documentation

- [Configuration Reference](docs/Configuration.md)
- [YouTube Feature Guide](docs/YouTube.md)
- [Twitter Bot Guide](docs/TwitterBot.md)
- [Affiliate Marketing Guide](docs/AffiliateMarketing.md)
- [Full Feature Checklist](CHECKLIST.md)

## Credits

- Original project: [FujiwaraChoki/MoneyPrinterV2](https://github.com/FujiwaraChoki/MoneyPrinterV2)
- [Edge-TTS](https://github.com/rany2/edge-tts)
- [OpenRouter](https://openrouter.ai)
- [KittenTTS](https://github.com/KittenML/KittenTTS)

## License

MoneyPrinterV2 is licensed under `Affero General Public License v3.0`. See [LICENSE](LICENSE) for more information.

## Disclaimer

This project is for educational purposes only. The author will not be responsible for any misuse of the information provided. All the information provided is published in good faith and for general information purpose only. Any action you take upon the information you find in this project is strictly at your own risk. The author will not be liable for any losses and/or damages in connection with the use of this project.
