# Imports
from pydantic_settings import BaseSettings
from typing import Literal

# Settings Klasse
class Settings(BaseSettings):

    # Qdrant
    qdrant_endpoint: str
    qdrant_api_key: str
    qdrant_collection_name: str = 'fhdw_studienberater'

    # Ollama
    ollama_base_url: str = 'http://localhost:11434'
    ollama_llm_model: str = 'qwen2.5:7b'
    ollama_embedding_model: str = 'bge-m3'

    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5

    # Vektorstore 
    # (Später erweiterbar zb um FAISS oder ChromaDB zu testen)
    vector_store: Literal['qdrant']

    class Config:
        env_file = '.env'

settings = Settings()