# Imports
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

from ...domain.models import Document, Page
from ...domain.ports import DocumentLoaderPort


class BeautifulSoupWebDocumentLoader(DocumentLoaderPort):

    def __init__(self, timeout: int = 15):
        self._timeout = timeout

    def load(self, source: str) -> Document:
        response = requests.get(
            source,
            timeout=self._timeout,
            headers={
                "User-Agent": "rag-studienberater/0.3"
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup(['script', 'style', 'nav', 'footer', 'noscript']):
            tag.decompose()

        title = self._extract_title(soup, source)
        text = soup.get_text(separator=" ", strip=True)

        return Document(
            name=title,
            source=source,
            pages=[
                Page(
                    text=text,
                    page_number=1,
                )
            ],
        )
    
    def _extract_title(self, soup: BeautifulSoup, source: str) -> str:
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        
        parsed = urlparse(source)
        return parsed.netloc or source