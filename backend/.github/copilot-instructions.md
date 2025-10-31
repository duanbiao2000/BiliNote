# Copilot / AI agent quick guidance for BiliNote backend

This file contains concise, actionable notes to help an AI coding assistant be productive in the BiliNote backend.

- Project entrypoint: `main.py` (FastAPI + uvicorn). The application factory is `app.create_app` in `app/__init__.py` and uses an async lifespan in `main.py` to init DB, seed providers and transcribers.

- Key directories:

  - `app/routers/` — REST API endpoints (e.g. `note.py` for the main note-generation flow).
  - `app/services/` — core business logic. `app/services/note.py` contains the NoteGenerator orchestration (download → transcribe → GPT summarize → post-process → save).
  - `app/downloaders/` — platform-specific downloaders (youtube, bilibili, douyin, local). They use `yt-dlp` and provide `download()` and `download_video()` methods returning `AudioDownloadResult`.
  - `app/transcriber/` — transcriber provider/implementations (fast-whisper, bcut, groq, etc.). Use `app.transcriber.transcriber_provider.get_transcriber` to obtain a shared instance.
  - `app/db/` — database models and simple seed functions (SQLite or configured DB via SQLAlchemy engine in `app/db/engine.py`). `init_db()` creates tables.
  - `ffmpeg_helper.py` — code that validates ffmpeg presence; several flows depend on ffmpeg being available.

- Important data flows and patterns:

  - Note generation is triggered via `POST /api/generate_note` (see `app/routers/note.py`) which enqueues a background task calling `NoteGenerator.generate`.
  - `NoteGenerator.generate` orchestrates steps and writes status files to `NOTE_OUTPUT_DIR` (default `note_results/`) using atomic replace (writes to `.tmp` then replace).
  - Downloaders return a small dataclass-like `AudioDownloadResult` containing `file_path`, `title`, `duration`, `video_id`, `raw_info` and `video_path` (if video downloaded).
  - Status and result files are stored as JSON under `note_results/` and named `{task_id}.status.json` and `{task_id}.json`.

- Conventions & traps to watch for (codebase-specific):

  - Many functions use environment variables; `.env` is used in packaging. See `main.py`, `ffmpeg_helper.py`, and `app/services/note.py` for env usage (`TRANSCRIBER_TYPE`, `NOTE_OUTPUT_DIR`, `BACKEND_PORT`...).
  - Downloaders use `yt-dlp` with hardcoded format strings (e.g. prefer `m4a` or `mp4`). Be careful when changing formats — upstream videos may lack the requested ext.
  - When modifying file-writing logic, follow the project's atomic write pattern (`.tmp` then `replace`) used in `_update_status` in `NoteGenerator`.
  - Database seeding reads `app/db/builtin_providers.json`. When packaging with PyInstaller, code accounts for `sys._MEIPASS` — keep that path logic if you change seeding.
  - Transcriber selection uses a small registry pattern in `app/transcriber/transcriber_provider.py` — new transcribers should be registered there. MLX whisper is only enabled on macOS.

- Build / run notes (how developers typically run backend):

  - Development: run `python main.py` (or `uvicorn app:create_app --reload` with appropriate lifespan wiring). `main.py` reads `.env` and auto-creates `static/` and `uploads/` directories.
  - Packaging: there are `build.sh` and `build.bat` scripts that use `pyinstaller` to produce a Tauri bundle. These scripts copy `.env.example` to `backend/.env` before packaging and expect `app/db/builtin_providers.json` to be included via `--add-data`.
  - Dependencies referenced in `requirements.txt`. Note `yt-dlp==2025.3.31` and multiple speech/ML libs (faster-whisper, ctranslate2, onnxruntime). Some native binaries (ffmpeg) are required at runtime.

- Good example code references to copy style/patterns from:

  - API wiring / app factory: `app/__init__.py` and `main.py` lifecycles.
  - Orchestration pattern: `app/services/note.py` (status updates, caching, stepwise error handling, and atomic file writes).
  - Provider seeding & packaging path handling: `app/db/provider_dao.py` (uses `sys._MEIPASS` for PyInstaller).

- Suggested direct instructions for code-changes by an AI assistant:
  npm install -g @google/gemini-cli

  - When editing downloaders, prefer _adding_ permissive fallback formats and catching yt-dlp errors. See `app/downloaders/youtube_downloader.py` for an example of where format fallbacks are necessary.
  - Preserve atomic file write pattern when modifying status/result writing (`.tmp` then `replace`).
  - When adding new transcribers, register them in `app/transcriber/transcriber_provider.py` and handle platform-specific availability.
  - Avoid assuming `output_dir` is always present — many flows read `DATA_DIR` or accept `None`.

- Quick checklist for PR reviewers:
  - Does the change preserve file write atomicity used for `{task_id}.status.json`?
  - If adding or changing a downloader, does it handle missing formats and provide a fallback? Are yt-dlp errors logged? Is `yt-dlp` version pinned/compatible? (See `requirements.txt`.)
  - If touching packaging or seeding code, ensure `sys._MEIPASS` logic is preserved for PyInstaller builds.
  - If adding dependencies that require native binaries (ffmpeg, onnxruntime, ctranslate2), include notes in README or packaging scripts.

If any of the above assumptions are incorrect or you'd like the assistant to also create a short `README.md` for `backend/` with run commands and env examples, say so and I will generate it.
