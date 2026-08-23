# Milestone 4 — Embeddings

## Goal

Convert each chunk into a numerical vector for semantic search.

## Technology

Use a local `sentence-transformers` embedding model.

The embedding model should be configurable.

## AI IDE instructions

1. Load the embedding model once.
2. Generate embeddings for all chunks.
3. Preserve chunk-to-vector mapping.
4. Use batching where practical.
5. Record the model name/configuration.
6. Avoid unnecessary re-embedding when the existing index is still valid.

## Critical rule

The vector position must always map back to the correct chunk metadata.

Never allow:

vector → wrong chunk → wrong source

## Acceptance criteria

- Every chunk has an embedding.
- All embeddings have the same dimension.
- Number of embeddings matches number of chunks.
- Model choice is documented.
- Rebuilding the index produces a consistent mapping.

## Tests

Verify:

- embedding generation
- dimensions
- count matching
- chunk/vector mapping
