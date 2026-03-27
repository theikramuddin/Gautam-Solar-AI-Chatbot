# ☀️ Gautam Solar AI Chatbot — RAG Project

> **Surya** - An intelligent solar energy assistant powered by **LangChain + ChromaDB + Mistral AI**

---

## 🏗️ Project Structure

```
gautam_solar_rag/
├── data/
│   └── raw/
│       ├── pdfs/                  ← Product datasheets, KUSUM guide, manuals
│       ├── text/                  ← Blog articles, company profile
│       └── json/                  ← FAQs, product catalog
│
├── ingestion/
│   ├── loader.py                  ← Load PDFs, TXTs, JSONs, website
│   └── chunker.py                 ← Smart document chunking
│
├── vectorstore/
│   └── chroma_store.py            ← ChromaDB embed & retrieve
│
├── chain/
│   └── rag_chain.py               ← LangChain RAG chain + memory
│
├── app/
│   └── streamlit_app.py           ← Chatbot UI
│
├── utils/
│   └── evaluate.py                ← RAG evaluation suite
│
├── ingest.py                      ← One-time data ingestion runner
├── config.py                      ← Central configuration
├── .env.example                   ← Environment variables template
├── requirements.txt               ← All dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone <your-repo>
cd gautam_solar_rag
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env and add your MISTRAL_API_KEY
```

Get your free Mistral API key at: https://console.mistral.ai/

### 3. Add Data Files
Copy all dummy data files into the `data/raw/` directory:
```
data/raw/pdfs/
    product_datasheet.pdf
    pm_kusum_scheme_guide.pdf
    installation_maintenance_manual.pdf
    roi_savings_guide.pdf

data/raw/text/
    company_profile.txt
    blog_topcon_vs_perc.txt
    blog_rooftop_solar_guide.txt

data/raw/json/
    faqs.json
    product_catalog.json
```

### 4. Build the Vector Database (Run Once)
```bash
python ingest.py
```

This will:
- Load all documents
- Chunk them intelligently
- Embed using Mistral `mistral-embed` model
- Store in ChromaDB at `./chroma_db/`

### 5. Launch the Chatbot
```bash
streamlit run app/streamlit_app.py
```

Open your browser at: **http://localhost:8501**

---

## 🔧 Configuration

Edit `config.py` or `.env` to customize:

| Setting | Default | Description |
|---|---|---|
| `LLM_MODEL` | `mistral-large-latest` | Mistral model for generation |
| `EMBEDDING_MODEL` | `mistral-embed` | Embedding model |
| `CHUNK_SIZE` | `800` | Characters per chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between chunks |
| `RETRIEVER_TOP_K` | `5` | Retrieved docs per query |

---

## 🧪 Evaluate RAG Quality
```bash
python utils/evaluate.py
```

Tests 7 real questions against expected keywords in answers.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral Large (mistral-large-latest) |
| Embeddings | Mistral Embed (mistral-embed) |
| Vector DB | ChromaDB (local persistence) |
| RAG Framework | LangChain |
| UI | Streamlit |
| PDF Parsing | PyPDF |
| Data | PDFs, JSON, TXT |

---

## 💡 Sample Questions to Try

- *"Which Gautam Solar panel is best for my 5kWp rooftop in Delhi?"*
- *"What is the efficiency of the G12 R TOPCon module?"*
- *"Am I eligible for PM-KUSUM as a farmer in Rajasthan?"*
- *"How much subsidy will I get under PM-KUSUM?"*
- *"What is the payback period for a 10kWp commercial system?"*
- *"Compare TOPCon vs Mono PERC solar panels"*
- *"How often should I clean Gautam Solar panels?"*
- *"What certifications does Gautam Solar have?"*

---

## 📞 Contact Gautam Solar

- 📧 info@gautamsolar.com  
- 📞 1800-532-0800  
- 💬 WhatsApp: +91 93117 97248  
- 🌐 www.gautamsolar.com
