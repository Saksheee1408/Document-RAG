# RAG Document Q&A — AI IDE Instructions

This folder is intentionally split into separate milestone documents. Give the AI IDE one milestone at a time.

## Project goal

Build a complete RAG-based document Q&A system for the provided PDF knowledge base.

Required core flow:

PDFs → text extraction → chunking → embeddings → FAISS → retrieval → Groq LLM → grounded answer + sources.

## Fixed technology direction

- Python
- Streamlit for reviewer UI
- FAISS for vector search
- sentence-transformers for embeddings
- Groq API for LLM generation
- `.env` for secrets
- pytest for testing

## Important rules

- Implement milestones sequentially.
- Do not move ahead while a core acceptance criterion is broken.
- Keep the code modular and simple.
- Never commit a real API key.
- Preserve document name, page number, and chunk metadata.
- Never fabricate sources.
- If the documents do not contain the answer, the system must say so rather than hallucinate.
- Run tests after each milestone.
- Update README/design documentation as implementation decisions are made.

## How to use this package

Start with `01_PROJECT_SETUP.md`.

After completing it, move to `02_PDF_INGESTION.md`, then continue in numerical order.
