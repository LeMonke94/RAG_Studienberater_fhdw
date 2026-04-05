# Imports
from rag_studienberater.application.services import RetrievalService
from rag_studienberater.application.use_cases import RetrievalUseCase
from rag_studienberater.domain.models import Query


class TestRetrievalUseCaseTopK:

    def test_top_k_from_constructor_is_used(self, stub_embedder, stub_vector_store, make_scored_chunk):
        stub_vector_store.search_results = [make_scored_chunk() for _ in range(10)]
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        uc = RetrievalUseCase(retrieval_service=svc, top_k=3)
        result = uc.execute(Query(question='Was kostet das Studium?'))
        assert len(result.scored_chunks) == 3

    def test_default_top_k_is_five(self, stub_embedder, stub_vector_store, make_scored_chunk):
        stub_vector_store.search_results = [make_scored_chunk() for _ in range(10)]
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        uc = RetrievalUseCase(retrieval_service=svc)
        result = uc.execute(Query(question='Was kostet das Studium?'))
        assert len(result.scored_chunks) == 5

    def test_top_k_setting_is_stored(self, stub_embedder, stub_vector_store):
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        uc = RetrievalUseCase(retrieval_service=svc, top_k=7)
        assert uc.top_k == 7
