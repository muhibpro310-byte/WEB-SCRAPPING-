# app.py
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Make sure there's *something* in the vector store before we boot,
    # so a first-time run never hits an empty/broken retriever.
    import ingest_sample

    if ingest_sample.needs_sample_data():
        ingest_sample.run()
    yield


app = FastAPI(title="RAG Chat", lifespan=lifespan)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list


@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Imported lazily so the health check above still works even if
    # GROQ_API_KEY is missing — chat.py raises on import if it's not set.
    from chat import ask_with_sources

    try:
        result = ask_with_sources(req.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(answer=result["answer"], sources=result["sources"])


app.mount("/static", StaticFiles(directory="static"), name="static")
