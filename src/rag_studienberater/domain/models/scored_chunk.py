# Imports
from dataclasses import dataclass

from .chunk import Chunk


@dataclass
class ScoredChunk:
    chunk: Chunk
    score: float