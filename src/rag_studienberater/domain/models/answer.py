# Imports
from dataclasses import dataclass

from .chunk import Chunk


@dataclass
class Answer:
    text: str
    sources: list[Chunk]
    has_evidence: bool