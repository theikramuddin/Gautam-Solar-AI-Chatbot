# vectorstore/chroma_store.py — ChromaDB vector store management
import os
from typing import List
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma
from config import (
    MISTRAL_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
    RETRIEVER_TOP_K,
)


def get_embeddings() -> MistralAIEmbeddings:
    """Return Mistral embedding model."""
    return MistralAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=MISTRAL_API_KEY,
    )


def build_vectorstore(chunks: List[Document]) -> Chroma:
    """
    Embed all chunks and persist to ChromaDB.
    Call this once during setup / re-indexing.
    """
    print(f"🔢 Embedding {len(chunks)} chunks with Mistral ({EMBEDDING_MODEL})...")
    print("   This may take a few minutes on first run...\n")

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
        collection_name=CHROMA_COLLECTION_NAME,
    )

    print(f"✅ ChromaDB built & persisted at: {CHROMA_PERSIST_DIR}")
    print(f"   Collection: {CHROMA_COLLECTION_NAME}")
    print(f"   Total vectors stored: {vectorstore._collection.count()}\n")
    return vectorstore


def load_vectorstore() -> Chroma:
    """Load an existing persisted ChromaDB vectorstore."""
    if not os.path.exists(CHROMA_PERSIST_DIR):
        raise FileNotFoundError(
            f"ChromaDB not found at '{CHROMA_PERSIST_DIR}'.\n"
            "Please run: python ingest.py"
        )

    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
    )
    count = vectorstore._collection.count()
    print(f"✅ ChromaDB loaded — {count} vectors in collection '{CHROMA_COLLECTION_NAME}'")
    return vectorstore


def get_retriever(vectorstore: Chroma = None, top_k: int = RETRIEVER_TOP_K):
    """Return a similarity-search retriever."""
    vs = vectorstore or load_vectorstore()
    return vs.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k},
    )