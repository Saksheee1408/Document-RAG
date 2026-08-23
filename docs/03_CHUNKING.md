# Milestone 3 — Chunking

## Goal

Split extracted text into retrieval-friendly chunks.

## Recommended starting strategy

Use structure-aware splitting:

1. Preserve page boundaries where practical.
2. Prefer headings/sections.
3. Split by paragraphs.
4. Split oversized paragraphs further.
5. Keep related information together.
6. Add overlap between neighboring chunks.

## Starting parameters

Use as initial values:

- target size: approximately 500–800 tokens
- overlap: approximately 75–150 tokens

These are starting points. Evaluate and adjust if retrieval results justify it.

## Every chunk must contain

- unique chunk ID
- document name
- page number
- chunk text
- chunk order/index
- optional section/heading

## Important reasoning

The README must explain:

- why the chosen chunk size was selected
- why overlap is needed
- how oversized content is split
- how page boundaries are handled

## Acceptance criteria

- Chunks are generated for all documents.
- Chunk metadata is preserved.
- Chunking is deterministic.
- No meaningful text is silently discarded.
- A reviewer can inspect chunks and understand the boundaries.

## Tests

Test:

- chunk creation
- metadata preservation
- overlap
- oversized text handling
