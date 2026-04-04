# Imports
from abc import ABC, abstractmethod

from ..models import Document


class DocumentLoaderPort(ABC):
    
    @abstractmethod
    def load(self, source: str) -> Document:
        """Lädt ein Dokument aus einer Quelle."""
        ...