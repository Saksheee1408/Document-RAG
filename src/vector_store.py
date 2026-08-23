"""
FAISS Vector Store Module.
Manages building, saving, loading, and searching FAISS vector indices
along with chunk metadata persistence.
"""

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import faiss

from src.chunking import Chunk

logger = logging.getLogger("doc_rag.vector_store")


class FaissVectorStore:
    """FAISS Vector Store with Metadata Storage."""

    INDEX_FILENAME = "index.faiss"
    METADATA_FILENAME = "metadata.json"

    def __init__(self, index_dir: Path, dimension: int = 384):
        self.index_dir = Path(index_dir)
        self.dimension = dimension
        self.index: Optional[faiss.IndexFlatIP] = None
        self.metadata: List[Dict[str, Any]] = []

    def build(self, embeddings: np.ndarray, chunks: List[Chunk]):
        """Build FAISS IndexFlatIP (Cosine Similarity) from embeddings and chunks."""
        if len(embeddings) != len(chunks):
            raise ValueError(
                f"Count mismatch: {len(embeddings)} embeddings vs {len(chunks)} chunks."
            )

        if len(embeddings) > 0:
            if embeddings.shape[1] != self.dimension:
                self.dimension = embeddings.shape[1]

        # Use IndexFlatIP for normalized vectors (cosine similarity)
        self.index = faiss.IndexFlatIP(self.dimension)
        if len(embeddings) > 0:
            self.index.add(embeddings.astype(np.float32))

        self.metadata = [asdict(chunk) for chunk in chunks]
        logger.info(f"Built FAISS index with {self.index.ntotal} vectors.")

    def save(self):
        """Save FAISS index and metadata to index_dir."""
        if self.index is None:
            raise RuntimeError("Cannot save an uninitialized FAISS index.")

        self.index_dir.mkdir(parents=True, exist_ok=True)
        index_path = self.index_dir / self.INDEX_FILENAME
        metadata_path = self.index_dir / self.METADATA_FILENAME

        faiss.write_index(self.index, str(index_path))

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved FAISS index and metadata to '{self.index_dir}'")

    def load(self) -> bool:
        """Load FAISS index and metadata from index_dir."""
        index_path = self.index_dir / self.INDEX_FILENAME
        metadata_path = self.index_dir / self.METADATA_FILENAME

        if not index_path.exists() or not metadata_path.exists():
            logger.warning(f"Index or metadata file missing in '{self.index_dir}'")
            return False

        try:
            self.index = faiss.read_index(str(index_path))
            with open(metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

            self.dimension = self.index.d
            logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors from '{self.index_dir}'")
            return True
        except Exception as e:
            logger.error(f"Error loading vector store from '{self.index_dir}': {e}")
            raise RuntimeError(f"Corrupted or invalid FAISS index in '{self.index_dir}': {e}")

    def search(self, query_vector: np.ndarray, top_k: int = 4) -> List[Tuple[Chunk, float]]:
        """
        Search for top_k most similar vectors.
        Returns list of (Chunk, similarity_score) tuples.
        """
        if self.index is None or self.index.ntotal == 0:
            logger.warning("FAISS index is empty or uninitialized.")
            return []

        # Reshape to 2D matrix if 1D
        if query_vector.ndim == 1:
            query_vector = np.expand_dims(query_vector, axis=0)

        query_vector = query_vector.astype(np.float32)
        k = min(top_k, self.index.ntotal)

        # FAISS search
        scores, indices = self.index.search(query_vector, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue

            meta = self.metadata[idx]
            chunk = Chunk(
                chunk_id=meta["chunk_id"],
                document_name=meta["document_name"],
                page_number=meta["page_number"],
                chunk_index=meta["chunk_index"],
                text=meta["text"],
                section=meta.get("section"),
                token_count=meta.get("token_count", 0),
            )
            results.append((chunk, float(score)))

        return results
