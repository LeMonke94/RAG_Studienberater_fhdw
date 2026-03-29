# Imports
from dataclasses import dataclass

# Dataklass für ein Dokument
@dataclass
class Document:
    dateiname: str
    rohtext: str
    seiten_anzahl: int
    pfad: str