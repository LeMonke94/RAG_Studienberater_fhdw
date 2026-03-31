# Imports
from dataclasses import dataclass
from typing import List
from .chunk import Chunk

# Datenklasse für LLM-Antwort
@dataclass
class Answer:
    antwort_text: str
    quellen: List[Chunk]
    hat_evidenz: bool