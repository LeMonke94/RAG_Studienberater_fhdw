# Imports
from abc import ABC, abstractmethod
from app.shared.domain.models import Document

# Abstrakte Klasse für einen Dokument loader
class DocumentLoaderPort(ABC):

    @abstractmethod
    def load(self, path: str) -> Document:
        """Lädt ein Dokument"""
        pass