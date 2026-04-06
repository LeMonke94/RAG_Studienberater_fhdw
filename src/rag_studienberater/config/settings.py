# Imports
from functools import lru_cache
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class QdrantSettings(BaseModel):
    endpoint: str
    api_key: str
    collection_name: str = 'studienberater'
    vector_dimensions: int = Field(default=1024, gt=0)

class OllamaSettings(BaseModel):
    base_url: str = 'http://localhost:11434'
    language_model: str = 'qwen2.5:7b'
    embedding_model: str = 'bge-m3'

class ChunkingSettings(BaseModel):
    chunk_size: int = Field(default=512, gt=0)
    chunk_overlap: int = Field(default=50, ge=0)
    top_k: int = Field(default=10, gt=0)

class GuardrailSettings(BaseModel):
    min_score: float = Field(default=0.6, ge=0.0, le=1.0)

class LoggingSettings(BaseModel):
    level: str = 'INFO'

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf-8",
        env_nested_delimiter='__',
        extra='ignore',
    )

    qdrant: QdrantSettings
    ollama: OllamaSettings = OllamaSettings()
    chunking: ChunkingSettings = ChunkingSettings()
    guardrail: GuardrailSettings = GuardrailSettings()
    logging: LoggingSettings = LoggingSettings()

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()