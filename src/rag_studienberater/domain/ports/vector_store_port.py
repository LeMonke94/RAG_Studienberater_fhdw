# Imports
from abc import ABC, abstractmethod

from ..models import Chunk
from ..models import ScoredChunk


class VectorStorePort(ABC):

    @abstractmethod
    def add_chunks(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Speichert Chunks mit den zugehörigen Vektoren in der Datenbank."""
        ...

    @abstractmethod
    def search(self, query_vector: list[float], top_k: int = 5) -> list[ScoredChunk]:
        """Sucht die ähnlichsten Chunks zum gegebenen Vektor aus der Datenbank."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Löscht alle gespeicherten Werte."""
        ...