# BiliNote Project Overview

## Purpose
BiliNote is a FastAPI-based backend application designed to generate comprehensive notes from video content, particularly focusing on platforms like Bilibili. The system processes videos through several stages:
1. Video/audio download from various platforms
2. Audio transcription
3. Content summarization and note generation
4. Screenshot integration and markdown formatting

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLAlchemy
- **Video Processing**: yt-dlp, ffmpeg
- **Transcription**: Multiple providers (fast-whisper, bcut, groq)
- **Packaging**: PyInstaller for Tauri integration

## Key Components
1. **NoteGenerator**: Core service class handling the entire note generation pipeline
2. **Downloaders**: Platform-specific video/audio downloaders
3. **Transcribers**: Multiple transcription service implementations
4. **GPT Integration**: For summarization and content processing

## Directory Structure
- `/app`: Main application code
  - `/services`: Core business logic
  - `/routers`: API endpoints
  - `/downloaders`: Platform-specific downloaders
  - `/transcriber`: Transcription services
  - `/db`: Database models and operations
- `/note_results`: Output directory for generated notes
- `/static`: Static files (covers, screenshots)
- `/uploads`: Temporary upload directory