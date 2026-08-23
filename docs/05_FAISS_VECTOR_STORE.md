# Milestone 5 — FAISS Vector Store

## Goal

Store embeddings and support semantic similarity search.

## Technology

Use FAISS as the local vector store.

## AI IDE instructions

Implement:

1. Index creation.
2. Adding chunk embeddings.
3. Persistent index saving.
4. Persistent metadata mapping.
5. Index loading.
6. Top-k similarity search.
7. Mapping search results back to document/page/chunk metadata.

## Critical requirement

A FAISS result is only useful if its vector ID can reliably map to:

- document name
- page number
- chunk ID
- chunk text

## Configuration

Make top-k configurable. Start around 4–6.

## Acceptance criteria

- Index builds successfully.
- Index persists to disk.
- Existing index can be loaded.
- Search returns relevant chunks with metadata.
- Missing/corrupt index produces a clear error.

## Tests

Test:

- build
- save
- load
- query
- metadata mapping
