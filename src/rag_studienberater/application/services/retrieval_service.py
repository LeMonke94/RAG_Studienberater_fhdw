# Imports
import logging

from ...domain.models import Query, RetrievalResult, ScoredChunk
from ...domain.ports import EmbeddingPort, VectorStorePort

logger = logging.getLogger(__name__)


class RetrievalService:

    def __init__(self, vector_store: VectorStorePort, embedder: EmbeddingPort):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(self, query: Query, top_k: int = 5) -> RetrievalResult:
        """Führt Retrieval für eine Nutzerfrage aus und liefert bewertete Chunks zurück."""

        query_vector = self.embedder.embed_query(query.question)

        scored_chunks: list[ScoredChunk] = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k
        )

        logger.debug(f'Gefundene Chunks: {len(scored_chunks)}')
        for instance in scored_chunks:
            logger.debug(
                f'Score: {instance.score} | Text: {instance.chunk.text[:50]}'
            )

        return RetrievalResult(
            scored_chunks=scored_chunks
        )