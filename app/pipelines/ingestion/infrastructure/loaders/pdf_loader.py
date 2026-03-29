# Imports
import os
from pypdf import PdfReader
from typing import List
from app.shared.domain.ports import DocumentLoaderPort
from app.shared.domain.models import Document, Page

# PDFLoader Adapter für DocumentLoaderPort
class PDFLoader(DocumentLoaderPort):

    def load(self, path: str) -> Document:
        reader = PdfReader(path)

        seiten = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                seiten.append(Page(
                    text=text,
                    seite=i + 1
                ))

        return Document(
            dateiname=os.path.basename(path),
            seiten=seiten,
            seiten_anzahl=len(reader.pages),
            pfad=path
        )