# Production RAG Document Q&A Knowledge System

A modular, production-ready Retrieval-Augmented Generation (RAG) system built in Python to perform grounded document question answering over a multi-PDF knowledge base (`files/`).

---

## 🏗️ Architecture Overview

The system follows a strict 8-step pipeline to ingest documents, index semantic vectors, and generate grounded answers:

```
[ PDF Files ] 
      │
      ▼
1. PDF Ingestion (pypdf text & page metadata extraction)
      │
      ▼
2. Structure-Aware Chunking (~600 words target size + 100 words overlap)
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
6. FAISS Top-K Retrieval & Similarity Score Thresholding (Threshold: 0.35)
      │
      ▼
7. Groq LLM Grounding Prompt (`llama-3.3-70b-versatile`)
      │
      ▼
8. Grounded Answer + Verifiable Source Attribution (Doc, Page, Chunk ID)
```

---

## 🛠️ Technology Stack & Rationale

| Layer | Technology | Purpose & Selection Rationale |
|---|---|---|
| **Language** | Python 3.10+ | Standard ecosystem for machine learning, NLP, and vector search. |
| **PDF Processing** | `pypdf` | Fast, lightweight pure-Python PDF reader that accurately preserves page numbers and text layouts without external binaries. |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) | State-of-the-art 384-dimensional dense embeddings. Runs efficiently locally on CPU with zero API costs or network latency. |
| **Vector Store** | `faiss-cpu` (`IndexFlatIP`) | High-performance C++ vector similarity index by Meta. Uses inner product on L2-normalized vectors to achieve exact Cosine Similarity. |
| **LLM Generation** | Groq API (`llama-3.3-70b-versatile`) | Ultra-fast LPU inference engine powering LLaMA 3.3 70B for high-quality grounded reasoning. |
| **User Interface** | `streamlit` | Clean, interactive web dashboard for submitting questions, inspecting source attributions, and managing vector indices. |
| **Testing & Environment** | `pytest` / `python-dotenv` | Automated test suite with mocked LLM calls and clean configuration management via `.env`. |

---

## ✂️ Chunking Strategy & Rationale

- **Target Chunk Size:** ~600 words / tokens (~2,000–2,400 characters).
- **Overlap:** ~100 words / tokens (~350–400 characters).
- **Structure Awareness:** Text is split cleanly along structural boundaries (paragraphs/newlines) before applying sliding window token bounds.
- **Why these parameters?**
  1. 600 tokens provides sufficient context window for complete paragraphs, procedures, and table rows without diluting semantic signal.
  2. 100 token overlap prevents context fragmentation across chunk boundaries (e.g., ensuring a multi-sentence policy is not split mid-thought).
  3. Every chunk retains immutable metadata: `document_name`, `page_number`, `chunk_index`, and `chunk_id`.

---

## 🔎 Retrieval & Grounding Safeguards

To prevent hallucinations and confident fabrications:

1. **Similarity Score Thresholding:** Retrieved chunks must pass a minimum cosine similarity threshold (default `0.35`). Queries falling below this threshold trigger an immediate unanswerable fallback.
2. **Grounding System Prompt:** The LLM is instructed to answer strictly using the provided context block. It is forbidden from using outside knowledge or speculating.
3. **Explicit Refusal Fallback:** If the context is insufficient, the system returns:
   > *"The answer is not available in the provided documents."*
4. **Clean Source Attribution:** Unanswerable queries strip all source citations, preventing misleading or fabricated references.

---

## 🚀 Quick Setup Guide (< 10 Minutes)

### 1. Prerequisites
Ensure Python 3.10+ and `git` are installed on your machine.

### 2. Clone Repository & Setup Environment
```bash
git clone <repository_url>
cd Doc-RAG

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and add your Groq API Key:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
GROQ_API_KEY=gsk_your_actual_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=all-MiniLM-L6-v2
TOP_K=4
SIMILARITY_THRESHOLD=0.35
```

### 4. Knowledge Base Files
Place all target PDF documents inside the `files/` directory (already pre-populated with 7 PDFs).

### 5. Run Automated Tests
Execute the unit and integration test suite:
```bash
pytest tests/ -v
```

### 6. Launch Streamlit Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`. Click **"🔨 Rebuild Vector Index"** on the sidebar if launching for the first time.

---

## 🔒 Security Practices

- **Zero Hardcoded Secrets:** All secrets are loaded dynamically via `python-dotenv`.
- **Git Protection:** `.env` is explicitly ignored in `.gitignore`. Only `.env.example` with safe placeholder tokens is committed.
- **Sanitized Logging:** Error handlers strip sensitive authorization strings and API keys from console logs and UI banners.

---

## ⚖️ Trade-offs and Limitations

- **Local CPU Embeddings:** `all-MiniLM-L6-v2` is fast and lightweight, but domain-specific complex jargon (e.g. medical/legal) may benefit from specialized fine-tuning or larger models (e.g., `bge-large-en-v1.5`).
- **Local FAISS Index:** FAISS `IndexFlatIP` provides exact nearest-neighbor search, which is optimal for thousands of chunks. Scaling to millions of documents would require an approximate index (`IVFFlat` or `HNSW`) or a distributed vector DB (Qdrant/Milvus).
- **PDF Table Parsing:** Basic PDF text extraction handles standard formatted tables well, but complex multi-column or borderless tables may require dedicated table parsers (such as `pdfplumber` or OCR).

---

## 🔮 Future Enhancements

1. **Hybrid Search:** Combine BM25 keyword matching with dense vector retrieval using Reciprocal Rank Fusion (RRF).
2. **Cross-Encoder Re-ranking:** Re-rank top-20 retrieved candidates using a cross-encoder (e.g. `ms-marco-MiniLM-L-6-v2`) before sending top-4 to the LLM.
3. **Conversational Memory:** Add multi-turn dialogue memory with query reformulation.

---

## 🤖 AI Assistant Disclosure

In accordance with assignment guidelines, this project was designed and developed with the assistance of **Antigravity AI Assistant** (Google DeepMind Agentic Coding AI) for architectural planning, code modularization, prompt engineering, and test suite generation.
# Document-RAG
