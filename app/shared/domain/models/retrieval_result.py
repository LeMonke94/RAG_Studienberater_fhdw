# Imports
from dataclasses import dataclass
from typing import List
from .chunk import Chunk

# Datenklasse für Retrieval Result
@dataclass
class RetrievalResult:
    chunks: List[Chunk]
    hat_evidenz: bool