# Imports
from app.shared.domain.models import RetrievalResult
from app.pipelines.retrieval.domain.services.retrieval_service import RetrievalService
from app.pipelines.retrieval.domain.services.guardrail_service import GuardrailService

# Retrieval Pipeline zusammenstellen
class RetrievalOrchestrator:

    def __init__(self, retrieval_service: RetrievalService, guardrail_service: GuardrailService):
        self.retrieval_service = retrieval_service
        self.guardrail_service = guardrail_service

    def retrieve(self, frage: str, top_k: int = 5) -> RetrievalResult:
        """Holt relevante Chunks und prüft die Evidenz"""
        result = self.retrieval_service.retrieve(frage, top_k)

        if not self.guardrail_service.hat_ausreichend_evidenz(result):
            return RetrievalResult(chunks=[], hat_evidenz=False)
        return result