# Sandbox blocks reading certain AppData directories

- **Date**: 2026-06-26
- **Context**: Attempted to read and copy Python 3.14.6 from `C:\Users\Jason Huo\AppData\Local\Python\pythoncore-3.14-64` into the workspace
- **Error**: `Access denied` — `Get-ChildItem` and `Copy-Item` both blocked with `UnauthorizedAccessException`
- **Root cause**: The sandbox restricts read access to certain directories under `AppData\Local\Python`, even though read access to `:root` is declared
- **Resolution**: Used Python 3.12 from `AppData\Local\Programs\Python\Python312` instead, which was readable. The user manually ran the copy from their own terminal.
- **Prevention**: Always verify directory readability with `Test-Path` and `Get-ChildItem` before attempting copy operations. Have the user run file copy commands from their own terminal when the sandbox blocks reads.
