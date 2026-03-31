# Imports
from typing import List
from app.shared.domain.models import Query, RetrievalResult, ScoredChunk
from app.shared.domain.ports import VectorStorePort, EmbeddingPort

# Retrieval Service
class RetrievalService:

    def __init__(self, vector_store: VectorStorePort, embedding: EmbeddingPort):
        self.vector_store = vector_store
        self.embedding = embedding

    # Chunks aus der Vektor-Datenbank holen
    def retrieve(self, frage: str, top_k: int = 5) -> RetrievalResult:
        query = Query(frage=frage)
        query.vektor = self.embedding.embed_text(frage)

        scored_chunks: List[ScoredChunk] = self.vector_store.search(
            query_vector=query.vektor,
            top_k=top_k
        )

        # Temporär zum Debuggen:
        print(f"Gefundene Chunks: {len(scored_chunks)}")
        for sc in scored_chunks:
            print(f"  Score: {sc.score} | Text: {sc.chunk.text[:50]}")

        hat_evidenz = len(scored_chunks) > 0

        return RetrievalResult(
            chunks=scored_chunks,
            hat_evidenz=hat_evidenz
        )