# Imports
from langchain_ollama import OllamaEmbeddings

from ...domain.ports import EmbeddingPort

# Ollama Adapter für EmbeddingPort
class OllamaEmbeddingModel(EmbeddingPort):

    def __init__(self, model: str, base_url: str):
        self.embeddings = OllamaEmbeddings(
            model=model,
            base_url=base_url,
        )

    def embed_query(self, text: str) -> list[float]:
        """Erzeugt einen Embedding-Vektor für eine Suchanfrage."""
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Erzeugt Embedding-Vektoren für mehrere Texte."""
        return self.embeddings.embed_documents(texts)
