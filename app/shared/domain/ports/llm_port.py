# Imports
from abc import ABC, abstractmethod

# Abstrakte Klasse für ein LLM
class LLMPort(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generiert eine Antwort auf den gegebenen Prompt"""
        pass

