"""
Stubs und fixtures für alle Unit-Tests
Stubs sind konkrete, minimale Implementierungen der Port-Interfaces
Ersetzen externe Abhängigkeiten (Ollama, Qdrant) vollständig
"""

# Imports
import pytest

# Import Dataclasses from Models
from rag_studienberater.domain.models import (
    Chunk,
    Document,
    Page,
    Query,
    RetrievalResult,
    ScoredChunk,
)
# Import Ports
from rag_studienberater.domain.ports import (
    DocumentLoaderPort,
    EmbeddingPort,
    LanguageModelPort,
    TextSplitterPort,
    VectorStorePort,
)


# Stubs
class StubTextSplitter(TextSplitterPort):
    """Gibt eine konfigurierbare Liste von Strings zurück."""

    def __init__(self, chunks: list[str] | None = None):
        self._chunks = chunks if chunks is not None else [
            "Dies ist Chunk A mit ausreichend Inhalt.",
            "Dies ist Chunk B mit ausreichend Inhalt.",
        ]

    def split_text(self, text: str) -> list[str]:
        return self._chunks


class StubEmbedder(EmbeddingPort):
    """Liefert Dummy-Vektoren und protokolliert Aufrufe."""

    # Dimensionen
    DIM = 3

    def __init__(self):
        self.embed_query_calls: list[str] = []
        self.embed_documents_calls: list[list[str]] = []

    def embed_query(self, text: str) -> list[float]:
        self.embed_query_calls.append(text)
        return [0.6] * self.DIM
    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.embed_documents_calls.append(texts)
        return [[0.3] * self.DIM for _ in texts]


class StubVectorStore(VectorStorePort):
    """In-Memory-Store mit konfigurierbaren Suchergebnissen."""

    def __init__(self):
        self.stored_chunks: list[Chunk] = []
        self.stored_vectors: list[list[float]] = []
        self.search_results: list[ScoredChunk] = []
        self.add_chunks_call_count: int = 0

    def add_chunks(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        self.stored_chunks.extend(chunks)
        self.stored_vectors.extend(vectors)
        self.add_chunks_call_count += 1

    def search(self, query_vector: list[float], top_k: int = 5) -> list[ScoredChunk]:
        return self.search_results[:top_k]

    def clear(self) -> None:
        self.stored_chunks.clear()
        self.stored_vectors.clear()
        self.search_results.clear()


class StubLanguageModel(LanguageModelPort):
    """Gibt eine konfigurierbare Antwort zurück und protokolliert den letzten Prompt."""

    def __init__(self, response: str = 'Test-Antwort'):
        self.response = response
        self.last_prompt: str | None = None
        self.call_count: int = 0

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        self.call_count += 1
        return self.response


class StubDocumentLoader(DocumentLoaderPort):
    """Liefert ein konfigurierbares Dokument."""

    def __init__(self, document: Document | None = None):
        self.document = document or Document(
            name='test.pdf',
            source='test.pdf',
            pages=[Page(text='Standardinhalt', page_number=1)],
        )
        self.load_calls: list[str] = []

    def load(self, source: str) -> Document:
        self.load_calls.append(source)
        return self.document


class StubRetrievalUseCase:
    """Stub für RetrievalUseCase (kein Port, daher kein ABC)."""

    def __init__(self, result: RetrievalResult | None = None):
        self.result = result or RetrievalResult(scored_chunks=[])

    def execute(self, query: Query) -> RetrievalResult:
        return self.result


# Fixtures — Factory Objekte
@pytest.fixture
def make_chunk():
    """Factory-Fixture für Chunk-Objekte."""
    def factory(
        text: str = 'Beispieltext.',
        source: str = 'test.pdf',
        page: int | None = 1,
        index: int = 0,
    ) -> Chunk:
        return Chunk(
            chunk_id=f"{source}:{page}:{index}",
            text=text,
            source=source,
            page=page,
        )
    return factory


@pytest.fixture
def make_scored_chunk(make_chunk):
    """Factory-Fixture für ScoredChunk-Objekte."""
    def factory(
        text: str = 'Beispieltext.',
        source: str = 'test.pdf',
        page: int | None = 1,
        score: float = 0.8,
    ) -> ScoredChunk:
        return ScoredChunk(chunk=make_chunk(text=text, source=source, page=page), score=score)
    return factory


@pytest.fixture
def make_document():
    """Factory-Fixture für Document-Objekte."""
    def factory(
        pages: list[Page] | None = None,
        name: str = 'test.pdf',
        source: str = 'test.pdf',
    ) -> Document:
        if pages is None:
            pages = [Page(text='Standardinhalt', page_number=1)]
        return Document(name=name, source=source, pages=pages)
    return factory


# Instanzierung der Fixtures
@pytest.fixture
def stub_text_splitter() -> StubTextSplitter:
    return StubTextSplitter()

@pytest.fixture
def stub_embedder() -> StubEmbedder:
    return StubEmbedder()

@pytest.fixture
def stub_vector_store() -> StubVectorStore:
    return StubVectorStore()

@pytest.fixture
def stub_llm() -> StubLanguageModel:
    return StubLanguageModel()

@pytest.fixture
def stub_loader() -> StubDocumentLoader:
    return StubDocumentLoader()

@pytest.fixture
def stub_retrieval_uc() -> StubRetrievalUseCase:
    return StubRetrievalUseCase()