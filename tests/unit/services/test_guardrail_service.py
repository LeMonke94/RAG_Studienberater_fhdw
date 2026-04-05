# Imports
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


class TestGuardrailServiceIsQuestionValid:

    def test_short_question_is_invalid(self):
        svc = GuardrailService()
        assert svc.is_question_valid('hi') is False

    def test_empty_string_is_invalid(self):
        svc = GuardrailService()
        assert svc.is_question_valid('') is False

    def test_only_whitespace_is_invalid(self):
        svc = GuardrailService()
        assert svc.is_question_valid('   ') is False

    def test_question_at_min_length_is_valid(self):
        svc = GuardrailService(min_question_length=10)
        assert svc.is_question_valid('Was kostet?') is True  # 11 Zeichen

    def test_question_below_min_length_is_invalid(self):
        svc = GuardrailService(min_question_length=10)
        assert svc.is_question_valid('Hallo') is False

    def test_custom_min_length(self):
        svc = GuardrailService(min_question_length=5)
        assert svc.is_question_valid('Hallo') is True

    def test_invalid_question_response_is_nonempty(self):
        svc = GuardrailService()
        assert len(svc.get_invalid_question_response()) > 0


class TestGuardrailServiceNoEvidenceResponse:

    def test_returns_nonempty_string(self):
        svc = GuardrailService()
        assert len(svc.get_no_evidence_response()) > 0

    def test_response_does_not_raise(self):
        svc = GuardrailService()
        svc.get_no_evidence_response()
