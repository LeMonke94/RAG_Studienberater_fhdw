import pytest

from rag_studienberater.application.services import GroundingService
from rag_studienberater.domain.models import Query, RetrievalResult


class TestGroundingServiceBuildPrompt:

    def setup_method(self):
        self.svc = GroundingService()

    def test_prompt_contains_question(self, make_scored_chunk):
        query = Query(question="Was kostet das Studium?")
        result = RetrievalResult(scored_chunks=[make_scored_chunk()])
        prompt = self.svc.build_prompt(query, result)
        assert "Was kostet das Studium?" in prompt

    def test_prompt_contains_chunk_text(self, make_scored_chunk):
        query = Query(question="Frage?")
        sc = make_scored_chunk(text="Studiengebühren betragen 500 Euro.")
        result = RetrievalResult(scored_chunks=[sc])
        prompt = self.svc.build_prompt(query, result)
        assert "Studiengebühren betragen 500 Euro." in prompt

    def test_prompt_with_empty_chunks_does_not_raise(self):
        query = Query(question="Frage?")
        result = RetrievalResult(scored_chunks=[])
        prompt = self.svc.build_prompt(query, result)
        assert "Frage?" in prompt


class TestGroundingServiceFormatContext:

    def setup_method(self):
        self.svc = GroundingService()

    def test_context_contains_source_with_page(self, make_scored_chunk):
        sc = make_scored_chunk(source="studiengang.pdf", page=3)
        result = RetrievalResult(scored_chunks=[sc])
        context = self.svc._format_context(result)
        assert "studiengang.pdf" in context
        assert "3" in context

    def test_context_contains_source_without_page(self, make_scored_chunk):
        sc = make_scored_chunk(source="fhdw-website.html", page=None)
        result = RetrievalResult(scored_chunks=[sc])
        context = self.svc._format_context(result)
        assert "fhdw-website.html" in context

    def test_context_numbers_sources_starting_at_one(self, make_scored_chunk):
        result = RetrievalResult(scored_chunks=[
            make_scored_chunk(text="Erster Chunk"),
            make_scored_chunk(text="Zweiter Chunk"),
            make_scored_chunk(text="Dritter Chunk"),
        ])
        context = self.svc._format_context(result)
        assert "Quelle 1" in context
        assert "Quelle 2" in context
        assert "Quelle 3" in context

    def test_context_separates_chunks(self, make_scored_chunk):
        result = RetrievalResult(scored_chunks=[
            make_scored_chunk(text="Alpha"),
            make_scored_chunk(text="Beta"),
        ])
        context = self.svc._format_context(result)
        assert "Alpha" in context
        assert "Beta" in context

    def test_empty_context_returns_empty_string(self):
        result = RetrievalResult(scored_chunks=[])
        context = self.svc._format_context(result)
        assert context == ""

    def test_page_none_omits_page_in_header(self, make_scored_chunk):
        sc = make_scored_chunk(source="web.html", page=None)
        result = RetrievalResult(scored_chunks=[sc])
        context = self.svc._format_context(result)
        assert "Seite" not in context
