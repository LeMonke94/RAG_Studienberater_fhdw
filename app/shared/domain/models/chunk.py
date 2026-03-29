# Imports
from dataclasses import dataclass, field
from typing import List, Optional

# Datenklasse für Chunk
@dataclass
class Chunk:
    chunk_id: str
    text: str
    quelle: str
    seite: int
    vektor: Optional[List[float]] = None