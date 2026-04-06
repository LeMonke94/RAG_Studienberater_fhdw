# Imports
from dataclasses import dataclass

from .scored_chunk import ScoredChunk


@dataclass
class Answer:
    text: str
    sources: list[ScoredChunk]
    has_evidence: bool