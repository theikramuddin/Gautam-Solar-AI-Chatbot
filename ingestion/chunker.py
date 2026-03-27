# ingestion/chunker.py — Smart chunking for Gautam Solar RAG
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(docs: List[Document]) -> List[Document]:
    """
    Split documents into chunks.
    FAQs and product catalog entries are kept as-is (already small).
    PDFs and text files are split recursively.
    """
    to_split = []
    keep_as_is = []

    for doc in docs:
        source_type = doc.metadata.get("source_type", "")
        if source_type in ("faq", "product_catalog"):
            keep_as_is.append(doc)
        else:
            to_split.append(doc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    split_chunks = splitter.split_documents(to_split)

    # Add chunk index to metadata for traceability
    for i, chunk in enumerate(split_chunks):
        chunk.metadata["chunk_index"] = i

    all_chunks = keep_as_is + split_chunks

    print(f"✂️  Chunking complete:")
    print(f"   Kept as-is (FAQs + Products): {len(keep_as_is)}")
    print(f"   Split chunks (PDFs + Text):   {len(split_chunks)}")
    print(f"   Total chunks:                 {len(all_chunks)}\n")

    return all_chunks