# Milestone 12 — Automated Testing

## Goal

Demonstrate engineering quality and prevent regressions.

## Test areas

### Ingestion

Verify:

- PDF discovery
- page extraction
- metadata preservation
- failure handling

### Chunking

Verify:

- chunk creation
- approximate size bounds
- overlap
- metadata preservation

### Embeddings

Verify:

- embeddings generated
- consistent dimensions
- count equals chunk count

### FAISS

Verify:

- build
- save
- load
- search
- metadata mapping

### Retrieval

Verify:

- known questions retrieve expected documents
- paraphrases retrieve relevant content

### Grounding

Verify:

- supported questions have supporting context
- unsupported questions do not produce fabricated answers

### Configuration

Verify:

- missing Groq key is handled
- invalid configuration gives useful errors

## Acceptance criteria

Core tests pass from a fresh environment.

Tests that require Groq should use mocks unless an explicit integration-test mode is configured.
