# Imports
from ...domain.models import RetrievalResult


class GuardrailService:
    
    def __init__(self, min_score: float = 0.5):
        self.min_score = min_score

    def has_sufficient_evidence(self, result: RetrievalResult) -> bool:
        """Prüft, ob genügend relevante Informationen für eine Antwort vorhanden sind."""

        if not result.scored_chunks:
            return False
        
        return any(sc.score >= self.min_score for sc in result.scored_chunks)
    
    def get_no_evidence_response(self) -> str:
        """Gibt eine Standardantwort zurück, wenn keine ausreichenden Informationen vorhanden sind."""
        
        return (
            "Dazu finde ich in den vorliegenden FHDW-Unterlagen leider nichts. "
            "Bitte wende dich direkt an die FHDW für weitere Informationen."
        )