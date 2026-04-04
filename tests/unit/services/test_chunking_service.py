import pytest

from rag_studienberater.application.services import ChunkingService
from rag_studienberater.domain.models import Document, Page


class TestChunkingServiceChunkDocument:

    def test_creates_one_chunk_per_splitter_result(self, stub_text_splitter):
        stub_text_splitter._chunks = ["Teil A", "Teil B"]
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="test.pdf", source="test.pdf", pages=[
            Page(text="Seiteninhalt", page_number=1),
        ])
        chunks = svc.chunk_document(doc)
        assert len(chunks) == 2

    def test_chunk_id_format_is_source_page_index(self, stub_text_splitter):
        stub_text_splitter._chunks = ["Inhalt"]
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="doc.pdf", source="dokument.pdf", pages=[
            Page(text="Text", page_number=2),
        ])
        chunks = svc.chunk_document(doc)
        assert chunks[0].chunk_id == "dokument.pdf:2:0"

    def test_chunk_id_index_increments_per_page(self, stub_text_splitter):
        stub_text_splitter._chunks = ["a", "b"]
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="doc.pdf", source="doc.pdf", pages=[
            Page(text="Seite", page_number=1),
        ])
        chunks = svc.chunk_document(doc)
        assert chunks[0].chunk_id == "doc.pdf:1:0"
        assert chunks[1].chunk_id == "doc.pdf:1:1"

    def test_chunk_preserves_source(self, stub_text_splitter):
        stub_text_splitter._chunks = ["x"]
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="test.pdf", source="meine_quelle.pdf", pages=[
            Page(text="Text", page_number=1),
        ])
        chunks = svc.chunk_document(doc)
        assert chunks[0].source == "meine_quelle.pdf"

    def test_chunk_preserves_page_number(self, stub_text_splitter):
        stub_text_splitter._chunks = ["x"]
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="test.pdf", source="test.pdf", pages=[
            Page(text="Text", page_number=5),
        ])
        chunks = svc.chunk_document(doc)
        assert chunks[0].page == 5

    def test_multiple_pages_accumulate_chunks(self, stub_text_splitter):
        stub_text_splitter._chunks = ["a", "b"]
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="test.pdf", source="doc.pdf", pages=[
            Page(text="Seite 1", page_number=1),
            Page(text="Seite 2", page_number=2),
        ])
        chunks = svc.chunk_document(doc)
        # 2 Seiten × 2 Chunks = 4
        assert len(chunks) == 4

    def test_splitter_returning_empty_list_produces_no_chunks(self, stub_text_splitter):
        stub_text_splitter._chunks = []
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="leer.pdf", source="leer.pdf", pages=[
            Page(text="", page_number=1),
        ])
        chunks = svc.chunk_document(doc)
        assert chunks == []

    def test_document_with_no_pages_returns_empty(self, stub_text_splitter):
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="test.pdf", source="test.pdf", pages=[])
        chunks = svc.chunk_document(doc)
        assert chunks == []

    def test_chunk_text_matches_splitter_output(self, stub_text_splitter):
        stub_text_splitter._chunks = ["Erster Teil", "Zweiter Teil"]
        svc = ChunkingService(text_splitter=stub_text_splitter)
        doc = Document(name="test.pdf", source="test.pdf", pages=[
            Page(text="Irgendwas", page_number=1),
        ])
        chunks = svc.chunk_document(doc)
        assert chunks[0].text == "Erster Teil"
        assert chunks[1].text == "Zweiter Teil"
