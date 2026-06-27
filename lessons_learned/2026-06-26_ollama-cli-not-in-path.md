# Ollama CLI not in PATH even after install

- **Date**: 2026-06-26
- **Context**: After winget install of Ollama, `ollama` command was not recognized in the user's terminal
- **Error**: `'ollama' is not recognized as an internal or external command`
- **Root cause**: Ollama installer places the binary at `%LOCALAPPDATA%\Programs\Ollama\ollama.exe` but may not add it to the system PATH. Even after a fresh terminal, the command was not found.
- **Resolution**: Use the full path: `& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull llama3.1:8b`. The Ollama service itself (background Windows service) was already running — only the CLI was affected.
- **Prevention**: After installing CLI tools via winget, verify with the full path. Do not assume PATH is updated. The API (localhost:11434) can be used as a fallback for most operations.
