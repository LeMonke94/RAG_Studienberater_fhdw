# Imports
import re


class TextCleanerService:
    """Bereinigt einen Text (Whitespace, Zeilenumbrüche etc.)."""

    def clean(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def clean_batch(self, texts: list[str]) -> list[str]:
        return [self.clean(text) for text in texts]