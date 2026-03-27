#!/usr/bin/env python3
"""
ingest.py — One-time data ingestion script for Gautam Solar RAG

Run this ONCE to build the ChromaDB vectorstore:
    python ingest.py

Re-run whenever you add new documents to data/raw/
"""
import time
import sys
from ingestion.loader import load_all_documents
from ingestion.chunker import chunk_documents
from vectorstore.chroma_store import build_vectorstore


def main():
    print("=" * 60)
    print("  🌞 GAUTAM SOLAR RAG — Data Ingestion Pipeline")
    print("=" * 60)
    start = time.time()

    # ── Step 1: Load ──────────────────────────────────────
    print("\n[1/3] Loading documents...")
    docs = load_all_documents(
        pdf_dir="./data/raw/pdfs",
        text_dir="./data/raw/text",
        faq_json="./data/raw/json/faqs.json",
        catalog_json="./data/raw/json/product_catalog.json",
        include_website=False,  # Set True to also scrape the live website
    )

    if not docs:
        print("❌ No documents found. Please add files to data/raw/")
        sys.exit(1)

    # ── Step 2: Chunk ─────────────────────────────────────
    print("[2/3] Chunking documents...")
    chunks = chunk_documents(docs)

    # ── Step 3: Embed & Store ─────────────────────────────
    print("[3/3] Embedding and storing in ChromaDB...")
    vectorstore = build_vectorstore(chunks)

    elapsed = time.time() - start
    print("=" * 60)
    print(f"  ✅ Ingestion complete in {elapsed:.1f}s")
    print(f"  📦 {len(chunks)} chunks embedded and stored")
    print(f"  🚀 Run the chatbot: streamlit run app/streamlit_app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()