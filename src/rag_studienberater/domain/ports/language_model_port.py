# Imports
from abc import ABC, abstractmethod


class LanguageModelPort(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generiert eine Antwort auf den gegebenen Prompt."""
        ...