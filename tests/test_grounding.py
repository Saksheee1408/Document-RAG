"""
Unit tests for Grounding & Unanswerable Questions handling.
"""

from unittest.mock import MagicMock
from src.chunking import Chunk
from src.llm import GroqLLM, UNANSWERABLE_RESPONSE


def test_llm_insufficient_context_fallback():
    llm = GroqLLM(api_key="mock_key")
    res = llm.generate_answer(
        query="What is Quantum Teleportation?",
        chunks=[],
        has_sufficient_context=False,
    )
    assert res["answer"] == UNANSWERABLE_RESPONSE
    assert res["is_grounded"] is True


def test_llm_answerable_question_mocked():
    llm = GroqLLM(api_key="mock_key")

    mock_chat = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "Employees receive 20 days of annual leave."
    mock_chat.completions.create.return_value.choices = [mock_choice]
    llm._client = MagicMock(chat=mock_chat)

    sample_chunks = [
        Chunk(
            chunk_id="c1",
            document_name="Employee_Handbook.pdf",
            page_number=4,
            chunk_index=0,
            text="Employees receive 20 days of paid annual leave per year.",
        )
    ]

    res = llm.generate_answer(
        query="How many annual leave days do employees get?",
        chunks=sample_chunks,
        has_sufficient_context=True,
    )

    assert "20 days" in res["answer"]
    assert res["is_grounded"] is True
