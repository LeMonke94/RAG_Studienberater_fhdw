# Imports
from langchain_ollama import OllamaEmbeddings
from typing import List
from app.shared.domain.ports import EmbeddingPort

# Ollama Adapter für EmbeddingPort
class OllamaEmbeddingClient(EmbeddingPort):

    def __init__(self, model: str = 'bge-m3'):
        self.embedding = OllamaEmbeddings(model=model)

    # Text in einen Vektor umwandeln
    def embed_text(self, text: str) -> List[float]:
        vector = self.embedding.embed_query(text)
        return vector
    
    # Batch an Texten in eine Vektorliste umwandeln
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        vectors = self.embedding.embed_documents(texts)
        return vectors