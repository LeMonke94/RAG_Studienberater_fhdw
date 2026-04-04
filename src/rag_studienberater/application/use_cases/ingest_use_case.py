# Imports
import logging
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
        if not chunks:
            return

        texts = [chunk.text for chunk in chunks]
        vectors = self.embedder.embed_documents(texts)

        if len(chunks) != len(vectors):
            raise ValueError('Chunks und Vektoren müssen die gleiche Anzahl haben.')

        self.vector_store.add_chunks(chunks=chunks, vectors=vectors)

    def execute_folder(self, folder: str) -> None:
        """PDFs aus einem Ordner einlesen und im Vector-Store speichern."""

        folder_path = Path(folder)

        files = [f for f in folder_path.iterdir() if f.suffix == '.pdf']
        
        logger.info(f"{len(files)} PDFs gefunden in {folder}")
        
        for file_path in files:
            logger.info(f'Verarbeite: {file_path.name}')
            self.execute_document(str(file_path))
            logger.info(f'{file_path.name} erfolgreich verarbeitet.')

    def execute_urls(self, urls: list[str]) -> None:
        """Webseiten einlesen und im Vector-Store speichern."""

        for url in urls:
            self.execute_document(url)