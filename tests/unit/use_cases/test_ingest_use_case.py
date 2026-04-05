# Imports
import pytest

from rag_studienberater.application.services import ChunkingService, TextCleanerService
from rag_studienberater.application.use_cases import IngestUseCase
from rag_studienberater.domain.models import Document, Page
from rag_studienberater.domain.ports import EmbeddingPort


# Create Use-Case
def make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
    return IngestUseCase(
        loader=stub_loader,
        text_cleaner_service=TextCleanerService(),
        chunking_service=ChunkingService(text_splitter=stub_text_splitter),
        embedder=stub_embedder,
        vector_store=stub_vector_store,
    )


class TestIngestUseCaseExecuteDocument:

    # Ensure source was passed correctly to the loader
    def test_calls_loader_with_source(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('mein_dokument.pdf')
        assert 'mein_dokument.pdf' in stub_loader.load_calls

    # Ensure chunks were saved correctly in the Vector-Store
    def test_stores_chunks_in_vector_store(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['Erster Chunk mit ausreichend Text.', 'Zweiter Chunk mit ausreichend Text.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        assert len(stub_vector_store.stored_chunks) == 2

    # Ensure chunk text was saved correctly as in the splitter
    def test_stored_chunks_match_texts(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['Erster Chunk mit ausreichend Text.', 'Zweiter Chunk mit ausreichend Text.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        texts = [c.text for c in stub_vector_store.stored_chunks]
        assert 'Erster Chunk mit ausreichend Text.' in texts
        assert 'Zweiter Chunk mit ausreichend Text.' in texts

    # Ensures there's one vector for one chunk
    def test_chunk_count_matches_vector_count(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['Chunk A mit ausreichend Text.', 'Chunk B mit ausreichend Text.', 'Chunk C mit ausreichend Text.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        assert len(stub_vector_store.stored_chunks) == len(stub_vector_store.stored_vectors)

    # Ensures text is cleaned before chunking
    def test_cleans_page_text_before_chunking(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, make_document):
        dirty_page = Page(text='  schmutziger   Text  ', page_number=1)
        stub_loader.document = make_document(pages=[dirty_page])
        stub_text_splitter._chunks = ['sauber']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        assert dirty_page.text == 'schmutziger Text'

    # Ensures empty chunks are not saved
    def test_empty_chunks_skips_vector_store(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = []
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        assert stub_vector_store.add_chunks_call_count == 0

    # Ensures each chunk is embedded individually
    def test_embedder_called_once_per_chunk(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['Alpha-Text mit ausreichend Inhalt.', 'Beta-Text mit ausreichend Inhalt.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        # Per-Chunk-Embedding: embed_documents wird einmal pro Chunk aufgerufen
        assert len(stub_embedder.embed_documents_calls) == 2
        assert stub_embedder.embed_documents_calls[0] == ['Alpha-Text mit ausreichend Inhalt.']
        assert stub_embedder.embed_documents_calls[1] == ['Beta-Text mit ausreichend Inhalt.']

    # Chunks with NaN vectors are silently skipped, not raising ValueError
    def test_nan_vector_chunks_are_skipped(self, stub_loader, stub_text_splitter, stub_vector_store, make_document):
        """Embedder der NaN zurückgibt — Chunk wird übersprungen, kein Absturz."""

        class NanEmbedder(EmbeddingPort):
            def embed_query(self, text: str) -> list[float]:
                return [float('nan')]

            def embed_documents(self, texts: list[str]) -> list[list[float]]:
                return [[float('nan'), float('nan'), float('nan')]]

        stub_text_splitter._chunks = ['Chunk A mit ausreichend Text.', 'Chunk B mit ausreichend Text.']
        uc = IngestUseCase(
            loader=stub_loader,
            text_cleaner_service=TextCleanerService(),
            chunking_service=ChunkingService(text_splitter=stub_text_splitter),
            embedder=NanEmbedder(),
            vector_store=stub_vector_store,
        )
        uc.execute_document('test.pdf')
        # Keine Exception, aber auch nichts gespeichert
        assert stub_vector_store.stored_chunks == []


class TestIngestUseCaseExecuteFolder:

    # Ensures only pdf files are loaded
    def test_processes_only_pdf_files(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, tmp_path):
        (tmp_path / 'a.pdf').write_text('PDF Inhalt A')
        (tmp_path / 'b.pdf').write_text('PDF Inhalt B')
        (tmp_path / 'ignored.txt').write_text('Kein PDF')

        stub_text_splitter._chunks = ['Chunk mit ausreichend Text fuer den Filter.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_folder(str(tmp_path))

        pdf_calls = [c for c in stub_loader.load_calls if c.endswith('.pdf')]
        assert len(pdf_calls) == 2

    # Ensures PDFs in subdirectories are also found
    def test_processes_pdfs_in_subdirectories(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, tmp_path):
        (tmp_path / 'root.pdf').write_text('Root PDF')
        sub = tmp_path / 'Unterordner'
        sub.mkdir()
        (sub / 'sub.pdf').write_text('Sub PDF')

        stub_text_splitter._chunks = ['Chunk mit ausreichend Text fuer den Filter.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_folder(str(tmp_path))

        pdf_calls = [c for c in stub_loader.load_calls if c.endswith('.pdf')]
        assert len(pdf_calls) == 2

    # Ensures process doesn't start if no pdf files are given
    def test_skips_non_pdf_files(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, tmp_path):
        (tmp_path / 'readme.txt').write_text('Kein PDF')

        stub_text_splitter._chunks = ['Chunk mit ausreichend Text fuer den Filter.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_folder(str(tmp_path))

        assert stub_loader.load_calls == []


class TestIngestUseCaseExecuteUrls:

    # Ensures every source was passed correctly to the loader
    def test_calls_execute_document_per_url(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['Chunk mit ausreichend Text fuer den Filter.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        urls = ['https://fhdw.de/page1', 'https://fhdw.de/page2']
        uc.execute_urls(urls)
        assert stub_loader.load_calls == urls


class TestIngestUseCaseExecuteUrlsFromFile:

    # Ensures URLs are read from JSON and passed to loader
    def test_reads_urls_from_json(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, tmp_path):
        import json
        url_file = tmp_path / 'urls.json'
        url_file.write_text(json.dumps({'urls': ['https://fhdw.de/a', 'https://fhdw.de/b']}))

        stub_text_splitter._chunks = ['Chunk mit ausreichend Text fuer den Filter.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_urls_from_file(str(url_file))

        assert stub_loader.load_calls == ['https://fhdw.de/a', 'https://fhdw.de/b']

    # Ensures empty URL list does nothing
    def test_empty_urls_does_nothing(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, tmp_path):
        import json
        url_file = tmp_path / 'urls.json'
        url_file.write_text(json.dumps({'urls': []}))

        stub_text_splitter._chunks = ['Chunk mit ausreichend Text fuer den Filter.']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_urls_from_file(str(url_file))

        assert stub_loader.load_calls == []