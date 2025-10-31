## Code Style Guide

### Python (Backend)
- Naming: functions `verb_noun`, variables descriptive, no 1–2 char names
- Types: annotate public APIs; avoid `Any` unless needed
- Control flow: prefer guard clauses; avoid deep nesting and broad try/except
- Errors: never swallow; raise with context; use domain errors where applicable
- Logging: use `app.utils.logger.get_logger`; include request/task id automatically
- Formatting: Black-ish (multi-line, no trailing spaces); wrap long lines
- Comments: only for non-obvious rationale, invariants, perf/security notes

### TypeScript (Frontend)
- Components: small, focused; lift state up only when necessary
- Types: strong typing for props/services/stores; avoid `any` in public types
- API services: centralize under `src/services`; do not scatter fetch calls
- State: `zustand` stores in `src/store`; no hidden globals
- UI: graceful error/empty/loading states; no blocking toasts
- Formatting: ESLint + Prettier; consistent imports and ordering

### Tests
- Backend: pytest with mocks for network/LLM/ffmpeg; cover happy + 1–2 failures
- Frontend: Vitest + RTL for hooks/components; avoid snapshot-only tests


