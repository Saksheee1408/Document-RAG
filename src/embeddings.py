"""
Embeddings Module.
Wraps sentence-transformers to generate dense vector embeddings for document chunks and user queries.
"""

import logging
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from src.chunking import Chunk

logger = logging.getLogger("doc_rag.embeddings")


class EmbeddingManager:
    """Embedding generation using sentence-transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model: Union[SentenceTransformer, None] = None
        self._embedding_dim: Union[int, None] = None

    @property
    def model(self) -> SentenceTransformer:
        """Lazy-load the SentenceTransformer model."""
        if self._model is None:
            logger.info(f"Loading embedding model '{self.model_name}'...")
            self._model = SentenceTransformer(self.model_name)
            self._embedding_dim = self._model.get_embedding_dimension()
            logger.info(f"Loaded '{self.model_name}' with dimension {self._embedding_dim}.")
        return self._model

    @property
    def embedding_dim(self) -> int:
        """Get the dimensionality of the embedding vectors."""
        if self._embedding_dim is None:
            _ = self.model
        return self._embedding_dim

    def embed_texts(self, texts: List[str], batch_size: int = 32, normalize: bool = True) -> np.ndarray:
        """Generate normalized vector embeddings for a list of strings."""
        if not texts:
            return np.empty((0, self.embedding_dim), dtype=np.float32)

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
        )
        return embeddings.astype(np.float32)

    def embed_chunks(self, chunks: List[Chunk], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for a list of Chunk objects."""
        texts = [chunk.text for chunk in chunks]
        logger.info(f"Generating embeddings for {len(texts)} chunk(s)...")
        embeddings = self.embed_texts(texts, batch_size=batch_size, normalize=True)
        logger.info(f"Generated embeddings shape: {embeddings.shape}")
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """Generate a normalized 1D vector embedding for a query string."""
        if not query or not query.strip():
            raise ValueError("Query string cannot be empty.")
        embeddings = self.embed_texts([query], batch_size=1, normalize=True)
        return embeddings[0]
