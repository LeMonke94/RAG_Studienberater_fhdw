# Imports
import re
from typing import List

# Hilfsklasse
class TextCleaner:

    # Bereinigt Text mit Regex
    def clean(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def clean_batch(self, texts: List[str]) -> List[str]:
        return [self.clean(text) for text in texts]