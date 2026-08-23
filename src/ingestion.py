"""
PDF Ingestion Module.
Responsible for finding, reading, and extracting clean text from PDF documents
while preserving document names and page numbers.
"""

import os
import re
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from pypdf import PdfReader

logger = logging.getLogger("doc_rag.ingestion")


@dataclass
class ExtractedPage:
    """Dataclass holding extracted text and metadata for a single PDF page."""

    document_name: str
    page_number: int  # 1-indexed
    text: str
    section: Optional[str] = None


class PDFIngestor:
    """PDF text extractor with metadata preservation and error resilience."""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)

    def find_pdf_files(self) -> List[Path]:
        """Find all PDF files in the configured data directory."""
        if not self.data_dir.exists():
            logger.warning(f"Data directory does not exist: {self.data_dir}")
            return []

        pdf_files = sorted(list(self.data_dir.glob("*.pdf")) + list(self.data_dir.glob("*.PDF")))
        logger.info(f"Found {len(pdf_files)} PDF file(s) in {self.data_dir}")
        return pdf_files

    @staticmethod
    def clean_text(text: str) -> str:
        """Normalize extracted text by stripping null bytes, fixing whitespaces, etc."""
        if not text:
            return ""
        # Remove null characters
        text = text.replace("\x00", " ")
        # Replace multiple spaces/tabs with single space while retaining line breaks
        text = re.sub(r"[ \t]+", " ", text)
        # Normalize excessive newlines (more than 2 to 2)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def extract_page(self, pdf_path: Path, page_num: int, page_obj) -> Optional[ExtractedPage]:
        """Extract text from a single pypdf Page object."""
        try:
            raw_text = page_obj.extract_text() or ""
            cleaned = self.clean_text(raw_text)
            if not cleaned:
                logger.warning(f"Page {page_num} of {pdf_path.name} yielded no extractable text.")

            return ExtractedPage(
                document_name=pdf_path.name,
                page_number=page_num,
                text=cleaned,
            )
        except Exception as e:
            logger.error(f"Error extracting text from page {page_num} of {pdf_path.name}: {e}")
            return ExtractedPage(
                document_name=pdf_path.name,
                page_number=page_num,
                text="",
            )

    def extract_document(self, pdf_path: Path) -> List[ExtractedPage]:
        """Process a single PDF document page by page."""
        extracted_pages = []
        try:
            reader = PdfReader(str(pdf_path))
            total_pages = len(reader.pages)
            logger.info(f"Processing '{pdf_path.name}' ({total_pages} pages)...")

            for idx, page in enumerate(reader.pages):
                page_num = idx + 1  # 1-indexed
                page_data = self.extract_page(pdf_path, page_num, page)
                if page_data:
                    extracted_pages.append(page_data)

        except Exception as e:
            logger.error(f"Failed to open or process PDF file '{pdf_path.name}': {e}")

        return extracted_pages

    def ingest_all(self) -> List[ExtractedPage]:
        """Ingest all PDFs in the data directory and return extracted pages."""
        pdf_files = self.find_pdf_files()
        if not pdf_files:
            logger.warning("No PDF files found to ingest.")
            return []

        all_pages = []
        for pdf_path in pdf_files:
            pages = self.extract_document(pdf_path)
            all_pages.extend(pages)

        logger.info(f"Ingestion complete. Total pages extracted: {len(all_pages)}")
        return all_pages
