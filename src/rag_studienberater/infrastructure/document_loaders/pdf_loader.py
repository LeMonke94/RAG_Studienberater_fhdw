# Imports
from pathlib import Path
import pdfplumber

from ...domain.models import Document, Page
from ...domain.ports import DocumentLoaderPort


class PdfPlumberDocumentLoader(DocumentLoaderPort):

    def load(self, source: str) -> Document:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f'PDF-Datei nicht gefunden: {source}')
        
        if path.suffix.lower() != '.pdf':
            raise ValueError(f'Keine PDF-Datei: {source}')
        
        pages: list[Page] = []

        with pdfplumber.open(path) as pdf:
            for index, pdf_page in enumerate(pdf.pages, start=1):
                text = pdf_page.extract_text() or ''
                pages.append(
                    Page(
                        text=text,
                        page_number=index
                    )
                )

        return Document(
            name=path.name,
            source=str(path),
            pages=pages,
        )