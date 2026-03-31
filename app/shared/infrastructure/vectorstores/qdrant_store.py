# Imports
from app.shared.domain.ports import VectorStorePort
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import List
from app.shared.domain.models import Chunk
from app.shared.domain.models import ScoredChunk
import uuid

# Qdrant Adapter für VectorStorePort
class QdrantStore(VectorStorePort):

    def __init__(self, endpoint: str, api_key: str, collection_name: str):
        self.client = QdrantClient(url=endpoint, api_key=api_key)
        self.collection_name = collection_name
        self._ensure_collection_exists()

    # Erstellt eine Collection wenn keine existiert
    def _ensure_collection_exists(self) -> None:
        if not self.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance.COSINE
                )
            )

    # Chunks in Qdrant speichern
    def add_chunks(self, chunks: List[Chunk]) -> None:
        # Points mit Payload erstellen
        points = []
        for chunk in chunks:
            point = PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id)),
                vector=chunk.vektor,
                payload= {
                    'chunk_id': chunk.chunk_id,
                    'text': chunk.text,
                    'quelle': chunk.quelle,
                    'seite': chunk.seite
                }
            )
            points.append(point)
        # Points mit Payload in die Vektor-Datenbank hochladen
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    # Zum Vektor ähnliche Chunks finden
    def search(self, query_vector: List[float], top_k: int = 5) -> List[ScoredChunk]:
        # Ähnliche Points aus der Vektor-Datenbank holen
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k
        ).points

        # ScoredChunk aus dem Chunk und Score im result Payload erstellen
        scored_chunks = []
        for result in results:
            scored_chunk = ScoredChunk(
                chunk=Chunk(
                    chunk_id=result.payload['chunk_id'],
                    text=result.payload['text'],
                    quelle=result.payload['quelle'],
                    seite=result.payload['seite']
                ),
                score=result.score
            )
            scored_chunks.append(scored_chunk)
        return scored_chunks

    # Prüfung ob die Collection existiert
    def collection_exists(self, collection_name: str) -> bool:
        collections = self.client.get_collections().collections
        namen = [c.name for c in collections]
        return collection_name in namen
    
    # Collection löschen
    def delete_collection(self, collection_name: str) -> None:
        self.client.delete_collection(collection_name=collection_name)