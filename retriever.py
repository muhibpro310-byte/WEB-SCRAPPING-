# retriever.py
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import PERSIST_DIR, COLLECTION_NAME, EMBEDDING_MODEL, TOP_K

load_dotenv()

embedding_function = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    persist_directory=PERSIST_DIR,
    collection_name=COLLECTION_NAME,
    embedding_function=embedding_function,
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": TOP_K},
)


def get_relevant_docs(query: str):
    return retriever.invoke(query)


# quick standalone test: python retriever.py
if __name__ == "__main__":
    results = get_relevant_docs("What is this project about?")
    for i, doc in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(doc.page_content[:300])
        print(doc.metadata)
