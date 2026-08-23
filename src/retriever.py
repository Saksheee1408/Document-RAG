"""
Semantic Retrieval Module.
Handles converting user queries into vectors, performing similarity searches,
and applying threshold filtering to avoid low-relevance matches.
"""

import logging
from dataclasses import dataclass
from typing import List, Tuple
from src.embeddings import EmbeddingManager
from src.vector_store import FaissVectorStore
from src.chunking import Chunk

logger = logging.getLogger("doc_rag.retriever")


@dataclass
class RetrievedSearchResult:
    """Single search result item with chunk metadata and similarity score."""

    chunk: Chunk
    score: float
    is_above_threshold: bool


@dataclass
class RetrievalResponse:
    """Aggregate search response."""

    query: str
    results: List[RetrievedSearchResult]
    has_sufficient_context: bool

    @property
    def top_chunks(self) -> List[Chunk]:
        return [r.chunk for r in self.results if r.is_above_threshold]


class Retriever:
    """Semantic retriever using embedding manager and FAISS vector store."""

    def __init__(
        self,
        embedding_manager: EmbeddingManager,
        vector_store: FaissVectorStore,
        top_k: int = 4,
        similarity_threshold: float = 0.35,
    ):
        self.embedding_manager = embedding_manager
        self.vector_store = vector_store
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(self, query: str, top_k: int = None, threshold: float = None) -> RetrievalResponse:
        """Embed user query, search vector store, and filter results by threshold."""
        if not query or not query.strip():
            logger.warning("Empty query received for retrieval.")
            return RetrievalResponse(query=query, results=[], has_sufficient_context=False)

        k = top_k if top_k is not None else self.top_k
        thresh = threshold if threshold is not None else self.similarity_threshold

        query_vector = self.embedding_manager.embed_query(query)
        raw_results: List[Tuple[Chunk, float]] = self.vector_store.search(query_vector, top_k=k)

        formatted_results = []
        above_threshold_count = 0

        for chunk, score in raw_results:
            is_above = score >= thresh
            if is_above:
                above_threshold_count += 1
            formatted_results.append(
                RetrievedSearchResult(
                    chunk=chunk,
                    score=score,
                    is_above_threshold=is_above,
                )
            )

        has_context = above_threshold_count > 0
        logger.info(
            f"Retrieval for '{query[:40]}...': found {len(formatted_results)} chunk(s), "
            f"{above_threshold_count} above similarity threshold {thresh}."
        )

        return RetrievalResponse(
            query=query,
            results=formatted_results,
            has_sufficient_context=has_context,
        )
