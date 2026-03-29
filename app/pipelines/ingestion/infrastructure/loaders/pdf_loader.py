# Imports
import os
import pdfplumber
from app.shared.domain.ports import DocumentLoaderPort
from app.shared.domain.models import Document, Page

# PDFLoader Adapter für DocumentLoaderPort
class PDFLoader(DocumentLoaderPort):

    def load(self, path: str) -> Document:
        seiten = []

        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                 text = page.extract_text()
                 if text:
                    seiten.append(Page(
                        text=text.strip(),
                        seite=i + 1
                    ))

        return Document(
            dateiname=os.path.basename(path),
            seiten=seiten,
            seiten_anzahl=len(seiten),
            pfad=path
        )