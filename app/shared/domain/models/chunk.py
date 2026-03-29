# Imports
from dataclasses import dataclass
from typing import List, Optional

# Datenklasse für ein Chunk
@dataclass
class Chunk:
    chunk_id: str
    text: str
    quelle: str
    seite: int
    vektor: Optional[List[float]] = None