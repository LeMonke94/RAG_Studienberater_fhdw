import pytest

from rag_studienberater.application.services import GroundingService, GuardrailService
from rag_studienberater.application.use_cases import AnswerUseCase
from rag_studienberater.domain.models import RetrievalResult


def make_answer_use_case(stub_retrieval_uc, stub_llm, min_score: float = 0.5) -> AnswerUseCase:
    return AnswerUseCase(
        retrieval_use_case=stub_retrieval_uc,
        grounding_service=GroundingService(),
        guardrail_service=GuardrailService(min_score=min_score),
        llm=stub_llm,
    )


class TestAnswerUseCaseNoEvidence:
    """Guardrail blockiert → kein LLM-Aufruf."""

    def test_has_evidence_is_false(self, stub_retrieval_uc, stub_llm):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        answer = uc.execute("Frage?")
        assert answer.has_evidence is False

    def test_sources_is_empty(self, stub_retrieval_uc, stub_llm):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        answer = uc.execute("Frage?")
        assert answer.sources == []

    def test_llm_is_not_called(self, stub_retrieval_uc, stub_llm):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        uc.execute("Frage?")
        assert stub_llm.call_count == 0

    def test_response_text_is_nonempty(self, stub_retrieval_uc, stub_llm):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        answer = uc.execute("Frage?")
        assert len(answer.text) > 0

    def test_all_chunks_below_threshold_blocks(self, stub_retrieval_uc, stub_llm, make_scored_chunk):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[
            make_scored_chunk(score=0.1),
            make_scored_chunk(score=0.3),
        ])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm, min_score=0.5)
        answer = uc.execute("Frage?")
        assert answer.has_evidence is False


class TestAnswerUseCaseWithEvidence:
    """Guardrail passiert → LLM wird aufgerufen."""

    def test_has_evidence_is_true(self, stub_retrieval_uc, stub_llm, make_scored_chunk):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[make_scored_chunk(score=0.9)])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        answer = uc.execute("Frage?")
        assert answer.has_evidence is True

    def test_answer_text_comes_from_llm(self, stub_retrieval_uc, stub_llm, make_scored_chunk):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[make_scored_chunk(score=0.9)])
        stub_llm.response = "Das Studium kostet 500 Euro pro Monat."
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        answer = uc.execute("Frage?")
        assert answer.text == "Das Studium kostet 500 Euro pro Monat."

    def test_llm_is_called_exactly_once(self, stub_retrieval_uc, stub_llm, make_scored_chunk):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[make_scored_chunk(score=0.9)])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        uc.execute("Frage?")
        assert stub_llm.call_count == 1

    def test_sources_contain_retrieved_chunks(self, stub_retrieval_uc, stub_llm, make_scored_chunk):
        sc = make_scored_chunk(score=0.9)
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[sc])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        answer = uc.execute("Frage?")
        assert sc.chunk in answer.sources

    def test_prompt_sent_to_llm_contains_question(self, stub_retrieval_uc, stub_llm, make_scored_chunk):
        stub_retrieval_uc.result = RetrievalResult(scored_chunks=[make_scored_chunk(score=0.9)])
        uc = make_answer_use_case(stub_retrieval_uc, stub_llm)
        uc.execute("Was kostet das Studium?")
        assert "Was kostet das Studium?" in stub_llm.last_prompt