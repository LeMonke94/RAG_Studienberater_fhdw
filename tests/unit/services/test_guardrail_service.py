import pytest

from rag_studienberater.application.services import GuardrailService
from rag_studienberater.domain.models import RetrievalResult


class TestGuardrailServiceHasSufficientEvidence:

    def test_empty_chunks_returns_false(self):
        svc = GuardrailService(min_score=0.5)
        result = RetrievalResult(scored_chunks=[])
        assert svc.has_sufficient_evidence(result) is False

    def test_all_below_threshold_returns_false(self, make_scored_chunk):
        svc = GuardrailService(min_score=0.5)
        result = RetrievalResult(scored_chunks=[
            make_scored_chunk(score=0.1),
            make_scored_chunk(score=0.49),
        ])
        assert svc.has_sufficient_evidence(result) is False

    def test_one_at_threshold_returns_true(self, make_scored_chunk):
        svc = GuardrailService(min_score=0.5)
        result = RetrievalResult(scored_chunks=[
            make_scored_chunk(score=0.3),
            make_scored_chunk(score=0.5),
        ])
        assert svc.has_sufficient_evidence(result) is True

    def test_one_above_threshold_returns_true(self, make_scored_chunk):
        svc = GuardrailService(min_score=0.5)
        result = RetrievalResult(scored_chunks=[
            make_scored_chunk(score=0.2),
            make_scored_chunk(score=0.9),
        ])
        assert svc.has_sufficient_evidence(result) is True

    def test_single_chunk_above_threshold(self, make_scored_chunk):
        svc = GuardrailService(min_score=0.7)
        result = RetrievalResult(scored_chunks=[make_scored_chunk(score=0.8)])
        assert svc.has_sufficient_evidence(result) is True

    def test_single_chunk_below_threshold(self, make_scored_chunk):
        svc = GuardrailService(min_score=0.7)
        result = RetrievalResult(scored_chunks=[make_scored_chunk(score=0.6)])
        assert svc.has_sufficient_evidence(result) is False

    def test_default_min_score_blocks_low_scores(self, make_scored_chunk):
        svc = GuardrailService()
        result = RetrievalResult(scored_chunks=[make_scored_chunk(score=0.1)])
        assert svc.has_sufficient_evidence(result) is False


class TestGuardrailServiceNoEvidenceResponse:

    def test_returns_nonempty_string(self):
        svc = GuardrailService()
        assert len(svc.get_no_evidence_response()) > 0

    def test_response_does_not_raise(self):
        svc = GuardrailService()
        svc.get_no_evidence_response()
