# Environment Configuration

This folder contains all environment-related configuration and tooling
for the Customer Analytics Query Agent POC.

## Files

| File | Purpose |
|---|---|
| `config.py` | Central configuration module — loads `.env`, exports typed settings |
| `verify.py` | Environment health check — validates all components |

## Setup Flow

1. Run `setup.bat` from the repository root for automated setup
2. Or manually: install Python → Ollama → create `.venv` → `pip install -r requirements.txt`
3. Run `python environment/verify.py` to confirm everything works

## Environment Variables

See `.env.example` in the repository root for all available settings.
