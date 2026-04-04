# Imports
from abc import ABC, abstractmethod


class EmbeddingPort(ABC):

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        """Wandelt einen Text in einen Vektor um."""
        ...

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Wandelt mehrere Texte in mehrere Vektoren um."""
        ...