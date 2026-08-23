"""
Unit tests for Semantic Retriever.
"""

import numpy as np
from src.chunking import Chunk
from src.vector_store import FaissVectorStore
from src.retriever import Retriever


class MockEmbeddingManager:
    embedding_dim = 4

    def embed_query(self, query: str) -> np.ndarray:
        if "alpha" in query.lower():
            return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
        return np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)


def test_retriever_search_and_threshold(tmp_path):
    vec_store = FaissVectorStore(index_dir=tmp_path, dimension=4)
    vecs = np.array([
        [1.0, 0.0, 0.0, 0.0],  # Alpha chunk
        [0.0, 1.0, 0.0, 0.0],  # Beta chunk
    ], dtype=np.float32)

    chunks = [
        Chunk(chunk_id="c1", document_name="Doc1.pdf", page_number=1, chunk_index=0, text="Alpha details"),
        Chunk(chunk_id="c2", document_name="Doc2.pdf", page_number=5, chunk_index=0, text="Beta details"),
    ]
    vec_store.build(vecs, chunks)

    mock_emb = MockEmbeddingManager()
    retriever = Retriever(
        embedding_manager=mock_emb,
        vector_store=vec_store,
        top_k=2,
        similarity_threshold=0.5,
    )

    # Query matching Alpha
    res = retriever.retrieve("Tell me about alpha")
    assert res.has_sufficient_context is True
    assert len(res.top_chunks) == 1
    assert res.top_chunks[0].chunk_id == "c1"

    # Query with no close match
    res_unrelated = retriever.retrieve("Unrelated topic gamma")
    assert res_unrelated.has_sufficient_context is False
    assert len(res_unrelated.top_chunks) == 0
