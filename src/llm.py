"""
Groq LLM Integration Module.
Constructs grounded prompts, queries Groq API, and handles fallbacks & errors.
"""

import logging
from typing import List, Dict, Any, Optional
from src.chunking import Chunk

logger = logging.getLogger("doc_rag.llm")

# Standardized fallback message for unanswerable questions
UNANSWERABLE_RESPONSE = "The answer is not available in the provided documents."


class GroqLLM:
    """Groq API client wrapper with strict grounding prompts."""

    SYSTEM_PROMPT = (
        "You are an accurate, honest AI assistant answering questions based strictly on the provided document excerpts.\n"
        "Rules:\n"
        "1. Answer ONLY using the facts explicitly stated in the context provided below.\n"
        "2. Do NOT use outside knowledge or speculate.\n"
        "3. Do NOT fabricate citations, page numbers, or details not present in the context.\n"
        "4. If the context does NOT contain enough information to answer the question, reply EXACTLY with:\n"
        f"   \"{UNANSWERABLE_RESPONSE}\"\n"
        "5. Keep the answer direct, clear, and concise."
    )

    def __init__(self, api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model_name = model_name
        self._client = None

    @property
    def client(self):
        """Lazy initialization of Groq Client."""
        if self._client is None:
            if not self.api_key or self.api_key.startswith("your_"):
                raise ValueError(
                    "Groq API Key is not configured. Please set GROQ_API_KEY in your .env file."
                )
            try:
                from groq import Groq
                self._client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                raise RuntimeError("Could not initialize Groq LLM client.") from e
        return self._client

    @staticmethod
    def format_context(chunks: List[Chunk]) -> str:
        """Format retrieved chunks into a prompt context block."""
        if not chunks:
            return "No relevant context found."

        context_blocks = []
        for idx, chunk in enumerate(chunks, 1):
            block = (
                f"--- Excerpt [{idx}] ---\n"
                f"Document: {chunk.document_name}\n"
                f"Page: {chunk.page_number}\n"
                f"Content: {chunk.text.strip()}\n"
            )
            context_blocks.append(block)

        return "\n".join(context_blocks)

    DEFAULT_FALLBACK_MODELS = [
        "groq/compound-mini",
        "groq/compound",
        "qwen/qwen3.6-27b",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "allam-2-7b",
        "llama-3.3-70b-versatile",
    ]

    def generate_answer(
        self,
        query: str,
        chunks: List[Chunk],
        has_sufficient_context: bool = True,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Generate a grounded answer using Groq API.
        If context is insufficient, returns fallback immediately without calling API.
        If model is 404/not found, automatically retries with alternative supported Groq models.
        """
        if not query or not query.strip():
            return {
                "answer": "Question cannot be empty.",
                "is_grounded": False,
                "error": "Empty query",
            }

        # Safeguard: if retrieval indicates insufficient context, short-circuit
        if not has_sufficient_context or not chunks:
            logger.info("Insufficient context for query; returning unanswerable fallback.")
            return {
                "answer": UNANSWERABLE_RESPONSE,
                "is_grounded": True,
                "error": None,
            }

        formatted_context = self.format_context(chunks)
        user_prompt = (
            f"Context:\n{formatted_context}\n\n"
            f"Question: {query}\n\n"
            "Answer:"
        )

        # Build list of models to try (specified model first, followed by fallbacks)
        models_to_try = [self.model_name] + [
            m for m in self.DEFAULT_FALLBACK_MODELS if m != self.model_name
        ]

        last_error = None
        for candidate_model in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=candidate_model,
                    messages=[
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                    max_tokens=1024,
                )

                raw_answer = response.choices[0].message.content.strip()
                if not raw_answer:
                    return {
                        "answer": UNANSWERABLE_RESPONSE,
                        "is_grounded": True,
                        "error": None,
                    }

                if candidate_model != self.model_name:
                    logger.info(f"Fallback model succeeded: {candidate_model}")

                return {
                    "answer": raw_answer,
                    "is_grounded": True,
                    "model_used": candidate_model,
                    "error": None,
                }

            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                if any(k in error_msg.lower() for k in ["model_not_found", "model_decommissioned", "404", "decommissioned"]):
                    logger.warning(
                        f"Model '{candidate_model}' unavailable on Groq API. Trying next fallback..."
                    )
                    continue
                else:
                    break

        # If all candidates failed or non-404 error occurred
        logger.error(f"Error calling Groq API: {last_error}")
        friendly_error = str(last_error)
        if any(k in friendly_error.lower() for k in ["model_not_found", "model_decommissioned", "decommissioned", "404"]):
            friendly_error = (
                "The selected LLM model is unavailable or decommissioned on Groq API. "
                "Please select an active model (such as 'groq/compound-mini' or 'qwen/qwen3.6-27b') from the Settings panel."
            )
        elif "api_key" in friendly_error.lower() or "401" in friendly_error:
            friendly_error = "Invalid or missing Groq API Key. Please set a valid GROQ_API_KEY in your .env file."
        elif "rate_limit" in friendly_error.lower() or "429" in friendly_error:
            friendly_error = "Groq API rate limit reached. Please wait a few moments before asking another question."

        return {
            "answer": friendly_error,
            "is_grounded": False,
            "error": friendly_error,
        }
