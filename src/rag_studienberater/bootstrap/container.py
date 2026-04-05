# Imports
from dataclasses import dataclass

from ..application.services import (
    ChunkingService,
    GroundingService,
    GuardrailService,
    RetrievalService,
    TextCleanerService,
)
from ..application.use_cases import (
    AnswerUseCase,
    IngestUseCase,
    RetrievalUseCase,
)
from ..config.logging_config import setup_logging
from ..config.settings import Settings, get_settings
from ..infrastructure.document_loaders import (
    BeautifulSoupWebDocumentLoader,
    PdfPlumberDocumentLoader,
    RoutingDocumentLoader,
)
from ..infrastructure.embedding_models import OllamaEmbeddingModel
from ..infrastructure.language_models import OllamaLanguageModel
from ..infrastructure.text_splitters import LangChainTextSplitter
from ..infrastructure.vector_stores import QdrantVectorStore


@dataclass(frozen=True)
class Container:
    settings: Settings
    answer_use_case: AnswerUseCase
    ingest_use_case: IngestUseCase
    retrieval_use_case: RetrievalUseCase

def create_container() -> Container:
    settings = get_settings()

    setup_logging(settings.logging.level)

    # Infrastructure
    pdf_loader = PdfPlumberDocumentLoader()
    web_loader = BeautifulSoupWebDocumentLoader(timeout=15)
    document_loader = RoutingDocumentLoader(
        pdf_loader=pdf_loader,
        web_loader=web_loader,
    )
    text_splitter = LangChainTextSplitter(
        chunk_size=settings.chunking.chunk_size,
        chunk_overlap=settings.chunking.chunk_overlap,
    )
    embedder = OllamaEmbeddingModel(
        model=settings.ollama.embedding_model,
        base_url=settings.ollama.base_url,
    )
    llm = OllamaLanguageModel(
        model=settings.ollama.language_model,
        base_url=settings.ollama.base_url,
    )
    vector_store = QdrantVectorStore(
        endpoint=settings.qdrant.endpoint,
        api_key=settings.qdrant.api_key,
        collection_name=settings.qdrant.collection_name,
        vector_dimensions=settings.qdrant.vector_dimensions,
    )

    # Services
    text_cleaner_service = TextCleanerService()
    chunking_service = ChunkingService(text_splitter=text_splitter)
    retrieval_service = RetrievalService(
        vector_store=vector_store,
        embedder=embedder,
    )
    grounding_service = GroundingService()
    guardrail_service = GuardrailService(
        min_score=settings.guardrail.min_score
    )

    # Use Cases
    retrieval_use_case = RetrievalUseCase(
        retrieval_service=retrieval_service,
        top_k=settings.chunking.top_k,
    )
    ingest_use_case = IngestUseCase(
        loader=document_loader,
        text_cleaner_service=text_cleaner_service,
        chunking_service=chunking_service,
        embedder=embedder,
        vector_store=vector_store,
    )
    answer_use_case = AnswerUseCase(
        retrieval_use_case=retrieval_use_case,
        grounding_service=grounding_service,
        guardrail_service=guardrail_service,
        llm=llm,
    )

    return Container(
        settings=settings,
        ingest_use_case=ingest_use_case,
        retrieval_use_case=retrieval_use_case,
        answer_use_case=answer_use_case,
    )