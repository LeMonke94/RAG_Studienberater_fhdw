# Imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import setup_logging, logger, settings
from app.shared.infrastructure.vectorstores.qdrant_store import QdrantStore
from app.shared.infrastructure.embeddings.ollama_embedding import OllamaEmbeddingClient
from app.shared.infrastructure.llm.ollama_client import OllamaClient
from app.pipelines.retrieval.domain.services.retrieval_service import RetrievalService
from app.pipelines.retrieval.domain.services.guardrail_service import GuardrailService
from app.pipelines.retrieval.application.retrieval_orchestrator import RetrievalOrchestrator
from app.pipelines.generation.domain.services.grounding_service import GroundingService
from app.pipelines.generation.application.answer_orchestrator import AnswerOrchestrator

setup_logging()

# Infrastruktur
store = QdrantStore(
    endpoint=settings.qdrant_endpoint,
    api_key=settings.qdrant_api_key,
    collection_name=settings.qdrant_collection_name,
)
embedder = OllamaEmbeddingClient(model=settings.ollama_embedding_model)
llm = OllamaClient(model=settings.ollama_llm_model)

# Services
retrieval_service = RetrievalService(vector_store=store, embedding=embedder)
guardrail_service = GuardrailService(min_score=settings.min_score)
grounding_service = GroundingService()

# Orchestratoren
retrieval_orchestrator = RetrievalOrchestrator(
    retrieval_service=retrieval_service,
    guardrail_service=guardrail_service,
)
answer_orchestrator = AnswerOrchestrator(
    retrieval=retrieval_orchestrator,
    grounding=grounding_service,
    guardrail=guardrail_service,
    llm=llm,
)

# Testfragen
fragen = [
    "Welche KI-Tools sind an der FHDW erlaubt?",
    "Was passiert bei einem Verstoß gegen die KI-Richtlinien?",
    "Was ist die Hauptstadt von Frankreich?",  # Guardrail Test
]

for frage in fragen:
    print(f"\n{'='*50}")
    print(f"FRAGE: {frage}")
    print('='*50)
    antwort = answer_orchestrator.run_answer(frage)
    print(f"ANTWORT: {antwort.antwort_text}")
    if antwort.hat_evidenz:
        print(f"\nQUELLEN:")
        for chunk in antwort.quellen:
            print(f"  - {chunk.quelle}, Seite {chunk.seite}")