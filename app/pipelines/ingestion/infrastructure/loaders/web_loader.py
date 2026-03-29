# Imports
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from app.shared.domain.ports import DocumentLoaderPort
from app.shared.domain.models import Page, Document

# WebLoader Adapter für DocumentLoaderPort
class WebLoader(DocumentLoaderPort):

    def load(self, path: str) -> Document:
        response = requests.get(path)

        # HTML Parsen
        soup = BeautifulSoup(response.text, 'html.parser')

        # Unerwünschte Tags entfernen
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()

        # Text extrahieren
        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        parsed = urlparse(path)
        dateiname = parsed.netloc + parsed.path

        return Document(
            dateiname=dateiname,
            seiten=[Page(
                text=text,
                seite=1
            )],
            seiten_anzahl=1
        )