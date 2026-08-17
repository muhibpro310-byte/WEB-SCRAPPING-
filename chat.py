# chat.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import OPENAI_MODEL
from retriever import retriever

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
    )

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.2,
    api_key=os.getenv("OPENAI_API_KEY"),
)

prompt = ChatPromptTemplate.from_template(
    """You are a helpful assistant. Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't know — don't make things up.

Context:
{context}

Question:
{question}

Answer:"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


def ask(question: str) -> str:
    """Simple string-in, string-out call used by chat.py's CLI."""
    return rag_chain.invoke(question)


def ask_with_sources(question: str) -> dict:
    """Used by app.py — returns the answer plus the chunks that backed it."""
    docs = retriever.invoke(question)
    context = format_docs(docs)
    answer = (prompt | llm | StrOutputParser()).invoke(
        {"context": context, "question": question}
    )
    return {
        "answer": answer,
        "sources": [
            {"content": d.page_content[:400], "metadata": d.metadata} for d in docs
        ],
    }


# quick standalone CLI test: python chat.py
if __name__ == "__main__":
    print("RAG chat ready. Type 'exit' to quit.\n")
    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break
        print(f"\nBot: {ask(q)}\n")
