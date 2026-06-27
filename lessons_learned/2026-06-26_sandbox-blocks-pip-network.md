# pip network access blocked by sandbox

- **Date**: 2026-06-26
- **Context**: Attempted to run `pip install -r requirements.txt` from the in-workspace venv
- **Error**: `WinError 10013` — `以一种访问权限不允许的方式做了一个访问套接字的尝试` (socket access denied)
- **Root cause**: The Codex sandbox blocks outbound network connections from processes running inside the sandbox. pip cannot reach PyPI to download packages.
- **Resolution**: The user ran `pip install` from their own terminal (outside Codex), which has unrestricted network access. Both `requirements.txt` and `requirements-dev.txt` installed successfully.
- **Prevention**: Any command requiring internet access (pip install, npm install, git clone from remote, curl, etc.) must be escalated or run by the user from their own terminal.
