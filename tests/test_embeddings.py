"""
Unit tests for Embeddings generation.
"""

import numpy as np
from src.chunking import Chunk
from src.embeddings import EmbeddingManager


def test_embedding_dimension_and_count():
    manager = EmbeddingManager(model_name="all-MiniLM-L6-v2")
    texts = ["Hello world", "RAG pipeline test"]

    embeddings = manager.embed_texts(texts)
    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] == 384
    assert embeddings.dtype == np.float32


def test_chunk_embedding_mapping():
    manager = EmbeddingManager(model_name="all-MiniLM-L6-v2")
    chunks = [
        Chunk(chunk_id="c1", document_name="d1.pdf", page_number=1, chunk_index=0, text="First chunk text"),
        Chunk(chunk_id="c2", document_name="d1.pdf", page_number=1, chunk_index=1, text="Second chunk text"),
    ]

    embeddings = manager.embed_chunks(chunks)
    assert len(embeddings) == len(chunks)


def test_query_embedding():
    manager = EmbeddingManager(model_name="all-MiniLM-L6-v2")
    q_vec = manager.embed_query("What is the refund policy?")
    assert q_vec.ndim == 1
    assert q_vec.shape[0] == 384
