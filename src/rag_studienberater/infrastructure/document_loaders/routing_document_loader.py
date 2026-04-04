# Imports
from pathlib import Path
from urllib.parse import urlparse

from ...domain.models import Document
from ...domain.ports import DocumentLoaderPort


class RoutingDocumentLoader(DocumentLoaderPort):

    def __init__(self, pdf_loader: DocumentLoaderPort, web_loader: DocumentLoaderPort):
        self._pdf_loader = pdf_loader
        self._web_loader = web_loader

    def load(self, source: str) -> Document:
        if self._is_url(source):
            return self._web_loader.load(source)
        
        if self._is_pdf_file(source):
            return self._pdf_loader.load(source)
        
        raise ValueError(f'Nicht unterstützte Quelle: {source}')
    
    def _is_url(self, source: str) -> bool:
        parsed = urlparse(source)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    
    def _is_pdf_file(self, source: str) -> bool:
        return Path(source).suffix.lower() == ".pdf"