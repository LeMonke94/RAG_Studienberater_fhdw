import pytest

from rag_studienberater.application.services import RetrievalService
from rag_studienberater.domain.models import Query


class TestRetrievalServiceRetrieve:

    def test_embeds_the_query_question(self, stub_embedder, stub_vector_store):
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        svc.retrieve(Query(question="Was sind die Studiengebühren?"))
        assert stub_embedder.embed_query_calls == ["Was sind die Studiengebühren?"]

    def test_returns_retrieval_result_with_store_chunks(
        self, stub_embedder, stub_vector_store, make_scored_chunk
    ):
        sc = make_scored_chunk(score=0.9)
        stub_vector_store.search_results = [sc]
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        result = svc.retrieve(Query(question="Frage?"))
        assert len(result.scored_chunks) == 1
        assert result.scored_chunks[0].score == 0.9

    def test_empty_store_returns_empty_result(self, stub_embedder, stub_vector_store):
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        result = svc.retrieve(Query(question="Frage?"))
        assert result.scored_chunks == []

    def test_respects_top_k(self, stub_embedder, stub_vector_store, make_scored_chunk):
        stub_vector_store.search_results = [make_scored_chunk() for _ in range(10)]
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        result = svc.retrieve(Query(question="Frage?"), top_k=3)
        assert len(result.scored_chunks) == 3

    def test_default_top_k_is_five(self, stub_embedder, stub_vector_store, make_scored_chunk):
        stub_vector_store.search_results = [make_scored_chunk() for _ in range(10)]
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        result = svc.retrieve(Query(question="Frage?"))
        assert len(result.scored_chunks) == 5

    def test_embed_query_called_exactly_once(self, stub_embedder, stub_vector_store):
        svc = RetrievalService(vector_store=stub_vector_store, embedder=stub_embedder)
        svc.retrieve(Query(question="Frage?"))
        assert len(stub_embedder.embed_query_calls) == 1
