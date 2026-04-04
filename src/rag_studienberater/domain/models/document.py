# Imports
from dataclasses import dataclass

from .page import Page


@dataclass
class Document:
    name: str
    source: str
    pages: list[Page]