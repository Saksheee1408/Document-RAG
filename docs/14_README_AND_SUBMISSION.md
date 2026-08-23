# Milestone 14 — README and Submission

## Goal

Produce the documentation and deliverables required by the assignment.

## README must contain

### Project overview

What the application does.

### Architecture

PDF → extraction → chunking → embeddings → FAISS → retrieval → Groq → answer + sources.

### Technology choices

Explain:

- Python
- Streamlit
- sentence-transformers
- FAISS
- Groq
- PDF extraction approach

### Chunking

Explain:

- chunk size
- overlap
- splitting logic
- why these values were chosen

### Retrieval

Explain:

- embedding model
- vector DB
- top-k
- relevance threshold if used
- known limitations

### LLM

Explain:

- Groq integration
- prompt/grounding rules
- unanswerable behavior
- source handling

### Setup

A reviewer should be able to:

1. Clone repository.
2. Create environment.
3. Install dependencies.
4. Configure `.env`.
5. Add PDFs.
6. Build index.
7. Start application.

The assignment expects a fresh setup to be runnable in under 10 minutes.

### Security

Document:

- no real API keys committed
- `.env` ignored
- `.env.example` provided

### Trade-offs and limitations

Be honest about:

- local embedding quality/speed
- FAISS being local rather than distributed
- PDF/table extraction limitations
- retrieval dependence on chunking and embeddings
- Groq external dependency/rate limits

### Future improvements

Possible extras:

- hybrid search
- reranking
- OCR
- better table extraction
- evaluation metrics
- conversation history
- production vector database
- caching
- observability
- authentication
- streaming

## Submission deliverables

- Git repository
- README.md
- working demo
- 10+ sample Q&A examples
- at least 2 unanswerable examples

## Assignment-specific requirement

Acknowledge use of AI coding assistants such as ChatGPT/Copilot in the README, as requested by the assignment.
