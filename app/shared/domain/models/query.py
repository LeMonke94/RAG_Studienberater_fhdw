# Imports
from dataclasses import dataclass
from typing import List, Optional

# Datenklasse für Fragen
@dataclass
class Query:
    frage: str
    vektor: Optional[List[float]] = None