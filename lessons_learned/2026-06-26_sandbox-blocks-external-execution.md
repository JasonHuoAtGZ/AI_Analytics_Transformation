# Cannot execute binaries outside workspace

- **Date**: 2026-06-26
- **Context**: Attempted to run Python 3.12 from `C:\Users\Jason Huo\AppData\Local\Programs\Python\Python312\python.exe` to create a venv
- **Error**: `Access is denied` / `Unable to create process`
- **Root cause**: Codex sandbox blocks execution of any binary outside the repository root `C:\Users\Jason Huo\OneDrive\Documents\AI_Analytics_Transformation`
- **Resolution**: Copied full Python 3.12 installation into `.python312/` inside the workspace, then created venv from the in-workspace copy
- **Prevention**: Always install or copy tools inside the repository. Never reference binaries outside the workspace path.
