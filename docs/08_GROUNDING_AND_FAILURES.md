# Milestone 8 — Grounding and Unanswerable Questions

## Goal

Prevent confident hallucinations.

This is a high-priority requirement because the assignment explicitly evaluates edge-case handling.

## Required behavior

### Answerable

Question → relevant chunks → Groq → answer + sources.

### Unanswerable

Question → insufficient relevant context → clear "not available in the provided documents" response.

Do not ask the LLM to invent an answer when retrieval has no adequate support.

## Recommended safeguards

Use a combination of:

- similarity/relevance threshold
- top-k retrieval
- grounding prompt
- explicit unanswerable handling
- source validation
- tests with deliberately unanswerable questions

Do not rely only on the prompt.

## Acceptance criteria

- At least two unanswerable questions are tested.
- The system does not confidently fabricate answers.
- Answers are supported by retrieved context.
- Sources correspond to actual retrieved chunks.

## Tests

Include questions about topics absent from the provided PDFs.
