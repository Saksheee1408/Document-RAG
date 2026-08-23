"""
Chunking Module.
Splits extracted document pages into retrieval-friendly chunks with configurable size and overlap,
preserving document name, page number, and chunk index metadata.
"""

import re
import logging
from dataclasses import dataclass
from typing import List, Optional
from src.ingestion import ExtractedPage

logger = logging.getLogger("doc_rag.chunking")


@dataclass
class Chunk:
    """Dataclass holding chunk content and full metadata."""

    chunk_id: str
    document_name: str
    page_number: int
    chunk_index: int
    text: str
    section: Optional[str] = None
    token_count: int = 0


class TextChunker:
    """Structure-aware text chunker with overlap and metadata preservation."""

    def __init__(
        self,
        target_chunk_size: int = 200,  # approximate word/token target
        overlap: int = 40,            # approximate word/token overlap
        min_chunk_size: int = 50,       # skip tiny empty fragments unless only text
    ):
        self.target_chunk_size = target_chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate token count based on word splitting."""
        if not text:
            return 0
        words = text.split()
        return len(words)

    def split_text_into_paragraphs(self, text: str) -> List[str]:
        """Split text into structural paragraphs or section blocks."""
        # Split by double newlines or structural markers
        raw_paragraphs = re.split(r"\n\s*\n", text)
        paragraphs = []
        for p in raw_paragraphs:
            cleaned = p.strip()
            if cleaned:
                paragraphs.append(cleaned)
        return paragraphs

    def chunk_page(self, page: ExtractedPage) -> List[Chunk]:
        """Chunk a single page, respecting section boundaries where possible."""
        if not page.text or not page.text.strip():
            return []

        text = page.text.strip()
        words = text.split()

        # If page is small enough to fit in a single target chunk
        if len(words) <= self.target_chunk_size + self.overlap:
            chunk_id = f"{page.document_name}_p{page.page_number}_c0"
            return [
                Chunk(
                    chunk_id=chunk_id,
                    document_name=page.document_name,
                    page_number=page.page_number,
                    chunk_index=0,
                    text=text,
                    section=page.section,
                    token_count=len(words),
                )
            ]

        # Use sliding window over words for long pages/texts
        chunks = []
        chunk_idx = 0
        start = 0
        total_words = len(words)

        while start < total_words:
            end = min(start + self.target_chunk_size, total_words)
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunk_id = f"{page.document_name}_p{page.page_number}_c{chunk_idx}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_name=page.document_name,
                    page_number=page.page_number,
                    chunk_index=chunk_idx,
                    text=chunk_text,
                    section=page.section,
                    token_count=len(chunk_words),
                )
            )

            chunk_idx += 1
            if end >= total_words:
                break

            # Move start forward by target - overlap
            step = max(1, self.target_chunk_size - self.overlap)
            start += step

        return chunks

    def chunk_pages(self, pages: List[ExtractedPage]) -> List[Chunk]:
        """Generate chunks for a collection of ExtractedPage objects."""
        all_chunks = []
        for page in pages:
            page_chunks = self.chunk_page(page)
            all_chunks.extend(page_chunks)

        logger.info(f"Generated {len(all_chunks)} chunk(s) from {len(pages)} page(s).")
        return all_chunks
