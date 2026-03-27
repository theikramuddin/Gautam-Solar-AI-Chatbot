# ingestion/loader.py — Load all data sources for Gautam Solar RAG
import os
import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
)

# Website URLs to scrape
GAUTAM_SOLAR_URLS = [
    "https://gautamsolar.com/",
    "https://gautamsolar.com/topcon",
    "https://gautamsolar.com/mono",
    "https://gautamsolar.com/solarplants",
    "https://gautamsolar.com/kusum",
    "https://gautamsolar.com/quality",
]


def load_pdfs(pdf_dir: str) -> List[Document]:
    """Load all PDF files from a directory."""
    docs = []
    pdf_path = Path(pdf_dir)
    if not pdf_path.exists():
        print(f"⚠️  PDF directory not found: {pdf_dir}")
        return docs

    for pdf_file in pdf_path.glob("*.pdf"):
        try:
            loader = PyPDFLoader(str(pdf_file))
            pages = loader.load()
            # Add source metadata
            for page in pages:
                page.metadata["source_type"] = "pdf"
                page.metadata["filename"] = pdf_file.name
            docs.extend(pages)
            print(f"  ✅ Loaded PDF: {pdf_file.name} ({len(pages)} pages)")
        except Exception as e:
            print(f"  ❌ Failed to load {pdf_file.name}: {e}")
    return docs


def load_text_files(text_dir: str) -> List[Document]:
    """Load all .txt files from a directory."""
    docs = []
    text_path = Path(text_dir)
    if not text_path.exists():
        print(f"⚠️  Text directory not found: {text_dir}")
        return docs

    for txt_file in text_path.glob("*.txt"):
        try:
            loader = TextLoader(str(txt_file), encoding="utf-8")
            pages = loader.load()
            for page in pages:
                page.metadata["source_type"] = "text"
                page.metadata["filename"] = txt_file.name
            docs.extend(pages)
            print(f"  ✅ Loaded TXT: {txt_file.name}")
        except Exception as e:
            print(f"  ❌ Failed to load {txt_file.name}: {e}")
    return docs


def load_json_faqs(json_path: str) -> List[Document]:
    """Load FAQ JSON and convert each Q&A into a Document."""
    docs = []
    path = Path(json_path)
    if not path.exists():
        print(f"⚠️  FAQ JSON not found: {json_path}")
        return docs

    try:
        with open(path, "r", encoding="utf-8") as f:
            faqs = json.load(f)

        for i, faq in enumerate(faqs):
            # Combine Q&A into a single chunk for better retrieval
            content = f"Question: {faq['question']}\nAnswer: {faq['answer']}"
            doc = Document(
                page_content=content,
                metadata={
                    "source_type": "faq",
                    "category": faq.get("category", "General"),
                    "filename": path.name,
                    "faq_index": i,
                },
            )
            docs.append(doc)
        print(f"  ✅ Loaded FAQs: {len(docs)} Q&A pairs from {path.name}")
    except Exception as e:
        print(f"  ❌ Failed to load FAQs: {e}")
    return docs


def load_product_catalog(json_path: str) -> List[Document]:
    """Load product catalog JSON into structured Documents."""
    docs = []
    path = Path(json_path)
    if not path.exists():
        print(f"⚠️  Product catalog not found: {json_path}")
        return docs

    try:
        with open(path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        for product in catalog.get("products", []):
            lines = [
                f"Product: {product['name']}",
                f"Type: {product['type']}",
                f"Power Range: {product['power_range_wp']} Wp",
                f"Efficiency: {product['efficiency_pct']}%",
                f"Temperature Coefficient: {product.get('temp_coefficient_pmax', 'N/A')}",
                f"Bifacial Gain: {product.get('bifacial_gain_pct', 'N/A')}%",
                f"Warranty Product: {product['warranty_product_yrs']} years",
                f"Warranty Performance: {product['warranty_performance_yrs']} years",
                f"Certifications: {', '.join(product.get('certifications', []))}",
                f"ALMM Approved: {product.get('almm_approved', False)}",
                f"Best For: {', '.join(product.get('best_for', []))}",
                f"Price Range: Rs {product.get('price_range_inr_per_wp', 'N/A')}/Wp",
                f"Dimensions: {product.get('dimensions_mm', 'N/A')} mm",
                f"Weight: {product.get('weight_kg', 'N/A')} kg",
            ]
            content = "\n".join(lines)
            doc = Document(
                page_content=content,
                metadata={
                    "source_type": "product_catalog",
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "product_type": product["type"],
                    "filename": path.name,
                },
            )
            docs.append(doc)

        print(f"  ✅ Loaded Product Catalog: {len(docs)} products")
    except Exception as e:
        print(f"  ❌ Failed to load product catalog: {e}")
    return docs


def load_website(urls: List[str] = None) -> List[Document]:
    """Scrape Gautam Solar website pages."""
    docs = []
    urls = urls or GAUTAM_SOLAR_URLS
    try:
        loader = WebBaseLoader(urls)
        loader.requests_kwargs = {"timeout": 15}
        pages = loader.load()
        for page in pages:
            page.metadata["source_type"] = "website"
        docs.extend(pages)
        print(f"  ✅ Scraped Website: {len(docs)} pages")
    except Exception as e:
        print(f"  ⚠️  Website scraping skipped (offline/error): {e}")
    return docs


def load_all_documents(
    pdf_dir: str = "./data/raw/pdfs",
    text_dir: str = "./data/raw/text",
    faq_json: str = "./data/raw/json/faqs.json",
    catalog_json: str = "./data/raw/json/product_catalog.json",
    include_website: bool = False,
) -> List[Document]:
    """Master loader — loads all data sources."""
    print("\n📂 Loading all documents...\n")
    all_docs = []

    all_docs.extend(load_pdfs(pdf_dir))
    all_docs.extend(load_text_files(text_dir))
    all_docs.extend(load_json_faqs(faq_json))
    all_docs.extend(load_product_catalog(catalog_json))

    if include_website:
        all_docs.extend(load_website())

    print(f"\n📊 Total documents loaded: {len(all_docs)}\n")
    return all_docs