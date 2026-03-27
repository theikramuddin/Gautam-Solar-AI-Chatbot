# config.py — Central configuration for Gautam Solar RAG
import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")

# ── ChromaDB ──────────────────────────────────────────────
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "gautam_solar")

# ── Models ────────────────────────────────────────────────
EMBEDDING_MODEL = "mistral-embed"
LLM_MODEL = "mistral-large-latest"
LLM_TEMPERATURE = 0.2

# ── Chunking ──────────────────────────────────────────────
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))

# ── Retrieval ─────────────────────────────────────────────
RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", 5))

# ── Data Paths ────────────────────────────────────────────
DATA_DIR = "./data/raw"
PDF_DIR = f"{DATA_DIR}/pdfs"
TEXT_DIR = f"{DATA_DIR}/text"
JSON_DIR = f"{DATA_DIR}/json"

# ── Company Info ──────────────────────────────────────────
COMPANY_NAME = "Gautam Solar"
COMPANY_EMAIL = "info@gautamsolar.com"
COMPANY_PHONE = "1800-532-0800"
COMPANY_WHATSAPP = "+91 93117 97248"