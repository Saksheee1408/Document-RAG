# DocRAG Intelligence Studio — Grounded Knowledge Q&A System

[![Live Demo](https://img.shields.io/badge/Streamlit-Live%20Demo-2563EB?style=for-the-badge&logo=streamlit)](https://document-rag-d5bc7wrtfndbirsawmumau.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FAISS Vector Search](https://img.shields.io/badge/FAISS-Vector%20Search-047857?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![Groq LLM](https://img.shields.io/badge/Groq-LPU%20Inference-F59E0B?style=for-the-badge)](https://groq.com)

A modular, production-ready Retrieval-Augmented Generation (RAG) system built in Python to perform grounded document question answering over a multi-PDF knowledge base (`files/`).

👉 **Live Hosted Web App**: [https://document-rag-d5bc7wrtfndbirsawmumau.streamlit.app/](https://document-rag-d5bc7wrtfndbirsawmumau.streamlit.app/)

---

## 🏗️ Architecture Overview

The system follows a strict 8-step pipeline to ingest documents, index semantic vectors, perform vector similarity search, and generate grounded answers:

```
[ 7 PDF Files in files/ ] 
       │
       ▼
1. PDF Ingestion (pypdf text & page metadata extraction)
       │
       ▼
2. Structure-Aware Chunking (~200 tokens target size + 40 tokens overlap)
       │
       ▼
3. Local Vector Embedding (SentenceTransformers `all-MiniLM-L6-v2`)
       │
       ▼
4. FAISS Vector Store Indexing (IndexFlatIP for Cosine Similarity)
       │
       ▼
5. User Question ──► Query Embedding
       │
       ▼
6. FAISS Top-K Retrieval & Similarity Thresholding (Threshold: 0.20)
       │
       ▼
7. Groq LLM Grounding Synthesis (`groq/compound-mini` with fallback)
       │
       ▼
8. Grounded Answer + Verifiable Source Attribution (Doc, Page, Score %, Chunk ID)
```

---

## 🛠️ Technology Stack & Rationale

| Layer | Technology | Selection Rationale |
|---|---|---|
| **Language** | Python 3.10+ | Standard ecosystem for machine learning, NLP, and vector search. |
| **PDF Processing** | `pypdf` | Fast, lightweight pure-Python reader preserving page numbers and text layout metadata without native C binaries. |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) | 384-dimensional dense embeddings. Runs CPU-locally with zero API costs or network latency. |
| **Vector Store** | `faiss-cpu` (`IndexFlatIP`) | High-performance C++ vector similarity index by Meta. Uses inner product on L2-normalized vectors for exact Cosine Similarity. |
| **LLM Generation** | Groq API (`groq/compound-mini`) | Ultra-fast LPU inference engine with fallback models (`groq/compound`, `qwen/qwen3.6-27b`, `openai/gpt-oss-120b`). |
| **User Interface** | `streamlit` | Linear/Vercel-inspired monochrome dashboard with Dark/Light theme toggle, sample query chips, and visual progress score bars. |
| **Testing** | `pytest` | Automated test suite (16/16 test cases passing) validating chunking, retrieval, embeddings, and grounding guardrails. |

---

## ✂️ Chunking Strategy & Rationale

- **Target Chunk Size:** ~200 words / tokens (~800–1,000 characters).
- **Overlap:** ~40 words / tokens (~150–200 characters).
- **Structure Awareness:** Text is split along structural paragraph boundaries before applying sliding-window token bounds.
- **Why these parameters?**
  1. 200 tokens provides a focused context window for paragraphs, policies, procedures, and tables without diluting semantic vector density.
  2. 100 token overlap prevents context fragmentation across chunk boundaries.
  3. Every chunk retains immutable metadata: `document_name`, `page_number`, `chunk_index`, and `chunk_id`.

---

## 🔎 Retrieval & Grounding Safeguards

To prevent hallucinations and confident fabrications:

1. **Similarity Score Thresholding:** Retrieved chunks must pass a minimum cosine similarity threshold (default `0.20`). Queries falling below this threshold trigger an immediate unanswerable fallback.
2. **Grounding System Prompt:** The LLM is strictly instructed to answer using **ONLY** the provided context block. It is forbidden from speculating or referencing outside knowledge.
3. **Explicit Refusal Fallback:** If the context is insufficient, the system returns:
   > *"The answer is not available in the provided documents."*
4. **Verifiable Source Attribution:** Returns source document name, page number, chunk ID, exact text preview, and a visual relevance percentage bar. Unanswerable queries strip citations to avoid misleading references.

---

## 🚀 Quick Setup Guide (< 5 Minutes)

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/Saksheee1408/Document-RAG.git
cd Document-RAG

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and insert your Groq API Key:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
GROQ_API_KEY=gsk_your_actual_groq_api_key
GROQ_MODEL=groq/compound-mini
EMBEDDING_MODEL=all-MiniLM-L6-v2
TOP_K=4
SIMILARITY_THRESHOLD=0.20
DATA_DIR=files
INDEX_DIR=vector_store_data
```

### 3. Run Automated Test Suite
```bash
pytest tests/ -v
```

### 4. Launch Local Streamlit Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 🔒 Security Practices

- **Zero Hardcoded Secrets:** API keys are dynamically loaded via `python-dotenv` and Streamlit Secrets.
- **Git Protection:** `.env` is ignored in `.gitignore`. Only `.env.example` with safe placeholder tokens is committed.
- **Sanitized Error Handling:** Raw API stack traces and auth tokens are masked into clean user-friendly banners.

---

## ⚖️ Trade-offs and Limitations

- **Local CPU Embeddings:** `all-MiniLM-L6-v2` is fast and lightweight on CPU, but complex domain-specific jargon may benefit from larger models (e.g., `bge-large-en-v1.5`).
- **Exact Vector Index:** FAISS `IndexFlatIP` provides exact nearest-neighbor search, optimal for thousands of chunks. Scaling to millions of documents would use approximate indexing (`HNSW` / `IVFFlat`) or distributed vector DBs (Qdrant/Milvus).
- **PDF Table Layouts:** PyPDF handles formatted tables well, but complex multi-column borderless tables can benefit from specialized parsers (`pdfplumber` or vision-OCR models).

---

## 🤖 AI Assistant Disclosure

In accordance with assignment guidelines, this project was designed and developed with the assistance of **Antigravity AI Assistant** (Google DeepMind Agentic Coding AI) for architectural planning, code modularization, prompt engineering, theme design, and test suite generation.
