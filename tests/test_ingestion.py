"""
Unit tests for PDF Ingestion.
"""

from pathlib import Path
from src.ingestion import PDFIngestor, ExtractedPage


def test_pdf_discovery(tmp_path):
    # Create sample dummy PDF files
    (tmp_path / "doc1.pdf").write_bytes(b"%PDF-1.4 dummy")
    (tmp_path / "doc2.PDF").write_bytes(b"%PDF-1.4 dummy")
    (tmp_path / "notes.txt").write_text("not a pdf")

    ingestor = PDFIngestor(data_dir=tmp_path)
    files = ingestor.find_pdf_files()

    assert len(files) == 2
    filenames = [f.name for f in files]
    assert "doc1.pdf" in filenames
    assert "doc2.PDF" in filenames


def test_clean_text():
    raw_text = "Hello\x00 World!   This is   a \n\n\n test."
    cleaned = PDFIngestor.clean_text(raw_text)
    assert "\x00" not in cleaned
    assert "   " not in cleaned
    assert cleaned == "Hello World! This is a \n\n test."


def test_real_pdf_ingestion_preserves_metadata():
    files_dir = Path("files")
    if not files_dir.exists():
        return

    ingestor = PDFIngestor(data_dir=files_dir)
    pdf_files = ingestor.find_pdf_files()
    assert len(pdf_files) > 0, "No PDFs found in files directory"

    pages = ingestor.ingest_all()
    assert len(pages) > 0, "Ingestion produced no pages"

    first_page = pages[0]
    assert isinstance(first_page, ExtractedPage)
    assert first_page.document_name.endswith(".pdf")
    assert first_page.page_number >= 1
    assert isinstance(first_page.text, str)
