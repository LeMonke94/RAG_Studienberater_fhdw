# Imports
from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str
    page: int | None = None