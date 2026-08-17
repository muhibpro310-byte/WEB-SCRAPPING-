# RAG Chat

A minimal Retrieval-Augmented Generation chat app: ChromaDB retriever + OpenAI (via LangChain) + FastAPI + a simple web UI. Runs with one click after install.

## Project structure

```
rag-chat-app/
├── config.py          # shared settings — persist dir, collection name, embedding model
├── ingest_sample.py   # fallback demo data (only runs if chroma_db/ is empty)
├── retriever.py        # loads the Chroma vectorstore + retriever
├── chat.py             # retriever + Groq LLM combined into a RAG chain
├── app.py               # FastAPI backend (serves the API + the frontend)
├── static/index.html    # chat UI
├── requirements.txt
├── .env.example
├── start.bat             # one-click launcher (Windows)
└── start.sh              # one-click launcher (Mac/Linux)
```

## 1. First-time setup

**Windows:** double-click `start.bat`.
**Mac/Linux:** run `./start.sh` (you may need `chmod +x start.sh` first).

The script will:
1. Create a virtual environment (`venv/`)
2. Install everything in `requirements.txt`
3. Create a `.env` file from `.env.example` and open it for you to paste in your OpenAI API key (from https://platform.openai.com/api-keys)
4. Launch the server and open **http://127.0.0.1:8000** in your browser

Every time after that, just double-click `start.bat` / run `./start.sh` again — it skips setup steps that are already done and launches straight away.

## 2. Plug in YOUR real ingested data

Right now the app ships with a tiny demo dataset (`ingest_sample.py`) so it works out of the box. To use your own ChromaDB from your existing ingestion pipeline:

1. Copy your `chroma_db/` folder into this project folder (replacing the demo one), **or** point `PERSIST_DIR` in `config.py` at wherever it already lives.
2. Open `config.py` and make sure these three values match EXACTLY what your ingestion script used:
   - `PERSIST_DIR`
   - `COLLECTION_NAME`
   - `EMBEDDING_MODEL`
3. Restart the app.

If retrieval comes back empty or the answers don't reference your content, a mismatch in one of those three values is almost always the cause.

## 3. Testing pieces individually

```
venv\Scripts\activate      (Windows)   or   source venv/bin/activate   (Mac/Linux)

python retriever.py   # sanity-check retrieval alone, prints top chunks
python chat.py         # CLI chat loop, no browser needed
```

## 4. Swapping the LLM or model

Edit `OPENAI_MODEL` in `config.py`. Current default is `gpt-oss-120b` (OpenAI's open-weight model, served directly from their API). Swap to `gpt-4o-mini` or `gpt-4o` if you'd rather use their closed models.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "OPENAI_API_KEY is not set" | `.env` still has the placeholder — open it and paste your real key |
| "Invalid API Key" / 401 error | Key is wrong, expired, or has no billing set up on your OpenAI account — check https://platform.openai.com/account/billing |
| Retriever returns nothing relevant | `PERSIST_DIR` / `COLLECTION_NAME` / `EMBEDDING_MODEL` in `config.py` don't match your ingestion script |
| First run is slow | `sentence-transformers` downloads the embedding model (~90MB) the first time only |
| Port already in use | Another app is using 8000 — edit the port in `start.bat`/`start.sh` and `app.py`'s uvicorn call |
