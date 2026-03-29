# Imports
from dataclasses import dataclass

# Dataklass für eine Dokument-Seite
@dataclass
class Page:
    text: str
    seite: int