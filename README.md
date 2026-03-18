<p align="center">
  <h1 align="center">MoneyPrinterV2</h1>
  <p align="center"><strong>AI-Powered Multi-Platform Video Generator</strong></p>
  <p align="center">Generate, optimize, and publish short-form videos across YouTube, TikTok, Instagram, and Twitter — fully automated, no GPU required.</p>
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-AGPL--3.0-green?style=for-the-badge" alt="License AGPL-3.0"></a>
  <a href="Dockerfile"><img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Ready"></a>
  <a href="#"><img src="https://img.shields.io/badge/Platforms-4-FF6F00?style=for-the-badge" alt="4 Platforms"></a>
  <a href="#"><img src="https://img.shields.io/badge/No%20GPU-Required-success?style=for-the-badge" alt="No GPU Required"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features-overview">Features</a> &bull;
  <a href="#configuration">Configuration</a> &bull;
  <a href="#usage">Usage</a> &bull;
  <a href="#modules-reference">Modules</a> &bull;
  <a href="#api-keys">API Keys</a>
</p>

---

## Table of Contents

- [About](#about)
- [Features Overview](#features-overview)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Modules Reference](#modules-reference)
- [API Keys](#api-keys)
- [Platform Support](#platform-support)
- [Advanced Features](#advanced-features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Video Pipeline](#video-pipeline)
- [Templates and Prompts](#templates-and-prompts)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## About

MoneyPrinterV2 is a fully automated content creation and distribution engine. It takes a topic (or finds one for you), writes a script using AI, generates images, converts the script to speech, composes a polished short-form video with subtitles and transitions, and uploads it to one or more platforms — all in a single command.

This is an upgraded fork of [FujiwaraChoki/MoneyPrinterV2](https://github.com/FujiwaraChoki/MoneyPrinterV2) with 50+ new modules covering AI intelligence, multi-platform distribution, analytics, scheduling, and batch generation.

**Key differences from the original:**

| Original | This Fork |
|---|---|
| Requires GPU + local Ollama | No GPU needed — uses OpenRouter (free tier) |
| 5 LLM calls per video | 1 combined call (saves API budget) |
| KittenTTS only (English) | Edge-TTS: 300+ voices, 70+ languages |
| YouTube only | YouTube + TikTok + Instagram + Twitter |
| CLI only | CLI + Streamlit Web Dashboard + Docker |
| Sequential image generation | Parallel workers (3x faster) |
| Config re-read on every call | Cached in memory (single read) |
| No error recovery | Retry with exponential backoff |
| No subtitles fallback | Local Whisper + AssemblyAI + Groq Whisper |

---

## Features Overview

### Video Generation
| Feature | Description |
|---|---|
| YouTube Shorts Pipeline | End-to-end: script, images, TTS, subtitles, transitions, upload |
| Dynamic Subtitles | Word-by-word highlighting with multiple styles (karaoke, bounce, typewriter, fade) |
| Caption Styles | Configurable subtitle animations and visual effects |
| Video Backgrounds | Loop background videos from Pexels behind content |
| Thumbnail Generation | Auto-generate thumbnails with title overlay |
| Watermarks | Add logo or text watermarks for branding |
| Auto Repurpose | Split long-form videos into multiple shorts |
| Shorts to Longform | Combine multiple shorts into compilation videos |
| Batch Generation | Generate 10-50 videos in a single batch run |

### AI and Intelligence
| Feature | Description |
|---|---|
| OpenRouter LLM | Free cloud models (Llama, Mixtral, etc.) with 1000 req/day free tier |
| Viral Predictor | Score video ideas before generating to focus on high-potential content |
| Hook Optimizer | Generate multiple opening hooks and pick the most engaging one |
| Script Scorer | Rate script quality and auto-improve if below threshold |
| Trending Topics | Auto-detect viral topics from Google Trends |
| Competitor Analysis | Scrape and analyze competitor channels for content gaps |
| Reddit Scraper | Scrape subreddits for proven content ideas |
| SEO Optimization | Auto-generate optimized tags, titles, and descriptions |
| Hashtag Research | Research and apply trending hashtags per platform |

### Audio and Voice
| Feature | Description |
|---|---|
| Edge-TTS | 300+ voices across 70+ languages (free, no GPU) |
| KittenTTS | Alternative TTS engine |
| Voice Cloner | Select from 40+ Edge-TTS voice styles to match your brand |
| Music Matcher | Automatically match background music mood to content |
| 3 STT Providers | Local Whisper, AssemblyAI, or Groq Whisper for subtitle generation |

### Platform Upload
| Feature | Description |
|---|---|
| YouTube Upload | Official Data API v3 or Selenium-based upload |
| TikTok Upload | Automated upload via Selenium |
| Instagram Reels | Upload videos as Instagram Reels |
| Twitter/X Posting | Auto-generate and post tweets |
| Multi-Platform | Upload one video to all platforms simultaneously |

### Analytics and Testing
| Feature | Description |
|---|---|
| Posting Analytics | Track posting times and content performance |
| Split Testing | A/B test titles and thumbnails across variants |
| A/B Testing Framework | Structured A/B testing with statistical tracking |
| YouTube Analytics | Integrate with YouTube analytics for view/revenue data |
| Monetization Checker | Verify platform monetization eligibility requirements |

### Automation and Scheduling
| Feature | Description |
|---|---|
| Content Calendar | Plan a full week of content with no topic repetition |
| Video Series | Create multi-part connected video series |
| Queue System | Add videos to a processing queue, execute sequentially |
| Timezone Scheduler | Schedule posts for optimal times per platform and region |
| Pipeline State | Resume video generation from point of failure |
| CRON Scheduling | Automated recurring generation and posting |

### Notifications and Outreach
| Feature | Description |
|---|---|
| Webhooks | Discord and Telegram notifications on events |
| Email List Builder | CTA generation and subscriber tracking |
| Cross-Promotion | Generate natural promo content across platforms |

### Other Capabilities
| Feature | Description |
|---|---|
| Stock Footage | Pexels API integration for B-roll and stock video |
| Video Preview | Preview generated video before uploading |
| AI Avatar | AI talking avatar integration (D-ID, SadTalker) |
| Multi-Language | Dub videos into 20+ languages |
| Prompt Loader | Load and customize prompts from template files |
| Web Dashboard | Full Streamlit UI for management, generation, and analytics |

---

## Quick Start

### Prerequisites

- **Python 3.10+** (3.12 recommended)
- **Firefox** (for Selenium-based platform automation)
- **ImageMagick** ([download](https://imagemagick.org/script/download.php)) — required for subtitle rendering

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/AjjouqaMustapha/MoneyPrinterV2.git
cd MoneyPrinterV2

# 2. Copy the config template and fill in your API keys
cp config.example.json config.json

# 3. Create and activate a virtual environment
python -m venv venv

# On Windows (CMD)
venv\Scripts\activate.bat

# On Windows (PowerShell)
venv\Scripts\Activate.ps1

# On macOS / Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Edit config.json with your API keys (see Configuration section)

# 6. Run the application
python src/main.py
```

### macOS Quick Setup

```bash
bash scripts/setup_local.sh      # Auto-configures Ollama, ImageMagick, Firefox profile
python scripts/preflight_local.py # Validates all services are reachable
```

---

## Configuration

All configuration lives in `config.json` at the project root. Copy `config.example.json` to get started.

### Configuration Reference

| Key | Type | Default | Description |
|---|---|---|---|
| `verbose` | bool | `true` | Enable detailed console logging |
| `headless` | bool | `false` | Run Selenium browsers in headless mode |
| `firefox_profile` | string | `""` | Path to pre-authenticated Firefox profile |
| `openrouter_api_key` | string | `""` | OpenRouter API key for LLM text generation |
| `openrouter_model` | string | `"meta-llama/llama-3.2-3b-instruct:free"` | OpenRouter model identifier |
| `ollama_base_url` | string | `"http://127.0.0.1:11434"` | Ollama server URL (if using local LLM) |
| `ollama_model` | string | `""` | Ollama model name (leave empty to pick at startup) |
| `nanobanana2_api_key` | string | `""` | Google Gemini API key for image generation |
| `nanobanana2_model` | string | `"gemini-3.1-flash-image-preview"` | Gemini model for image generation |
| `nanobanana2_aspect_ratio` | string | `"9:16"` | Generated image aspect ratio |
| `nanobanana2_api_base_url` | string | `"https://generativelanguage.googleapis.com/v1beta"` | Gemini API base URL |
| `tts_engine` | string | `"edge_tts"` | TTS engine: `edge_tts` or `kitten_tts` |
| `tts_voice` | string | `"Jasper"` | KittenTTS voice name |
| `edge_tts_voice` | string | `"en-US-ChristopherNeural"` | Edge-TTS voice identifier |
| `video_transition` | string | `"fade"` | Transition effect: `fade`, `zoom`, `slide` |
| `transition_duration` | float | `0.5` | Transition duration in seconds |
| `background_music_enabled` | bool | `true` | Enable background music in videos |
| `threads` | int | `2` | Number of parallel image generation workers |
| `is_for_kids` | bool | `false` | Mark YouTube uploads as made for kids |
| `zip_url` | string | `""` | URL for additional resource downloads |
| `groq_api_key` | string | `""` | Groq API key for cloud Whisper STT |
| `pexels_api_key` | string | `""` | Pexels API key for stock footage and B-roll |
| `timezone` | string | `"UTC"` | Default timezone for scheduling |
| `discord_webhook_url` | string | `""` | Discord webhook URL for notifications |
| `telegram_bot_token` | string | `""` | Telegram bot token for notifications |
| `telegram_chat_id` | string | `""` | Telegram chat ID for notifications |
| `upload_platforms` | array | `["youtube"]` | Platforms to upload to: `youtube`, `tiktok`, `instagram` |
| `stt_provider` | string | `"local_whisper"` | STT provider: `local_whisper`, `third_party_assemblyai`, or `groq` |
| `whisper_model` | string | `"base"` | Local Whisper model size |
| `whisper_device` | string | `"auto"` | Whisper compute device |
| `whisper_compute_type` | string | `"int8"` | Whisper compute type |
| `assembly_ai_api_key` | string | `""` | AssemblyAI API key for cloud STT |
| `font` | string | `"bold_font.ttf"` | Font file for subtitles (from `fonts/` dir) |
| `imagemagick_path` | string | `""` | Path to ImageMagick binary |
| `script_sentence_length` | int | `4` | Number of sentences per video script |
| `twitter_language` | string | `"English"` | Language for Twitter bot content |
| `email.smtp_server` | string | `"smtp.gmail.com"` | SMTP server for outreach emails |
| `email.smtp_port` | int | `587` | SMTP port |
| `email.username` | string | `""` | SMTP username |
| `email.password` | string | `""` | SMTP password |
| `google_maps_scraper` | string | *(URL)* | Google Maps scraper binary URL |
| `google_maps_scraper_niche` | string | `""` | Niche for Google Maps business scraping |
| `scraper_timeout` | int | `300` | Scraper timeout in seconds |
| `outreach_message_subject` | string | `"I have a question..."` | Cold outreach email subject |
| `outreach_message_body_file` | string | `"outreach_message.html"` | Cold outreach email body template file |

---

## Usage

### CLI Mode

```bash
python src/main.py
```

The interactive menu presents the following options:

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

- **Account Management** — manage platform accounts and Firefox profiles
- **Video Generation** — generate videos with a visual interface
- **Task Queue** — view and manage the video generation queue
- **Analytics** — track performance, views, and revenue
- **Content Calendar** — plan and schedule upcoming content
- **Settings** — edit configuration without touching JSON files

### Docker

```bash
# Build and run the CLI
docker-compose up moneyprinter

# Run the web dashboard
docker-compose up dashboard
# Open http://localhost:8501 in your browser
```

---

## Modules Reference

### Core

| Module | Description |
|---|---|
| `src/main.py` | Main entry point and interactive CLI menu |
| `src/config.py` | Configuration management with in-memory caching and validation |
| `src/llm_provider.py` | OpenRouter LLM integration with retry and exponential backoff |
| `src/cron.py` | Scheduled automation runner (invoked as subprocess) |
| `src/prompt_loader.py` | Load prompt templates from `prompts/` directory |
| `src/dashboard.py` | Streamlit web dashboard for visual management |

### Video Generation

| Module | Description |
|---|---|
| `src/classes/YouTube.py` | Full YouTube Shorts generation pipeline: script, images, TTS, compose, upload |
| `src/classes/Tts.py` | Text-to-speech engine supporting Edge-TTS (300+ voices) and KittenTTS |
| `src/dynamic_subtitles.py` | Word-by-word subtitle highlighting with precise timing |
| `src/caption_styles.py` | Caption animation styles: karaoke, bounce, typewriter, fade, highlight |
| `src/video_backgrounds.py` | Background video loops sourced from Pexels API |
| `src/auto_repurpose.py` | Split long-form videos into multiple shorts |
| `src/shorts_to_longform.py` | Combine multiple shorts into a compilation video |
| `src/watermark.py` | Add logo or text watermarks for channel branding |
| `src/thumbnail.py` | Auto-generate thumbnails from video frames with title overlay |
| `src/batch_generator.py` | Batch video generation (10-50 videos per run) |
| `src/video_preview.py` | Preview generated video in system player before uploading |

### AI and Intelligence

| Module | Description |
|---|---|
| `src/viral_predictor.py` | Score video ideas on viral potential before committing to generation |
| `src/hook_optimizer.py` | Generate multiple opening hooks and select the most engaging one |
| `src/script_scorer.py` | Rate script quality via LLM and auto-improve if below threshold |
| `src/trending.py` | Detect trending topics from Google Trends |
| `src/competitor_analysis.py` | Scrape and analyze competitor YouTube channels |
| `src/reddit_scraper.py` | Scrape Reddit subreddits for proven content ideas |
| `src/seo.py` | Generate SEO-optimized tags, titles, and descriptions |
| `src/hashtag_research.py` | Research and suggest trending hashtags per platform |

### Audio

| Module | Description |
|---|---|
| `src/voice_cloner.py` | Edge-TTS voice style selection with 40+ voice options |
| `src/music_matcher.py` | Auto-match background music mood to video content |

### Platform Upload

| Module | Description |
|---|---|
| `src/classes/Twitter.py` | Twitter/X posting via Selenium automation |
| `src/tiktok_uploader.py` | TikTok video upload via Selenium |
| `src/instagram_uploader.py` | Instagram Reels upload via Selenium |
| `src/youtube_api.py` | YouTube Data API v3 upload (official API, no Selenium) |
| `src/multi_platform.py` | Multi-platform simultaneous posting orchestrator |

### Analytics and Testing

| Module | Description |
|---|---|
| `src/posting_analytics.py` | Track posting times and content performance metrics |
| `src/split_testing.py` | A/B test titles and thumbnails with variant tracking |
| `src/ab_testing.py` | A/B testing framework with statistical analysis |
| `src/analytics.py` | YouTube analytics integration for views and revenue |
| `src/monetization_checker.py` | Check platform monetization eligibility requirements |

### Automation and Scheduling

| Module | Description |
|---|---|
| `src/content_calendar.py` | Plan a week of content with no topic repetition |
| `src/video_series.py` | Create multi-part connected video series |
| `src/queue_system.py` | Video generation queue with sequential processing |
| `src/timezone_scheduler.py` | Schedule posts for optimal times by timezone and platform |
| `src/pipeline_state.py` | Save pipeline state and resume from point of failure |

### Notifications

| Module | Description |
|---|---|
| `src/webhooks.py` | Discord and Telegram webhook notifications |
| `src/email_list_builder.py` | CTA generation and subscriber tracking |
| `src/cross_promotion.py` | Cross-platform promotion content generation |

### Other

| Module | Description |
|---|---|
| `src/stock_footage.py` | Pexels API integration for stock footage and B-roll |
| `src/ai_avatar.py` | AI talking avatar generation (D-ID, SadTalker) |
| `src/multi_language.py` | Multi-language dubbing support (20+ languages) |
| `src/classes/AFM.py` | Affiliate marketing: Amazon scraping + LLM pitch generation |
| `src/classes/Outreach.py` | Cold outreach: Google Maps scraping + email automation |
| `src/cache.py` | JSON file persistence in `.mp/` directory |
| `src/constants.py` | Menu strings, Selenium selectors, platform constants |
| `src/utils.py` | Shared utility functions |
| `src/art.py` | ASCII art and CLI visual elements |
| `src/status.py` | Status display utilities |
| `src/auto_reply.py` | Automated reply generation |

---

## API Keys

### Required

| Service | Config Key | Where to Get | Cost |
|---|---|---|---|
| **OpenRouter** | `openrouter_api_key` | [openrouter.ai/keys](https://openrouter.ai/keys) | Free (1000 req/day) |
| **Google Gemini** | `nanobanana2_api_key` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Free tier available |
| **ImageMagick** | `imagemagick_path` | [imagemagick.org/download](https://imagemagick.org/script/download.php) | Free (local install) |

### Optional

| Service | Config Key | Where to Get | Cost | Used For |
|---|---|---|---|---|
| **Groq** | `groq_api_key` | [console.groq.com/keys](https://console.groq.com/keys) | Free tier | Cloud Whisper STT for subtitles |
| **Pexels** | `pexels_api_key` | [pexels.com/api](https://www.pexels.com/api/) | Free | Stock footage, B-roll, backgrounds |
| **AssemblyAI** | `assembly_ai_api_key` | [assemblyai.com](https://www.assemblyai.com/) | Free tier | Alternative cloud STT |
| **Discord** | `discord_webhook_url` | Discord Server Settings > Integrations | Free | Webhook notifications |
| **Telegram** | `telegram_bot_token` | [@BotFather](https://t.me/BotFather) | Free | Webhook notifications |
| **YouTube Data API** | OAuth credentials | [console.cloud.google.com](https://console.cloud.google.com/) | Free | Official YouTube upload |

> **Tip:** You can start with just OpenRouter + Gemini keys and add the rest as needed.

---

## Platform Support

| Platform | Upload Method | Module | Features |
|---|---|---|---|
| **YouTube** | Selenium or Data API v3 | `YouTube.py`, `youtube_api.py` | Shorts, thumbnails, SEO tags, analytics |
| **TikTok** | Selenium automation | `tiktok_uploader.py` | Video upload, hashtags |
| **Instagram** | Selenium automation | `instagram_uploader.py` | Reels upload |
| **Twitter/X** | Selenium automation | `Twitter.py` | Tweet generation, media posting |

All Selenium-based uploaders require a **pre-authenticated Firefox profile** — the app does not handle login flows. Set the `firefox_profile` path in your config to a profile that is already logged in to the target platforms.

---

## Advanced Features

### Batch Generation

Generate multiple videos in a single run using `src/batch_generator.py`. Configure batch sizes of 10-50 videos with automatic topic variation and scheduling.

### Video Series

Create multi-part connected video series with `src/video_series.py`. Each part references previous episodes and maintains narrative continuity.

### Split Testing

Run A/B tests on titles and thumbnails using `src/split_testing.py` and `src/ab_testing.py`. Track which variants perform best and apply learnings to future content.

### Competitor Analysis

Scrape and analyze competitor channels with `src/competitor_analysis.py`. Identify content gaps, successful formats, and trending topics in your niche.

### Viral Prediction

Score video ideas before generating them with `src/viral_predictor.py`. Prioritize high-potential content and skip ideas unlikely to gain traction.

### Content Calendar

Plan an entire week of content with `src/content_calendar.py`. The system ensures no topic repetition and maintains variety across your posting schedule.

### Auto Repurpose

Take existing long-form content and automatically split it into shorts with `src/auto_repurpose.py`. Conversely, combine shorts into compilations with `src/shorts_to_longform.py`.

### Multi-Language Dubbing

Dub videos into 20+ languages using `src/multi_language.py`. Expand your reach across international audiences without manual translation.

### AI Avatar

Generate AI talking-head avatars using `src/ai_avatar.py` with D-ID or SadTalker integration. Add a human presenter to faceless content.

### Timezone Scheduling

Schedule posts for optimal engagement times per platform and region with `src/timezone_scheduler.py`.

### Pipeline Recovery

If video generation fails mid-process, `src/pipeline_state.py` saves progress so you can resume from the exact point of failure without re-generating completed steps.

---

## Project Structure

```
MoneyPrinterV2/
├── src/
│   ├── main.py                    # CLI entry point
│   ├── dashboard.py               # Streamlit web dashboard
│   ├── config.py                  # Cached config with validation
│   ├── llm_provider.py            # OpenRouter API with retry
│   ├── cron.py                    # Scheduled automation runner
│   ├── prompt_loader.py           # Prompt template loader
│   ├── classes/
│   │   ├── YouTube.py             # Video generation + upload pipeline
│   │   ├── Twitter.py             # Tweet automation
│   │   ├── Tts.py                 # Edge-TTS + KittenTTS
│   │   ├── AFM.py                 # Affiliate marketing
│   │   └── Outreach.py            # Cold email outreach
│   ├── tiktok_uploader.py         # TikTok Selenium upload
│   ├── instagram_uploader.py      # Instagram Reels upload
│   ├── youtube_api.py             # YouTube Data API v3
│   ├── multi_platform.py          # Multi-platform orchestrator
│   ├── batch_generator.py         # Batch video generation
│   ├── trending.py                # Google Trends detection
│   ├── viral_predictor.py         # Viral score prediction
│   ├── hook_optimizer.py          # Opening hook generation
│   ├── script_scorer.py           # Script quality scoring
│   ├── competitor_analysis.py     # Competitor channel analysis
│   ├── reddit_scraper.py          # Reddit content scraping
│   ├── seo.py                     # SEO optimization
│   ├── hashtag_research.py        # Trending hashtag research
│   ├── content_calendar.py        # Weekly content planning
│   ├── video_series.py            # Multi-part video series
│   ├── ab_testing.py              # A/B testing framework
│   ├── split_testing.py           # Title/thumbnail split testing
│   ├── analytics.py               # YouTube analytics + revenue
│   ├── posting_analytics.py       # Posting performance tracking
│   ├── monetization_checker.py    # Monetization eligibility check
│   ├── queue_system.py            # Video generation queue
│   ├── pipeline_state.py          # Resume from failure
│   ├── timezone_scheduler.py      # Timezone-aware scheduling
│   ├── dynamic_subtitles.py       # Word-by-word subtitles
│   ├── caption_styles.py          # Subtitle animation styles
│   ├── video_backgrounds.py       # Pexels background loops
│   ├── thumbnail.py               # Thumbnail generation
│   ├── watermark.py               # Logo/text watermarks
│   ├── auto_repurpose.py          # Long video to shorts
│   ├── shorts_to_longform.py      # Shorts to compilation
│   ├── stock_footage.py           # Pexels stock footage
│   ├── video_preview.py           # Preview before upload
│   ├── voice_cloner.py            # Voice style selection
│   ├── music_matcher.py           # Background music matching
│   ├── multi_language.py          # Multi-language dubbing
│   ├── ai_avatar.py               # AI talking avatar
│   ├── webhooks.py                # Discord + Telegram alerts
│   ├── email_list_builder.py      # CTA + subscriber tracking
│   ├── cross_promotion.py         # Cross-platform promotion
│   ├── cache.py                   # JSON file persistence
│   ├── constants.py               # Selectors and constants
│   ├── utils.py                   # Shared utilities
│   ├── art.py                     # ASCII art
│   └── status.py                  # Status display
├── prompts/                       # 10 editable prompt templates
│   ├── topic.txt                  # Topic generation prompt
│   ├── script.txt                 # Script writing prompt
│   ├── title.txt                  # Title generation prompt
│   ├── description.txt            # Description generation prompt
│   ├── hook.txt                   # Hook generation prompt
│   ├── image_prompts.txt          # Image prompt generation
│   ├── seo_tags.txt               # SEO tag generation
│   ├── script_score.txt           # Script scoring criteria
│   ├── combined_video.txt         # Combined single-call prompt
│   └── tweet.txt                  # Tweet generation prompt
├── templates/                     # Pre-built niche configurations
│   ├── scary_stories.json         # Horror/scary stories niche
│   ├── motivation.json            # Motivational content niche
│   ├── cooking.json               # Cooking/recipe niche
│   ├── fun_facts.json             # Fun facts/trivia niche
│   └── tech_tips.json             # Tech tips niche
├── fonts/                         # Subtitle fonts
├── Songs/                         # Background music files
├── assets/                        # Static assets
├── scripts/                       # Setup and utility scripts
├── docs/                          # Additional documentation
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # CLI + Dashboard services
├── config.example.json            # Config template
├── requirements.txt               # Python dependencies
├── CHECKLIST.md                   # Feature tracking checklist
├── CONTRIBUTING.md                # Contribution guidelines
├── CODE_OF_CONDUCT.md             # Code of conduct
└── LICENSE                        # AGPL-3.0 license
```

---

## Requirements

### Minimum System Requirements

| Component | Requirement |
|---|---|
| **CPU** | Any modern CPU (no GPU required) |
| **RAM** | 4 GB minimum, 8 GB recommended |
| **Disk** | 2 GB free space (plus space for generated videos) |
| **OS** | Windows 10/11, macOS, or Linux |
| **Python** | 3.10 or higher (3.12 recommended) |
| **Internet** | Required for API calls and uploads |

### Software Dependencies

| Software | Required | Purpose |
|---|---|---|
| **Python 3.10+** | Yes | Runtime |
| **ImageMagick** | Yes | Subtitle rendering via MoviePy |
| **Firefox** | Yes (for uploads) | Selenium browser automation |
| **Go** | Only for Outreach | Google Maps scraper binary |
| **Docker** | Optional | Containerized deployment |

> **No GPU required.** All heavy computation (LLM, image generation, STT) runs on cloud APIs. Local processing is limited to lightweight video composition with MoviePy.

---

## Video Pipeline

Each video goes through this automated pipeline:

```
1. Topic Selection
   ├── Manual input
   ├── Google Trends auto-detection
   ├── Reddit scraping
   └── Content calendar

2. Script Generation (1 LLM call via OpenRouter)
   └── Topic + script + title + description + image prompts

3. Quality Gates
   ├── Viral prediction scoring
   ├── Hook optimization
   └── Script quality scoring (auto-improve if below threshold)

4. Image Generation (parallel workers)
   └── Gemini API creates 9:16 images

5. Text-to-Speech
   └── Edge-TTS or KittenTTS converts script to audio

6. Subtitle Generation
   ├── Local Whisper
   ├── Groq Whisper API
   └── AssemblyAI

7. Video Composition (MoviePy)
   ├── Images + audio + subtitles
   ├── Transitions (fade, zoom, slide)
   ├── Background music
   ├── Watermark
   └── Thumbnail generation

8. Upload
   ├── YouTube (API or Selenium)
   ├── TikTok (Selenium)
   ├── Instagram Reels (Selenium)
   └── Twitter/X (Selenium)

9. Post-Upload
   ├── Webhook notifications
   ├── Analytics tracking
   └── Cross-promotion
```

**Output:** ~20-40 second vertical video (configurable via `script_sentence_length`).

---

## Templates and Prompts

### Niche Templates

Pre-built configurations in `templates/` let you start generating content immediately for popular niches:

| Template | File | Description |
|---|---|---|
| Scary Stories | `scary_stories.json` | Horror narration with dark imagery |
| Motivation | `motivation.json` | Inspirational quotes and stories |
| Cooking | `cooking.json` | Quick recipe and cooking tip videos |
| Fun Facts | `fun_facts.json` | Interesting trivia and facts |
| Tech Tips | `tech_tips.json` | Technology tips and tutorials |

### Prompt Templates

All LLM prompts are editable text files in `prompts/`. Customize them to match your content style:

| Prompt | File | Purpose |
|---|---|---|
| Topic | `topic.txt` | Generate video topic ideas |
| Script | `script.txt` | Write the video narration script |
| Title | `title.txt` | Generate clickable video titles |
| Description | `description.txt` | Write video descriptions |
| Hook | `hook.txt` | Generate attention-grabbing opening hooks |
| Image Prompts | `image_prompts.txt` | Generate prompts for image creation |
| SEO Tags | `seo_tags.txt` | Generate SEO-optimized tags |
| Script Score | `script_score.txt` | Define script quality scoring criteria |
| Combined | `combined_video.txt` | Single-call prompt for all video metadata |
| Tweet | `tweet.txt` | Generate tweet content |

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Open an issue before starting work on a feature or fix
2. One feature or fix per pull request
3. PRs go against the `main` branch
4. Use the `WIP` label for in-progress pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

---

## License

MoneyPrinterV2 is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](LICENSE) for the full text.

---

## Credits

- Original project: [FujiwaraChoki/MoneyPrinterV2](https://github.com/FujiwaraChoki/MoneyPrinterV2)
- [Edge-TTS](https://github.com/rany2/edge-tts) — Microsoft Edge text-to-speech
- [OpenRouter](https://openrouter.ai) — Unified LLM API
- [KittenTTS](https://github.com/KittenML/KittenTTS) — Alternative TTS engine
- [Pexels](https://www.pexels.com) — Stock footage and images

---

## Disclaimer

This project is for **educational purposes only**. The author is not responsible for any misuse of the information provided. All information is published in good faith and for general informational purposes only. Any action you take based on this project is strictly at your own risk. The author will not be liable for any losses or damages in connection with the use of this project.
