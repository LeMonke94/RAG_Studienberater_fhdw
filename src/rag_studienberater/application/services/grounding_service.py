# Imports
from textwrap import dedent

from ...domain.models import Query, RetrievalResult


class GroundingService:

    def build_prompt(self, query: Query, result: RetrievalResult) -> str:
        """Baut einen Prompt aus Nutzerfrage und Retrieval-Ergebnis."""

        context = self._format_context(result)

        prompt = dedent(
            f"""\
            Du bist ein hilfreicher Studienberater der FHDW.
            Beantworte die Frage ausschließlich auf Basis der folgenden Informationen aus den FHDW-Unterlagen.
            Wenn die Informationen nicht ausreichen, sage das ehrlich.
            Gib am Ende immer die Quellen an.

            INFORMATIONEN AUS DEN UNTERLAGEN:
            {context}

            FRAGE:
            {query.question}

            ANTWORT:
            """
        )
        return prompt
    
    def _format_context(self, result: RetrievalResult) -> str:
        """Formatiert die gefundenen Chunks als Kontext für den Prompt."""

        parts: list[str] = []

        for index, scored_chunk in enumerate(result.scored_chunks, start=1):
            chunk = scored_chunk.chunk

            if chunk.page is not None:
                header = f'[Quelle {index}: {chunk.source}, Seite {chunk.page}]'
            else:
                header = f'[Quelle {index}: {chunk.source}]'

            parts.append(f'{header}\n{chunk.text}')

        return "\n\n".join(parts)