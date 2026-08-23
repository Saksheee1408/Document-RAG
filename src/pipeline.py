"""
RAG Pipeline Coordinator.
Orchestrates end-to-end PDF indexing and retrieval-augmented question answering.
"""

import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from src.config import AppConfig
from src.ingestion import PDFIngestor, ExtractedPage
from src.chunking import TextChunker, Chunk
from src.embeddings import EmbeddingManager
from src.vector_store import FaissVectorStore
from src.retriever import Retriever, RetrievalResponse
from src.llm import GroqLLM, UNANSWERABLE_RESPONSE

logger = logging.getLogger("doc_rag.pipeline")


@dataclass
class SourceAttribution:
    """Dataclass representing source attribution for a retrieved chunk."""

    document_name: str
    page_number: int
    chunk_id: str
    score: float
    text_preview: str


@dataclass
class RAGQueryResponse:
    """Complete RAG query response object."""

    query: str
    answer: str
    sources: List[SourceAttribution]
    has_sufficient_context: bool
    error: Optional[str] = None


class RAGPipeline:
    """Master pipeline orchestrator for Doc-RAG."""

    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig.load_from_env()

        self.ingestor = PDFIngestor(data_dir=self.config.data_dir)
        self.chunker = TextChunker(target_chunk_size=600, overlap=100)
        self.embedding_manager = EmbeddingManager(model_name=self.config.embedding_model)
        self.vector_store = FaissVectorStore(
            index_dir=self.config.index_dir,
            dimension=self.embedding_manager.embedding_dim,
        )
        self.retriever = Retriever(
            embedding_manager=self.embedding_manager,
            vector_store=self.vector_store,
            top_k=self.config.top_k,
            similarity_threshold=self.config.similarity_threshold,
        )
        self.llm = GroqLLM(
            api_key=self.config.groq_api_key,
            model_name=self.config.groq_model,
        )

    def is_indexed(self) -> bool:
        """Check if vector store index is loaded or ready."""
        if self.vector_store.index is not None and self.vector_store.index.ntotal > 0:
            return True
        return self.vector_store.load()

    def build_index(self, force_rebuild: bool = False) -> Dict[str, Any]:
        """Ingest PDFs, generate chunks & embeddings, and build FAISS index."""
        if not force_rebuild and self.vector_store.load():
            logger.info("Existing index loaded successfully. Skipping build.")
            return {
                "status": "loaded",
                "chunks": len(self.vector_store.metadata),
                "vectors": self.vector_store.index.ntotal,
            }

        logger.info("Building new index from scratch...")
        pages: List[ExtractedPage] = self.ingestor.ingest_all()
        if not pages:
            logger.warning("No PDF pages were extracted during ingestion.")
            return {"status": "empty", "chunks": 0, "vectors": 0}

        chunks: List[Chunk] = self.chunker.chunk_pages(pages)
        if not chunks:
            logger.warning("No chunks generated from extracted pages.")
            return {"status": "empty", "chunks": 0, "vectors": 0}

        embeddings = self.embedding_manager.embed_chunks(chunks)
        self.vector_store.build(embeddings, chunks)
        self.vector_store.save()

        logger.info("Index build and saving complete.")
        return {
            "status": "built",
            "chunks": len(chunks),
            "vectors": self.vector_store.index.ntotal,
        }

    def answer_question(self, query: str) -> RAGQueryResponse:
        """Process a user question through retrieval and LLM generation."""
        if not self.is_indexed():
            # Try to build index automatically if missing
            build_res = self.build_index()
            if build_res["status"] == "empty":
                return RAGQueryResponse(
                    query=query,
                    answer="No document knowledge base available. Please add PDFs to the files directory.",
                    sources=[],
                    has_sufficient_context=False,
                    error="Empty index",
                )

        # Retrieve relevant chunks
        retrieval_res: RetrievalResponse = self.retriever.retrieve(query)

        # Build source attributions
        sources = []
        # Filter chunks to present as sources
        active_results = [r for r in retrieval_res.results if r.is_above_threshold]
        for res in active_results:
            preview = res.chunk.text[:200] + "..." if len(res.chunk.text) > 200 else res.chunk.text
            sources.append(
                SourceAttribution(
                    document_name=res.chunk.document_name,
                    page_number=res.chunk.page_number,
                    chunk_id=res.chunk.chunk_id,
                    score=round(res.score, 4),
                    text_preview=preview,
                )
            )

        # Call Groq LLM
        retrieved_chunks = [r.chunk for r in active_results]
        llm_response = self.llm.generate_answer(
            query=query,
            chunks=retrieved_chunks,
            has_sufficient_context=retrieval_res.has_sufficient_context,
        )

        answer = llm_response["answer"]

        # If answer is unanswerable, clear sources to satisfy requirement (Milestone 9)
        if UNANSWERABLE_RESPONSE.lower() in answer.lower():
            sources = []

        return RAGQueryResponse(
            query=query,
            answer=answer,
            sources=sources,
            has_sufficient_context=retrieval_res.has_sufficient_context,
            error=llm_response.get("error"),
        )
