# Milestone 7 — Groq LLM Integration

## Goal

Use the Groq API to generate the final answer from retrieved document context.

## Important principle

The LLM is not the knowledge source.

Retrieved document chunks are the knowledge source.

## Prompt requirements

The LLM instructions should clearly state:

1. Answer only from the supplied context.
2. Do not invent unsupported facts.
3. If the context does not contain enough information, say that the answer is not available in the provided documents.
4. Prefer concise, direct answers.
5. Do not invent citations or page numbers.

## Configuration

Use:

- `GROQ_API_KEY` from environment
- configurable Groq model name

Never place secrets in source code.

## Error handling

Handle:

- missing key
- timeout
- rate limit
- provider/API failure
- empty response
- malformed response

Do not expose secrets in logs or UI.

## Acceptance criteria

- A valid question produces a grounded answer.
- Groq API integration works.
- Provider errors are handled cleanly.
- API key is never shown.
- Model can be changed through configuration.

## Tests

Mock the Groq client for automated tests so tests do not require a real API call.
