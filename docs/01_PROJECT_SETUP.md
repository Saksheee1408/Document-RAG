# Milestone 1 — Project Setup

## Goal

Create a clean, reproducible Python project before implementing the RAG pipeline.

## AI IDE instructions

1. Initialize the repository.
2. Create a modular project structure.
3. Configure the Python environment.
4. Add dependency management.
5. Add `.gitignore`.
6. Add `.env.example`.
7. Add configuration handling.
8. Add logging.
9. Create directories for raw PDFs, processed data, and vector storage.
10. Create an initial README.

## Required configuration

At minimum support:

- `GROQ_API_KEY`
- configurable Groq model name
- embedding model configuration
- retrieval parameters such as top-k

Never hard-code secrets.

## Expected structure

Create clear modules for:

- ingestion
- chunking
- embeddings
- vector store
- retrieval
- LLM
- pipeline
- configuration
- UI
- tests

## Acceptance criteria

- Fresh environment can install dependencies.
- Application starts without hard-coded secrets.
- Missing Groq API key produces a clear configuration error.
- `.env` is ignored by Git.
- `.env.example` contains placeholders only.
- Repository structure is clean and understandable.

## Before moving on

Run the project's basic validation/tests and fix all setup errors.
