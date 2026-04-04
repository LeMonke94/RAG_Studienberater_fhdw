# Imports
from dataclasses import dataclass

from .scored_chunk import ScoredChunk


@dataclass
class RetrievalResult:
    scored_chunks: list[ScoredChunk]