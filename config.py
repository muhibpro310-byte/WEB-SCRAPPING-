# config.py
# Central place for settings shared by ingest_sample.py, retriever.py, and app.py.
#
# IMPORTANT: If you already have a ChromaDB from your own ingestion pipeline,
# change these three values to match EXACTLY what your ingestion script used.
# A mismatch here is the #1 reason retrieval comes back empty or wrong.

PERSIST_DIR = "chroma_db"                                   # your persist_directory
COLLECTION_NAME = "my_collection"                            # your collection name
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"   # your embedding model

# How many chunks to retrieve per question
TOP_K = 4

# OpenAI model used for generation
OPENAI_MODEL = "gpt-oss-120b"
