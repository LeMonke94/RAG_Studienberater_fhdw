# Imports
from abc import ABC, abstractmethod
from typing import List

# Abstrakte Klasse für ein Embedding-Modell
class EmbeddingPort(ABC):

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Wandelt einen Text in einen Vektor um"""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Wandelt mehrere Texte in Vektoren um"""
        pass