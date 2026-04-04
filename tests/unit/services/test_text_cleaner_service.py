# Imports
import pytest

from rag_studienberater.application.services import TextCleanerService


class TestTextCleanerServiceClean:

    def setup_method(self):
        self.svc = TextCleanerService()

    def test_collapses_multiple_spaces(self):
        assert self.svc.clean('hello   world') == 'hello world'

    def test_collapses_newlines(self):
        assert self.svc.clean('hello\n\nworld') == 'hello world'

    def test_collapses_tabs(self):
        assert self.svc.clean('hello\t\tworld') == 'hello world'

    def test_strips_leading_whitespace(self):
        assert self.svc.clean('   hello') == 'hello'

    def test_strips_trailing_whitespace(self):
        assert self.svc.clean('hello   ') == 'hello'

    def test_empty_string_returns_empty(self):
        assert self.svc.clean('') == ''

    def test_already_clean_string_unchanged(self):
        assert self.svc.clean('schon sauber') == 'schon sauber'

    def test_only_whitespace_returns_empty(self):
        assert self.svc.clean('   \n\t  ') == ''


class TestTextCleanerServiceCleanBatch:

    def setup_method(self):
        self.svc = TextCleanerService()

    def test_cleans_every_element(self):
        result = self.svc.clean_batch(['  a  b  ', 'c\n\nd'])
        assert result == ['a b', 'c d']

    def test_empty_list_returns_empty_list(self):
        assert self.svc.clean_batch([]) == []

    def test_preserves_order(self):
        inputs = ['z  z', 'a  a', 'm  m']
        result = self.svc.clean_batch(inputs)
        assert result == ['z z', 'a a', 'm m']