# Imports
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from app.shared.domain.models import Document, Chunk

# Chunking Service
class ChunkingService:

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    # Dokument in Chunks verpacken
    def chunk_document(self, document: Document) -> List[Chunk]:
        chunks = []

        for page in document.seiten:
            texte = self.splitter.split_text(page.text)

            for i, chunk_text in enumerate(texte):
                chunk = Chunk(
                    chunk_id=f'{document.dateiname}_{page.seite}_{i}',
                    text=chunk_text,
                    quelle=document.dateiname,
                    seite=page.seite
                )
                chunks.append(chunk)

        return chunks