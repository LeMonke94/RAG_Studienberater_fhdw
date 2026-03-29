# Imports
from dataclasses import dataclass
from typing import List
from .page import Page

# Dataklass für ein Dokument
@dataclass
class Document:
    dateiname: str
    seiten: List[Page]
    seiten_anzahl: int
    pfad: str