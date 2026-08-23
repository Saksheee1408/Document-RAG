# Milestone 15 — Final Review and Demo

## Goal

Verify the complete system and prepare the final demonstration.

## Final functional checklist

- [ ] All PDFs ingest successfully.
- [ ] Text extraction works.
- [ ] Page metadata survives.
- [ ] Chunking works.
- [ ] Chunking strategy is documented.
- [ ] Embeddings are generated.
- [ ] FAISS index is built.
- [ ] FAISS index can be loaded.
- [ ] Semantic retrieval works.
- [ ] Groq generates grounded answers.
- [ ] Sources are returned.
- [ ] Unanswerable questions are handled safely.
- [ ] Streamlit UI works.

## Engineering checklist

- [ ] Code is modular.
- [ ] Configuration is separated.
- [ ] API keys use environment variables.
- [ ] `.env` is ignored.
- [ ] `.env.example` exists.
- [ ] Errors are handled.
- [ ] Logs do not leak secrets.
- [ ] Tests pass.

## Documentation checklist

- [ ] README exists.
- [ ] Architecture explained.
- [ ] Chunking justified.
- [ ] Embedding model documented.
- [ ] FAISS choice documented.
- [ ] Groq integration documented.
- [ ] Setup instructions tested.
- [ ] Trade-offs documented.
- [ ] Limitations documented.
- [ ] AI assistant usage acknowledged.

## Demo sequence

1. Start the application.
2. Show the indexed PDF knowledge base.
3. Ask an easy factual question.
4. Show answer and source.
5. Ask a paraphrased question.
6. Show semantic retrieval.
7. Ask a table/specification question.
8. Ask an unanswerable question.
9. Show the safe "not available in the provided documents" behavior.
10. Briefly show README architecture and design decisions.

## Final rule

Prefer a focused, reliable implementation over unnecessary bonus features.
