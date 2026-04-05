# Imports
import json
import logging
import math
from pathlib import Path

from ..services import ChunkingService, TextCleanerService
from ...domain.ports import DocumentLoaderPort, EmbeddingPort, VectorStorePort


logger = logging.getLogger(__name__)

class IngestUseCase:

    def __init__(self, loader: DocumentLoaderPort, text_cleaner_service: TextCleanerService, chunking_service: ChunkingService, embedder: EmbeddingPort, vector_store: VectorStorePort):
        self.loader = loader
        self.text_cleaner_service = text_cleaner_service
        self.chunking_service = chunking_service
        self.embedder = embedder
        self.vector_store = vector_store

    def execute_document(self, source: str) -> None:
        """Lädt, bereinigt, chunked, embeddet und speichert ein Dokument."""

        document = self.loader.load(source)

        for page in document.pages:
            page.text = self.text_cleaner_service.clean(page.text)

        chunks = self.chunking_service.chunk_document(document)
        chunks = [c for c in chunks if len(c.text.strip()) >= 20]
        if not chunks:
            logger.warning(f'Keine verwertbaren Chunks für {source} — übersprungen.')
            return

        valid_chunks, valid_vectors = self._embed_with_validation(chunks, source)

        if not valid_chunks:
            logger.warning(f'Keine gültigen Vektoren für {source} — übersprungen.')
            return

        self.vector_store.add_chunks(chunks=valid_chunks, vectors=valid_vectors)

    def _embed_with_validation(
        self, chunks: list, source: str
    ) -> tuple[list, list]:
        """Embeddet jeden Chunk einzeln und filtert ungültige Vektoren heraus.

        Durch einzelnes Embedding wird verhindert, dass ein problematischer Chunk
        den gesamten Batch scheitern lässt.
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

        return valid_chunks, valid_vectors

    def execute_folder(self, folder: str) -> None:
        """PDFs aus einem Ordner und allen Unterordnern einlesen und im Vector-Store speichern."""

        folder_path = Path(folder)

        files = list(folder_path.rglob('*.pdf'))

        logger.info(f"{len(files)} PDFs gefunden in {folder} (inkl. Unterordner)")

        for file_path in files:
            logger.info(f'Verarbeite: {file_path.name}')
            try:
                self.execute_document(str(file_path))
                logger.info(f'{file_path.name} erfolgreich verarbeitet.')
            except Exception as e:
                logger.warning(f'{file_path.name} konnte nicht verarbeitet werden: {e}')

    def execute_urls(self, urls: list[str]) -> None:
        """Webseiten einlesen und im Vector-Store speichern."""

        for url in urls:
            logger.info(f'Verarbeite: {url}')
            try:
                self.execute_document(url)
                logger.info(f'{url} erfolgreich verarbeitet.')
            except Exception as e:
                logger.warning(f'{url} konnte nicht verarbeitet werden: {e}')

    def execute_urls_from_file(self, json_path: str) -> None:
        """URLs aus einer JSON-Datei einlesen und im Vector-Store speichern.

        Erwartet folgendes Format:
            {"urls": ["https://...", "https://..."]}
        """

        path = Path(json_path)
        with path.open(encoding='utf-8') as f:
            data = json.load(f)

        urls: list[str] = data.get('urls', [])
        logger.info(f"{len(urls)} URLs gefunden in {json_path}")
        self.execute_urls(urls)