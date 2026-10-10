# Machine Self-Sufficiency Audit (2026-06-16)

## Self-sufficient on this box? -> With caveats

## Issues found
- **Deps missing:** Python app (`app.py`, `requirements.txt`) with no `.venv/`.
  Needs `python -m venv .venv && pip install -r requirements.txt`. Not installed
  this pass per audit scope.
- No Mac-only paths or mechanisms. Portable code.
- Secrets are env-driven via `python-dotenv`: `app.py` reads `OPENAI_API_KEY` and
  `SERPER_API_KEY` from env. `.env.example` is a placeholder template (no real
  values). No `.env` present on this box yet.

## Fixed this pass
- None needed.

## Outstanding (needs Brad)
- Create venv + install deps.
- Create `.env` from `.env.example` with real `OPENAI_API_KEY` and `SERPER_API_KEY`
  (these are NOT in 1Password `op://` form here — they're plain placeholders, so
  Brad must supply/route them).

## Resilience (good)
- Git repo, remote `github.com/violentlydelightful/research-agent.git`, clean tree,
  all pushed. `.gitignore` ignores `.env` + venvs. No committed secrets.
