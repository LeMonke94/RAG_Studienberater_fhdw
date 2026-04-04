# Imports
from ...domain.models import Document, Chunk
from ...domain.ports import TextSplitterPort


class ChunkingService:

    def __init__(self, text_splitter: TextSplitterPort):
        self.text_splitter = text_splitter

    # Split Document into Chunks
    def chunk_document(self, document: Document) -> list[Chunk]:
        """Trennt ein Dokument in Chunks auf."""

        chunks: list[Chunk] = []

        for page in document.pages:
            texts = self.text_splitter.split_text(page.text)

            for i, text in enumerate(texts):
                chunk = Chunk(
                    chunk_id=f'{document.source}:{page.page_number}:{i}',
                    text=text,
                    source=document.source,
                    page=page.page_number
                )
                chunks.append(chunk)

        return chunks