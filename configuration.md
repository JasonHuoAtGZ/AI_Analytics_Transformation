# Environment Configuration Plan

> Last updated: 2026-06-26
> Status: **ALL PHASES COMPLETE** ✅

## Overview

Four-phase setup for the Customer Analytics Query Agent POC on a Windows 11
laptop. Stack: Python 3.12 + Ollama (Llama 3.1 8B) + DuckDB + Streamlit.

---

## Phase 1 — Python ✅

**Actual outcome**: Python 3.12.10 copied into workspace.

- **Source**: `C:\Users\Jason Huo\AppData\Local\Programs\Python\Python312`
- **Workspace copy**: `.python312/` (143 MB, gitignored)
- **Venv**: `.venv/` created from `.python312/python.exe`
- **Python version**: 3.12.10

**Why not 3.14**: Python 3.14.6 exists on the machine but the sandbox blocks
reading from `pythoncore-3.14-64`. Python 3.12 is more stable and all packages
have wheels for it.

**What we learned**: `venv` with default settings creates redirects to the base
Python, which the sandbox blocks. Solution: copy full Python into workspace
first, then create venv from the in-workspace copy.

---

## Phase 2 — Ollama + Model ✅

- **Ollama service**: Already running at `http://localhost:11434`
- **CLI path**: `%LOCALAPPDATA%\Programs\Ollama\ollama.exe`
- **Model**: llama3.1:8b (5.2 GB, Q4_K_M quantization)
- **Inference**: ~7s per short response on CPU
- **ollama binary**: Not in PATH; use full path or `& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"`

---

## Phase 3 — Virtual Environment + Dependencies ✅

User installed from their terminal (Codex sandbox blocks pip network access):

```powershell
& ".venv\Scripts\pip.exe" install -r requirements.txt
& ".venv\Scripts\pip.exe" install -r requirements-dev.txt
```

Key packages: duckdb 1.5.4, openai 2.44.0, streamlit 1.58.0, pandas 3.0.3,
pydantic 2.13.4, pytest 9.1.1, faker 40.23.0, black 26.5.1, ruff 0.15.20.

---

## Phase 4 — Verification ✅

```powershell
& ".venv\Scripts\python.exe" environment\verify.py
```

**Result: 25/25 passed** (Python, venv, all packages, all directories,
DuckDB functional, Ollama reachable, model loaded).

---

## Quick Reference

| File | Purpose |
|---|---|
| `.python312/` | Python 3.12 install (gitignored, 143 MB) |
| `.venv/` | Virtual environment (gitignored) |
| `requirements.txt` | Production deps |
| `requirements-dev.txt` | Dev deps |
| `.env` | Local config (gitignored) |
| `environment/config.py` | Central typed settings |
| `environment/verify.py` | Health check (25 checks) |
| `setup.bat` | Automated setup script |

## Sandbox Lessons Learned

1. **Cannot execute binaries outside workspace** — always copy/install tools inside the repo
2. **Cannot read certain directories** (`AppData\Local\Python\pythoncore-3.14-64` blocked)
3. **pip network access blocked** — user must install packages from their terminal
4. **Ollama CLI not found** even when service is running — use full path
5. **venv creates redirects** by default, which the sandbox follows and blocks — use `--copies` or copy full Python first
