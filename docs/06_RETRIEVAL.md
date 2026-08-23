# Milestone 6 — Semantic Retrieval

## Goal

Turn a user's question into the most relevant document chunks.

## Pipeline

Question → query embedding → FAISS search → top-k chunks → optional relevance filtering.

## AI IDE instructions

The retrieval layer must:

- use the same embedding model as document indexing
- embed the question
- search FAISS
- return configurable top-k results
- preserve metadata
- retain similarity/distance information internally
- avoid blindly treating every returned result as relevant

## Evaluation questions

Test:

- straightforward factual questions
- paraphrased questions
- section-related questions
- table/specification questions
- questions needing multiple chunks
- questions not answered by the documents

## Acceptance criteria

For known questions, the expected document/page should appear among retrieved results.

## Tests

Create retrieval tests using the supplied knowledge base.

Do not evaluate only one happy-path question.
