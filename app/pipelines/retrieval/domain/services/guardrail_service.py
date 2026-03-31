# Imports
from app.shared.domain.models import RetrievalResult

# Guardrail service
class GuardrailService:

    def __init__(self, min_score: float = 0.7):
        self.min_score = min_score

    # Prüft ob Chunks evidenz haben
    def hat_ausreichend_evidenz(self, result: RetrievalResult) -> bool:
        if not result.hat_evidenz:
            return False
        return any(sc.score >= self.min_score for sc in result.chunks)
    
    # Antwort wenn keine Chunks
    def keine_evidenz_antwort(self) -> str:
        return (
            "Dazu finde ich in den vorliegenden FHDW-Unterlagen leider nichts. "
            "Bitte wende dich direkt an die FHDW für weitere Informationen."
        )