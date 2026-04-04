from langchain_text_splitters import RecursiveCharacterTextSplitter

from ...domain.ports import TextSplitterPort


class LangChainTextSplitter(TextSplitterPort):

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def split_text(self, text: str) -> list[str]:
        """Teilt einen Text mit LangChain in Teiltexte auf."""
        return self.splitter.split_text(text)
