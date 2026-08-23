"""
Unit tests for Text Chunking.
"""

from src.ingestion import ExtractedPage
from src.chunking import TextChunker, Chunk


def test_chunking_small_page():
    chunker = TextChunker(target_chunk_size=100, overlap=20)
    page = ExtractedPage(
        document_name="Test_Doc.pdf",
        page_number=1,
        text="This is a small page text for testing.",
    )

    chunks = chunker.chunk_page(page)
    assert len(chunks) == 1
    assert chunks[0].document_name == "Test_Doc.pdf"
    assert chunks[0].page_number == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].chunk_id == "Test_Doc.pdf_p1_c0"
    assert chunks[0].text == "This is a small page text for testing."


def test_chunking_large_page_with_overlap():
    chunker = TextChunker(target_chunk_size=10, overlap=3)
    long_text = " ".join([f"word{i}" for i in range(25)])
    page = ExtractedPage(
        document_name="Long_Doc.pdf",
        page_number=2,
        text=long_text,
    )

    chunks = chunker.chunk_page(page)
    assert len(chunks) > 1

    # Verify overlap between chunk 0 and chunk 1
    words_c0 = chunks[0].text.split()
    words_c1 = chunks[1].text.split()

    # The last 3 words of chunk 0 should equal the first 3 words of chunk 1
    assert words_c0[-3:] == words_c1[:3]


def test_chunk_pages():
    chunker = TextChunker(target_chunk_size=50, overlap=10)
    pages = [
        ExtractedPage(document_name="DocA.pdf", page_number=1, text="Sample content for page 1."),
        ExtractedPage(document_name="DocA.pdf", page_number=2, text="Sample content for page 2."),
    ]

    chunks = chunker.chunk_pages(pages)
    assert len(chunks) == 2
    assert chunks[0].chunk_id == "DocA.pdf_p1_c0"
    assert chunks[1].chunk_id == "DocA.pdf_p2_c0"
