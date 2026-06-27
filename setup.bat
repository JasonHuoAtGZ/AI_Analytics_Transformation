@echo off
setlocal enabledelayedexpansion
echo ============================================================
echo   AI Analytics Transformation - Environment Setup
echo ============================================================
echo.

echo [1/6] Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo   ERROR: Python not found. Install Python 3.12+ first.
    echo   https://www.python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo   Python %%v found.

echo.
echo [2/6] Creating virtual environment...
if not exist .venv (
    python -m venv .venv
    echo   Created .venv
) else (
    echo   .venv already exists.
)

echo.
echo [3/6] Installing dependencies...
call .venv\Scripts\activate
pip install -q -r requirements.txt
pip install -q -r requirements-dev.txt
echo   Dependencies installed.

echo.
echo [4/6] Checking Ollama...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo   WARNING: Ollama not found.
    echo   Install from: https://ollama.com
    echo   After install, run: ollama pull llama3.1:8b
) else (
    for /f "tokens=*" %%v in ('ollama --version 2^>^&1') do echo   Ollama %%v found.
    ollama list 2>nul | findstr "llama3.1:8b" >nul
    if %errorlevel% neq 0 (
        echo   Pulling llama3.1:8b ^(^~4.7 GB, may take several minutes^)...
        ollama pull llama3.1:8b
    ) else (
        echo   llama3.1:8b already available.
    )
)

echo.
echo [5/6] Creating .env from template...
if not exist .env (
    copy .env.example .env >nul
    echo   Created .env from .env.example
) else (
    echo   .env already exists.
)

echo.
echo [6/6] Running verification...
python environment/verify.py

echo.
echo ============================================================
echo   Setup complete. Run ^"streamlit run src/ui/app.py^" to start.
echo ============================================================
pause
