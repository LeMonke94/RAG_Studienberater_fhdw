# Imports
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

from ...domain.ports import VectorStorePort
from ...domain.models import Chunk, ScoredChunk


class QdrantVectorStore(VectorStorePort):

    def __init__(self, endpoint: str, api_key: str, collection_name: str, vector_dimensions: int):
        self.qdrant_client = QdrantClient(url=endpoint, api_key=api_key)
        self.collection_name = collection_name
        self.vector_dimensions = vector_dimensions
        self._ensure_collection_exists()

    def add_chunks(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError('Chunks und Vektoren müssen die gleiche Anzahl haben.')
        
        points = []

        for chunk, vector in zip(chunks, vectors):
            point = PointStruct(
                id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id)),
                vector=vector,
                payload={
                    'chunk_id': chunk.chunk_id,
                    'text': chunk.text,
                    'source': chunk.source,
                    'page': chunk.page
                }
            )
            points.append(point)

        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query_vector: list[float], top_k: int = 5) -> list[ScoredChunk]:
        results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k
        ).points

        scored_chunks: list[ScoredChunk] = []

        for result in results:
            scored_chunk = ScoredChunk(
                chunk=Chunk(
                    chunk_id=result.payload['chunk_id'],
                    text=result.payload['text'],
                    source=result.payload['source'],
                    page=result.payload['page'],
                ),
                score=result.score
            )
            scored_chunks.append(scored_chunk)

        return scored_chunks


    def _ensure_collection_exists(self) -> None:
        """Stellt sicher dass eine Collection initialisiert wird."""
        if not self._collection_exists():
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_dimensions,
                    distance=Distance.COSINE
                )
            )

    def _collection_exists(self) -> bool:
        """Prüft ob eine Collection bereits existiert."""
        collections = self.qdrant_client.get_collections().collections
        names = [c.name for c in collections]
        return self.collection_name in names
    
    def clear(self) -> None:
        self.qdrant_client.delete_collection(collection_name=self.collection_name)
        self._ensure_collection_exists()