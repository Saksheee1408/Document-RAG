# Milestone 13 — Error Handling and Edge Cases

## Goal

Make the application robust enough for reviewer use.

Handle:

- empty question
- very long question
- no PDFs
- corrupted PDF
- empty PDF
- page with no extractable text
- missing FAISS index
- corrupted FAISS index
- missing metadata
- no relevant results
- Groq failure
- Groq timeout
- Groq rate limit
- missing environment variables
- malformed LLM response
- question outside document knowledge

## Behavior

Normal users should receive clear, useful messages.

Do not expose raw stack traces or secrets in the UI.

Developer logs may contain technical details, but never API keys.

## Acceptance criteria

Each major failure mode has a predictable user-facing behavior and, where practical, a test.
