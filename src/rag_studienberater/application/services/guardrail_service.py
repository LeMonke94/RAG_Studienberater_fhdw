# Imports
from ...domain.models import RetrievalResult


class GuardrailService:

    def __init__(self, min_score: float = 0.5, min_question_length: int = 10):
        self.min_score = min_score
        self.min_question_length = min_question_length

    def is_question_valid(self, question: str) -> bool:
        """Prüft, ob die Frage lang genug ist um sinnvoll verarbeitet zu werden."""
        return len(question.strip()) >= self.min_question_length

    def get_invalid_question_response(self) -> str:
        """Gibt eine Standardantwort zurück, wenn die Frage ungültig ist."""
        return 'Bitte stelle eine konkrete Frage zum Studium an der FHDW.'

    def has_sufficient_evidence(self, result: RetrievalResult) -> bool:
        """Prüft, ob genügend relevante Informationen für eine Antwort vorhanden sind."""

        if not result.scored_chunks:
            return False

        return any(sc.score >= self.min_score for sc in result.scored_chunks)

    def filter_chunks(self, result: RetrievalResult) -> RetrievalResult:
        """Gibt ein neues RetrievalResult zurück, das nur Chunks über dem min_score enthält."""
        filtered = [sc for sc in result.scored_chunks if sc.score >= self.min_score]
        return RetrievalResult(scored_chunks=filtered)

    def get_no_evidence_response(self) -> str:
        """Gibt eine Standardantwort zurück, wenn keine ausreichenden Informationen vorhanden sind."""

        return (
            'Dazu finde ich in den vorliegenden FHDW-Unterlagen leider nichts.'
            'Bitte wende dich direkt an die FHDW für weitere Informationen.'
        )