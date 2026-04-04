# Imports
from abc import ABC, abstractmethod


class TextSplitterPort(ABC):

    @abstractmethod
    def split_text(self, text: str) -> list[str]:
        """Teilt einen Text in mehrere Teiltexte auf."""
        ...