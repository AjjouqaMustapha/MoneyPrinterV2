# MoneyPrinterV2 - Optimization & Feature Checklist

## Optimizations (Completed)

- [x] Cache config in memory — was reading config.json 30+ times per video, now reads once
- [x] OpenRouter integration — replaced local Ollama with OpenRouter API (no GPU needed)
- [x] Combine LLM calls — 5 API calls to 1 single structured JSON call (saves API budget)
- [x] Retry with exponential backoff — 3 retries, respects rate limits (429), handles server errors
- [x] Parallel image generation — ThreadPoolExecutor (3 workers) instead of sequential loop
- [x] Edge-TTS integration — 300+ voices, 70+ languages, replaces KittenTTS (still available as fallback)
- [x] Video transitions — fade, zoom, slide effects (configurable in config.json)
- [x] TTS instance reuse — created once at startup, not recreated every video
- [x] Config validation on startup — checks API keys, paths, shows clear warnings
- [x] Background music optional — no crash when no songs configured
- [x] Better error handling — removed bare except, errors now logged properly
- [x] Updated config.example.json — all new fields documented
- [x] Updated requirements.txt — added edge-tts, removed ollama dependency
- [x] Updated cron.py — removed Ollama model argument dependency

## Content Quality Features (Completed)

- [x] Dynamic subtitles — word-by-word highlighting (src/dynamic_subtitles.py)
- [x] B-roll / stock footage — Pexels API for video clips and images (src/stock_footage.py)
- [x] Thumbnail generation — auto-generate thumbnails from image + title overlay (src/thumbnail.py)
- [x] Hook optimization — generate multiple opening hooks, pick most engaging (src/hook_optimizer.py)
- [x] Prompt templates — prompts moved to prompts/ directory for easy tweaking

## Platform Features (Completed)

- [x] TikTok upload — Selenium-based uploader (src/tiktok_uploader.py)
- [x] Instagram Reels upload — Selenium-based uploader (src/instagram_uploader.py)
- [x] Multi-platform posting — one video uploads to YouTube + TikTok + Instagram (src/multi_platform.py)
- [x] YouTube API upload — official Data API v3 alternative to Selenium (src/youtube_api.py)
- [x] Schedule by timezone — timezone-aware optimal posting times (src/timezone_scheduler.py)

## AI / Intelligence Features (Completed)

- [x] Trending topic detection — Google Trends RSS feed scraping (src/trending.py)
- [x] Script quality scoring — LLM rates scripts, auto-improves if below threshold (src/script_scorer.py)
- [x] A/B title testing — generate multiple title variants with different strategies (src/ab_testing.py)
- [x] Analytics tracking — track videos, views, likes, revenue by niche/platform (src/analytics.py)
- [x] Content calendar — plan weekly content, no topic repetition (src/content_calendar.py)
- [x] SEO optimization — auto-generate optimized tags, title, description (src/seo.py)

## Technical / UX Features (Completed)

- [x] Web dashboard — Streamlit UI with account management, queue, analytics, settings (src/dashboard.py)
- [x] Queue system — add tasks to queue, process sequentially, track status (src/queue_system.py)
- [x] Webhook notifications — Discord and Telegram alerts (src/webhooks.py)
- [x] Video preview — open video in system media player before upload (src/video_preview.py)
- [x] Resume from failure — save pipeline state, skip completed stages (src/pipeline_state.py)
- [x] Docker support — Dockerfile + docker-compose.yml for one-command setup
- [x] Groq Whisper API — cloud-based subtitles as alternative to local Whisper

## Monetization Features (Completed)

- [x] Faceless channel templates — pre-built configs for 5 niches (templates/)
- [x] Cross-promotion — generate natural promo comments and tweets (src/cross_promotion.py)
- [x] Revenue tracking — CPM-based revenue estimation in analytics (src/analytics.py)

## File Map

### New Directories
- `prompts/` — 10 prompt template files (.txt)
- `templates/` — 5 faceless channel template configs (.json)

### New Source Files (src/)
| File | Feature |
|------|---------|
| prompt_loader.py | Load and fill prompt templates |
| content_calendar.py | Weekly content planning |
| seo.py | SEO metadata optimization |
| trending.py | Google Trends topic detection |
| hook_optimizer.py | Opening hook generation |
| script_scorer.py | Script quality scoring |
| ab_testing.py | A/B title testing |
| analytics.py | Video analytics + revenue tracking |
| cross_promotion.py | Promo comment/tweet generation |
| queue_system.py | Task queue with status tracking |
| pipeline_state.py | Resume from failure |
| webhooks.py | Discord + Telegram notifications |
| video_preview.py | System media player preview |
| timezone_scheduler.py | Timezone-aware scheduling |
| thumbnail.py | Thumbnail generation |
| stock_footage.py | Pexels B-roll/stock images |
| dynamic_subtitles.py | Word-by-word subtitle clips |
| youtube_api.py | YouTube Data API v3 upload |
| tiktok_uploader.py | TikTok Selenium upload |
| instagram_uploader.py | Instagram Reels Selenium upload |
| multi_platform.py | Multi-platform upload orchestrator |
| dashboard.py | Streamlit web dashboard |

### Modified Files
| File | Changes |
|------|---------|
| config.py | Cached config, 9 new getters, validation |
| llm_provider.py | OpenRouter API, retry, generate_structured |
| classes/YouTube.py | Combined LLM, parallel images, transitions, Groq Whisper |
| classes/Tts.py | Edge-TTS + KittenTTS with lazy loading |
| main.py | Config validation, TTS reuse, no Ollama |
| cron.py | Removed Ollama dependency |
| config.example.json | All new config fields |
| requirements.txt | edge-tts, streamlit, google-api-python-client |

### Docker Files
| File | Purpose |
|------|---------|
| Dockerfile | Python 3.12 + Firefox + ImageMagick |
| docker-compose.yml | CLI + Dashboard services |
| .dockerignore | Excludes git, cache, media files |
