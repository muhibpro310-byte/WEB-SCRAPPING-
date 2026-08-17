#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "=============================================="
echo "  RAG Chat - one-click setup and launch"
echo "=============================================="

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 not found. Install Python 3.10+ and try again."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "[setup] Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "[setup] Installing/checking dependencies... this can take a few minutes the first time."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "[setup] No .env found, creating one from .env.example..."
    cp .env.example .env
fi

if grep -q "your_openai_api_key_here" .env; then
    echo ""
    echo "[ACTION NEEDED] Edit the .env file and replace your_openai_api_key_here"
    echo "with your real OpenAI API key (get one at https://platform.openai.com/api-keys)."
    echo "Save the file, then press Enter here to continue."
    ${EDITOR:-nano} .env
    read -p "Press Enter once your key is saved..."
fi

echo "[launch] Starting server at http://127.0.0.1:8000 ..."
( sleep 2 && (open http://127.0.0.1:8000 2>/dev/null || xdg-open http://127.0.0.1:8000 2>/dev/null) ) &
uvicorn app:app --host 127.0.0.1 --port 8000
