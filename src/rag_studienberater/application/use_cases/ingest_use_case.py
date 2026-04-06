# Imports
import json
import logging
import math
from dataclasses import dataclass, field
from pathlib import Path

from ..services import ChunkingService, TextCleanerService
from ...domain.ports import DocumentLoaderPort, EmbeddingPort, VectorStorePort


logger = logging.getLogger(__name__)


@dataclass
class IngestStats:
    """Statistiken eines Ingest-Laufs (Ordner oder URL-Liste)."""
    total_chunks: int = 0
    skipped_chunks: int = 0
    failed_documents: list[str] = field(default_factory=list)

    @property
    def ingested_chunks(self) -> int:
        return self.total_chunks - self.skipped_chunks

    @property
    def skip_rate(self) -> float:
        return self.skipped_chunks / self.total_chunks if self.total_chunks > 0 else 0.0


class IngestUseCase:

    def __init__(self, loader: DocumentLoaderPort, text_cleaner_service: TextCleanerService, chunking_service: ChunkingService, embedder: EmbeddingPort, vector_store: VectorStorePort):
        self.loader = loader
        self.text_cleaner_service = text_cleaner_service
        self.chunking_service = chunking_service
        self.embedder = embedder
        self.vector_store = vector_store

    def execute_document(self, source: str) -> tuple[int, int]:
        """Lädt, bereinigt, chunked, embeddet und speichert ein Dokument.

        Gibt (total_chunks, skipped_chunks) zurück.
        """
        document = self.loader.load(source)

        for page in document.pages:
            page.text = self.text_cleaner_service.clean(page.text)

        chunks = self.chunking_service.chunk_document(document)
        chunks = [c for c in chunks if len(c.text.strip()) >= 20]
        if not chunks:
            logger.warning(f'Keine verwertbaren Chunks für {source} — übersprungen.')
            return 0, 0

        valid_chunks, valid_vectors, skipped = self._embed_with_validation(chunks, source)

        if not valid_chunks:
            logger.warning(f'Keine gültigen Vektoren für {source} — übersprungen.')
            return len(chunks), len(chunks)

        self.vector_store.add_chunks(chunks=valid_chunks, vectors=valid_vectors)
        return len(chunks), skipped

    def _embed_with_validation(
        self, chunks: list, source: str
    ) -> tuple[list, list, int]:
        """Embeddet jeden Chunk einzeln und filtert ungültige Vektoren heraus.

        Durch einzelnes Embedding wird verhindert, dass ein problematischer Chunk
        den gesamten Batch scheitern lässt.

        Gibt (valid_chunks, valid_vectors, skipped_count) zurück.
        """
        valid_chunks = []
        valid_vectors = []

        for chunk in chunks:
            try:
                vectors = self.embedder.embed_documents([chunk.text])
                if not vectors:
                    logger.warning(f'Leerer Vektor für {chunk.chunk_id} — übersprungen.')
                    continue
                vector = vectors[0]
                if not vector or not all(math.isfinite(float(v)) for v in vector):
                    logger.warning(f'NaN/Inf-Vektor für {chunk.chunk_id} — übersprungen.')
                    continue
                valid_chunks.append(chunk)
                valid_vectors.append(vector)
            except Exception as e:
                logger.warning(f'Embedding für {chunk.chunk_id} fehlgeschlagen: {e} — übersprungen.')

        skipped = len(chunks) - len(valid_chunks)
        if skipped > 0:
            logger.warning(f'{skipped}/{len(chunks)} Chunks für {source} übersprungen.')

        return valid_chunks, valid_vectors, skipped

    def execute_folder(self, folder: str) -> IngestStats:
        """PDFs aus einem Ordner und allen Unterordnern einlesen und im Vector-Store speichern."""
        stats = IngestStats()
        folder_path = Path(folder)
        files = list(folder_path.rglob('*.pdf'))

        logger.info(f'{len(files)} PDFs gefunden in {folder} (inkl. Unterordner)')

        for file_path in files:
            logger.info(f'Verarbeite: {file_path.name}')
            try:
                total, skipped = self.execute_document(str(file_path))
                stats.total_chunks += total
                stats.skipped_chunks += skipped
                logger.info(f'{file_path.name} erfolgreich verarbeitet.')
            except Exception as e:
                logger.warning(f'{file_path.name} konnte nicht verarbeitet werden: {e}')
                stats.failed_documents.append(file_path.name)

        return stats

    def execute_urls(self, urls: list[str]) -> IngestStats:
        """Webseiten einlesen und im Vector-Store speichern."""
        stats = IngestStats()

        for url in urls:
            logger.info(f'Verarbeite: {url}')
            try:
                total, skipped = self.execute_document(url)
                stats.total_chunks += total
                stats.skipped_chunks += skipped
                logger.info(f'{url} erfolgreich verarbeitet.')
            except Exception as e:
                logger.warning(f'{url} konnte nicht verarbeitet werden: {e}')
                stats.failed_documents.append(url)

        return stats

    def execute_urls_from_file(self, json_path: str) -> IngestStats:
        """URLs aus einer JSON-Datei einlesen und im Vector-Store speichern."""
        path = Path(json_path)
        with path.open(encoding='utf-8') as f:
            data = json.load(f)

        urls: list[str] = data.get('urls', [])
        logger.info(f'{len(urls)} URLs gefunden in {json_path}')
        return self.execute_urls(urls)
