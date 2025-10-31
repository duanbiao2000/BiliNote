## Testing Guide

### Backend (pytest)
Run:
```bash
pytest backend/tests -q
```

Scope:
- Unit: `app/services/note.py` phases (download/transcribe/summarize)
- Router: `/generate_note`, `/task_status/{id}`
- DAO: use temp SQLite or mock if needed

Principles:
- No network/LLM/ffmpeg: mock downloader/transcriber/GPT
- Use temp dirs via fixtures; assert status files and outputs
- Cover failure paths (invalid platform, timeouts, partial results)

### Frontend (Vitest + RTL)
Planned tasks:
- hooks: `useTaskPolling` state transitions
- services: error branches, payload correctness
- components: `NoteForm` validation, submit/retry flows


