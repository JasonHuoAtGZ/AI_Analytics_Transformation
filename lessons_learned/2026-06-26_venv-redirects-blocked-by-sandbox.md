# venv creates redirects that sandbox follows and blocks

- **Date**: 2026-06-26
- **Context**: Created `.venv` from Python 3.12 outside the workspace. The venv appeared to succeed but running `.venv\Scripts\python.exe` failed.
- **Error**: `Unable to create process using 'C:\Users\Jason Huo\AppData\Local\Programs\Python\Python312\python.exe'`
- **Root cause**: `python -m venv` by default creates launcher executables that redirect to the base Python installation. The sandbox follows these redirects and then blocks execution because the actual binary is outside the workspace.
- **Resolution**: Two options: (1) Use `python -m venv .venv --copies` which copies actual binaries instead of creating redirects, or (2) Copy the full Python installation into the workspace first, then create venv from the in-workspace copy. We used option (2) — copied Python 3.12 into `.python312/` (143 MB), then created venv from it.
- **Prevention**: Never create a venv from a Python outside the workspace without `--copies`. Better: always keep a workspace-local Python copy.
