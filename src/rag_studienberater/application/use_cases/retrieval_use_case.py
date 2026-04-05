# Imports
from ...domain.models import Query, RetrievalResult
from ..services import RetrievalService


class RetrievalUseCase:

    def __init__(self, retrieval_service: RetrievalService, top_k: int = 5):
        self.retrieval_service = retrieval_service
        self.top_k = top_k

    def execute(self, query: Query) -> RetrievalResult:
        """Führt Retrieval für eine Nutzerfrage aus."""
        return self.retrieval_service.retrieve(query, self.top_k)