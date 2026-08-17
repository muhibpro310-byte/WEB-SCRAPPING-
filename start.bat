@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ==============================================
echo   RAG Chat - one-click setup and launch
echo ==============================================

REM --- 1. Check Python is installed ---
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found on PATH.
    echo Install Python 3.10+ from https://www.python.org/downloads/ and try again.
    pause
    exit /b 1
)

REM --- 2. Create virtual environment if it doesn't exist yet ---
if not exist "venv\" (
    echo [setup] Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

REM --- 3. Install dependencies (fast no-op if already installed) ---
echo [setup] Installing/checking dependencies... this can take a few minutes the first time.
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency install failed. See the error above.
    pause
    exit /b 1
)

REM --- 4. Make sure .env exists and has a real key ---
if not exist ".env" (
    echo [setup] No .env found, creating one from .env.example...
    copy ".env.example" ".env" >nul
)

findstr /C:"your_openai_api_key_here" ".env" >nul
if not errorlevel 1 (
    echo.
    echo [ACTION NEEDED] Open the .env file that just opened in Notepad
    echo and replace your_openai_api_key_here with your real OpenAI API key
    echo ^(get one at https://platform.openai.com/api-keys^).
    echo Save the file, close Notepad, then come back here and press any key.
    echo.
    notepad ".env"
    pause
)

REM --- 5. Launch the app and open the browser ---
echo [launch] Starting server at http://127.0.0.1:8000 ...
start "" http://127.0.0.1:8000
uvicorn app:app --host 127.0.0.1 --port 8000

pause
