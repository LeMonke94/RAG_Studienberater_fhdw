# Imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import setup_logging, logger, settings
from app.shared.infrastructure.vectorstores.qdrant_store import QdrantStore
from app.shared.infrastructure.embeddings.ollama_embedding import OllamaEmbeddingClient
from app.pipelines.ingestion.infrastructure.loaders.pdf_loader import PDFLoader
from app.pipelines.ingestion.infrastructure.loaders.text_cleaner import TextCleaner
from app.pipelines.ingestion.domain.services.chunking_service import ChunkingService
from app.pipelines.ingestion.application.ingestion_orchestrator import IngestionOrchestrator

setup_logging()


def main():
    logger.info("Ingestion Pipeline gestartet")

    # Infrastruktur initialisieren
    store = QdrantStore(
        endpoint=settings.qdrant_endpoint,
        api_key=settings.qdrant_api_key,
        collection_name=settings.qdrant_collection_name,
    )
    embedder = OllamaEmbeddingClient(model=settings.ollama_embedding_model)
    loader = PDFLoader()
    cleaner = TextCleaner()
    chunker = ChunkingService(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    # Orchestrator zusammensetzen
    orchestrator = IngestionOrchestrator(
        loader=loader,
        text_cleaner=cleaner,
        chunking_service=chunker,
        embedder=embedder,
        vector_store=store,
    )

    # Pipeline ausführen
    orchestrator.run_ingest_folder("data/raw/pdf")
    logger.info("Ingestion abgeschlossen!")

if __name__ == "__main__":
    main()