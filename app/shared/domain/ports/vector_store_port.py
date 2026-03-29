# Imports
from abc import ABC, abstractmethod
from typing import List
from app.shared.domain.models import Chunk

# Abstrakte Klasse für die Vektor Datenbank
class VectorStorePort(ABC):

    @abstractmethod
    def add_chunks(self, chunks: List[Chunk]) -> None:
        """Fügt Chunks mit zugehörigen Vektoren und Metadaten in die Vektordatenbank hinzu"""
        pass

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Chunk]:
        """Sucht die ähnlichsten Chunks zum gegebenen Vektor"""
        pass

    @abstractmethod
    def collection_exists(self, collection_name: str) -> bool:
        """Prüft ob eine Collection bereits existiert"""
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> None:
        """Löscht eine Collection"""
        pass

