"""
Unit tests for FAISS vector store build, save, load, and query.
"""

import numpy as np
from src.chunking import Chunk
from src.vector_store import FaissVectorStore


def test_faiss_build_save_load_search(tmp_path):
    dim = 4
    store = FaissVectorStore(index_dir=tmp_path, dimension=dim)

    # Dummy normalized vectors
    vecs = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
    ], dtype=np.float32)

    chunks = [
        Chunk(chunk_id="c1", document_name="docA.pdf", page_number=1, chunk_index=0, text="Alpha topic"),
        Chunk(chunk_id="c2", document_name="docB.pdf", page_number=2, chunk_index=0, text="Beta topic"),
    ]

    # Build & Save
    store.build(vecs, chunks)
    store.save()

    # Load in fresh store instance
    new_store = FaissVectorStore(index_dir=tmp_path, dimension=dim)
    loaded = new_store.load()
    assert loaded is True
    assert new_store.index.ntotal == 2

    # Query matching vector 0
    query_vec = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
    results = new_store.search(query_vec, top_k=2)

    assert len(results) == 2
    top_chunk, score = results[0]
    assert top_chunk.chunk_id == "c1"
    assert top_chunk.document_name == "docA.pdf"
    assert top_chunk.page_number == 1
    assert abs(score - 1.0) < 1e-4
