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
        stub_text_splitter._chunks = ['chunk_a', 'chunk_b']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        assert len(stub_vector_store.stored_chunks) == 2

    # Ensure chunk text was saved correctly as in the splitter
    def test_stored_chunks_match_texts(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['Erster Chunk', 'Zweiter Chunk']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        texts = [c.text for c in stub_vector_store.stored_chunks]
        assert 'Erster Chunk' in texts
        assert 'Zweiter Chunk' in texts

    # Ensures there's one vector for one chunk
    def test_chunk_count_matches_vector_count(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['a', 'b', 'c']
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

    # Ensures only prepared chunks are sent to the embedder
    def test_embedder_called_with_chunk_texts(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['alpha', 'beta']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_document('test.pdf')
        assert stub_embedder.embed_documents_calls[-1] == ['alpha', 'beta']

    # Test for error raise if chunks amount doesnt fit vector amount
    def test_mismatched_chunks_and_vectors_raises(self, stub_loader, stub_text_splitter, stub_vector_store, make_document):
        """Embedder der immer nur 1 Vektor zurückgibt, egal wie viele Chunks."""

        class OnlyOneVectorEmbedder(EmbeddingPort):
            def embed_query(self, text: str) -> list[float]:
                return [0.1]

            def embed_documents(self, texts: list[str]) -> list[list[float]]:
                return [[0.1]]  # always one

        stub_text_splitter._chunks = ['a', 'b']  # two chunks
        uc = IngestUseCase(
            loader=stub_loader,
            text_cleaner_service=TextCleanerService(),
            chunking_service=ChunkingService(text_splitter=stub_text_splitter),
            embedder=OnlyOneVectorEmbedder(),
            vector_store=stub_vector_store,
        )
        with pytest.raises(ValueError):
            uc.execute_document('test.pdf')


class TestIngestUseCaseExecuteFolder:

    # Ensures only pdf files are loaded
    def test_processes_only_pdf_files(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, tmp_path):
        (tmp_path / 'a.pdf').write_text('PDF Inhalt A')
        (tmp_path / 'b.pdf').write_text('PDF Inhalt B')
        (tmp_path / 'ignored.txt').write_text('Kein PDF')

        stub_text_splitter._chunks = ['chunk']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_folder(str(tmp_path))

        pdf_calls = [c for c in stub_loader.load_calls if c.endswith('.pdf')]
        assert len(pdf_calls) == 2

    # Ensures process doesn't start if no pdf files are given
    def test_skips_non_pdf_files(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store, tmp_path):
        (tmp_path / 'readme.txt').write_text('Kein PDF')

        stub_text_splitter._chunks = ['chunk']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        uc.execute_folder(str(tmp_path))

        assert stub_loader.load_calls == []


class TestIngestUseCaseExecuteUrls:

    # Ensures every source was passed correctly to the loader
    def test_calls_execute_document_per_url(self, stub_loader, stub_text_splitter, stub_embedder, stub_vector_store):
        stub_text_splitter._chunks = ['chunk']
        uc = make_ingest_use_case(stub_loader, stub_text_splitter, stub_embedder, stub_vector_store)
        urls = ['https://fhdw.de/page1', 'https://fhdw.de/page2']
        uc.execute_urls(urls)
        assert stub_loader.load_calls == urls