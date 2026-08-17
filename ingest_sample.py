# ingest_sample.py
#
# This is a FALLBACK ONLY. It creates a tiny demo ChromaDB so the app has
# something to answer questions about the first time you run it.
#
# It will NOT touch your data if a chroma_db folder already exists.
#
# To use your REAL data: replace/merge this with your own ingestion pipeline,
# or just copy your existing chroma_db/ folder into this project folder and
# make sure config.py matches your ingestion settings exactly.

import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from config import PERSIST_DIR, COLLECTION_NAME, EMBEDDING_MODEL

SAMPLE_DOCS = [
    "RAG stands for Retrieval-Augmented Generation. It combines a retriever, "
    "which fetches relevant chunks of text from a knowledge base, with a "
    "language model that generates an answer grounded in those chunks.",

    "ChromaDB is an open-source vector database. It stores text as numeric "
    "embeddings and lets you search for the most similar chunks to a given "
    "query using vector similarity search.",

    "In this demo project, retriever.py loads an existing Chroma collection, "
    "chat.py combines the retriever with a Groq-hosted LLM using LangChain, "
    "and app.py exposes both through a FastAPI backend with a simple web UI.",

    "To swap in your own data, replace the contents of the chroma_db folder "
    "with the one produced by your own ingestion pipeline, and update "
    "config.py so PERSIST_DIR, COLLECTION_NAME, and EMBEDDING_MODEL match "
    "exactly what your ingestion script used.",
]


def needs_sample_data() -> bool:
    """True if there's no usable chroma_db yet."""
    if not os.path.isdir(PERSIST_DIR):
        return True
    return len(os.listdir(PERSIST_DIR)) == 0


def run():
    print(f"[ingest_sample] No existing data found in '{PERSIST_DIR}/' — creating demo data...")
    embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    docs = [Document(page_content=text) for text in SAMPLE_DOCS]

    Chroma.from_documents(
        documents=docs,
        embedding=embedding_function,
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION_NAME,
    )
    print("[ingest_sample] Demo data ready. Replace this with your real ingestion pipeline anytime.")


if __name__ == "__main__":
    if needs_sample_data():
        run()
    else:
        print(f"[ingest_sample] '{PERSIST_DIR}/' already has data — skipping demo ingestion.")
