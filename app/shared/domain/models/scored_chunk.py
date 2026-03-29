# Imports
from dataclasses import dataclass
from .chunk import Chunk

# Datenklasse für ein ScoredChunk
@dataclass
class ScoredChunk:
    chunk: Chunk
    score: float