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

## High Impact Features (Completed)

- [x] Auto-reply bot — reply to YouTube comments to boost engagement (src/auto_reply.py)
- [x] Competitor analysis — scrape competitors' top videos, reverse-engineer patterns (src/competitor_analysis.py)
- [x] Viral score predictor — score video ideas before generating, save API calls (src/viral_predictor.py)
- [x] Auto-repurpose — chop long videos into multiple shorts automatically (src/auto_repurpose.py)
- [x] Voiceover cloning — voice style matching with 40+ Edge-TTS voices (src/voice_cloner.py)
- [x] Background video loops — ambient videos instead of static images (src/video_backgrounds.py)
- [x] Music matching — auto-select background music mood based on content (src/music_matcher.py)
- [x] Batch generation — generate 10-50 videos in one command (src/batch_generator.py)
- [x] Email list builder — CTA in descriptions, track subscriber growth (src/email_list_builder.py)
- [x] Monetization checker — check platform requirements with progress tracking (src/monetization_checker.py)

## Medium Impact Features (Completed)

- [x] AI face/avatar — D-ID + SadTalker integration with overlay support (src/ai_avatar.py)
- [x] Split testing uploads — A/B test titles/thumbnails, track winners (src/split_testing.py)
- [x] Posting analytics — track best posting times based on YOUR data (src/posting_analytics.py)
- [x] Auto-hashtag research — LLM + niche database for optimal hashtags (src/hashtag_research.py)
- [x] Video series — generate connected multi-part series with cliffhangers (src/video_series.py)
- [x] Watermark/branding — logo + text overlay on every video (src/watermark.py)
- [x] Caption styles — karaoke, bounce, typewriter, fade, highlight box (src/caption_styles.py)
- [x] Multi-language dub — translate + dub in 20 languages via Edge-TTS (src/multi_language.py)
- [x] Shorts to longform — compile shorts into 10+ min videos with intro/outro (src/shorts_to_longform.py)
- [x] Reddit scraper — scrape 14 niche subreddits for content ideas (src/reddit_scraper.py)

## Nice to Have Features (Pending)

- [ ] Telegram bot control — control everything via Telegram commands
- [ ] Mobile app — trigger generation from phone
- [ ] Proxy support — rotate proxies for Selenium
- [ ] Account warmup — gradually increase posting frequency
- [ ] Plagiarism check — ensure scripts aren't too similar to existing content
- [ ] Auto-pin comment — pin promotional comment on uploaded video
- [ ] Scheduler calendar UI — visual drag-and-drop calendar in dashboard
- [ ] Revenue dashboard — pull real YouTube/TikTok analytics via API
- [ ] Multi-user support — multiple users with separate configs
- [ ] Plugin system — let others write plugins for new platforms

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
| auto_reply.py | YouTube comment auto-reply bot |
| competitor_analysis.py | Competitor video pattern analysis |
| viral_predictor.py | Viral score prediction for video ideas |
| auto_repurpose.py | Long video to shorts chopper |
| voice_cloner.py | Voice style matching with Edge-TTS |
| video_backgrounds.py | Ambient background video loops |
| music_matcher.py | Content-based background music selection |
| batch_generator.py | Bulk video generation (10-50 at once) |
| email_list_builder.py | Email CTA and subscriber tracking |
| monetization_checker.py | Platform monetization requirement checker |
| watermark.py | Logo + text watermark branding |
| reddit_scraper.py | Reddit content scraping (14 niches) |
| multi_language.py | Multi-language dubbing (20 languages) |
| video_series.py | Multi-part video series generator |
| hashtag_research.py | Auto-hashtag research + trending |
| caption_styles.py | 5 caption animation styles |
| shorts_to_longform.py | Shorts compilation into longform |
| split_testing.py | A/B split testing framework |
| posting_analytics.py | Posting time + performance tracking |
| ai_avatar.py | AI avatar (D-ID + SadTalker) |

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
