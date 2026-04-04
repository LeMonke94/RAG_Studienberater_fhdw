# Imports
from ...domain.models import Query, RetrievalResult
from ..services import RetrievalService


class RetrievalUseCase:

    def __init__(self, retrieval_service: RetrievalService):
        self.retrieval_service = retrieval_service

    def execute(self, query: Query, top_k: int = 5) -> RetrievalResult:
        """Führt Retrieval für eine Nutzerfrage aus."""
        return self.retrieval_service.retrieve(query, top_k)