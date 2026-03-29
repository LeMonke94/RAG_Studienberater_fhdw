# Imports
import os
from typing import List
from app.shared.domain.ports import DocumentLoaderPort, EmbeddingPort, VectorStorePort
from app.pipelines.ingestion.infrastructure.loaders import TextCleaner
from app.pipelines.ingestion.domain.services.chunking_service import ChunkingService

# Ingestion Pipeline zusammenstellen
class IngestionService():

    def __init__(self, loader: DocumentLoaderPort, text_cleaner: TextCleaner, chunking_service: ChunkingService, embedder: EmbeddingPort, vector_store: VectorStorePort):
        self.loader = loader
        self.text_cleaner = text_cleaner
        self.chunking_service = chunking_service
        self.embedder = embedder
        self.vector_store = vector_store

    def _process_document(self, path: str) -> None:
        """Lädt, bereinigt, chunked, embeddet und speichert ein Dokument."""
        document = self.loader.load(path)
        # Text bereinigen
        for page in document.seiten:
            page.text = self.text_cleaner.clean(page.text)
        # Dokument in Chunks aufteilen
        chunks = self.chunking_service.chunk_document(document)
        # Texte aus Chunks extrahieren
        texts = []
        for chunk in chunks:
            texts.append(chunk.text)
        # Texte zu Vektoren embedden
        vectors = self.embedder.embed_batch(texts)
        # Vektoren mit Chunks verknüpfen
        for chunk, vector in zip(chunks, vectors):
            chunk.vektor = vector
        # Chunks mit Vektoren in der Vektor-Datenbank speichern
        self.vector_store.add_chunks(chunks)

    def ingest_folder(self, ordner: str) -> None:
        """PDFs aus einem Ordner einlesen und in Qdrant speichern."""
        files = [
            f for f in os.listdir(ordner)
            if f.endswith('.pdf')
        ]
        for f in files:
            self._process_document(os.path.join(ordner, f))

    def ingest_urls(self, urls: List[str]) -> None:
        """Webseiten einlesen und in Qdrant speichern."""

        for url in urls:
            self._process_document(url)