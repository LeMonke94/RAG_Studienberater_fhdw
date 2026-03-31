# Imports
from app.shared.domain.models import RetrievalResult

# Grounding Service
class GroundingService:

    # Prompt String vorbereiten
    def build_prompt(self, frage: str, result: RetrievalResult) -> str:
        kontext = self._format_chunks(result)

        prompt = f"""
        Du bist ein hilfreicher Studienberater der FHDW.
        Beantworte die Frage ausschließlich auf Basis der folgenden Informationen aus den FHDW-Unterlagen.
        Wenn die Informationen nicht ausreichen, sage das ehrlich.
        Gib am Ende immer die Quellen an.

        INFORMATIONEN AUS DEN UNTERLAGEN:
        {kontext}

        FRAGE:
        {frage}

        ANTWORT:"""

    def _format_chunks(self, result: RetrievalResult) -> str:
        teile = []
        for i, scored_chunk in enumerate(result.chunks):
            teil = (
                f"[Quelle {i + 1}: {scored_chunk.chunk.quelle}, "
                f"Seite {scored_chunk.chunk.seite}]\n"
                f"{scored_chunk.chunk.text}"
            )
            teile.append(teil)
        return "\n\n".join(teile)