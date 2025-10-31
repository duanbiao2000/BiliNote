## Contributing to BiliNote

Thank you for your interest! This guide keeps contributions consistent and efficient.

### Branch & PR
- Create feature branches from `main`: `feat/<area>-<short-title>` or `fix/...`
- Keep PRs small and focused; include tests for bug fixes and new features
- PR title: imperative mood, concise; link issues if any

### Commit Style
- Conventional commits (recommended): `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`
- Keep subject ≤ 72 chars, body explains motivation and approach

### Code Review Checklist
- Readability: clear naming, small functions, early returns
- Safety: errors handled with meaningful messages; no silent except
- Logs: key phases log with request/task id
- Tests: cover main path + 1-2 failure paths; mocks for network/AI
- Frontend: no blocking UI; graceful error states

### How to Run Locally
- Backend: `pip install -r backend/requirements.txt` then `python backend/main.py`
- Frontend: `pnpm -C BillNote_frontend install && pnpm -C BillNote_frontend dev`
- FFmpeg required; see README

### Tests
- Backend: `pytest backend/tests -q`
- Frontend (planned): `pnpm -C BillNote_frontend test`

### Style & Lint
- Python: prefer Black/Ruff style; log via `app.utils.logger`
- TypeScript: ESLint + Prettier; avoid `any` in exported APIs

### Educational Comments
- Add brief comments only for non-obvious intent, invariants, or caveats
- Avoid restating the code; keep comments concise


