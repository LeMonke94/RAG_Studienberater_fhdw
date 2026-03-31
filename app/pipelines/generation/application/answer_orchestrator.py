# Imports
from app.shared.domain.models import Answer
from app.shared.domain.ports import LLMPort
from app.pipelines.retrieval.application.retrieval_orchestrator import RetrievalOrchestrator
from app.pipelines.generation.domain.services.grounding_service import GroundingService
from app.pipelines.retrieval.domain.services.guardrail_service import GuardrailService

# Generation Pipeline zusammenstellen
class AnswerOrchestrator:

    def __init__(self, retrieval: RetrievalOrchestrator, grounding: GroundingService, guardrail: GuardrailService, llm: LLMPort):
        self.retrieval = retrieval
        self.grounding = grounding
        self.guardrail = guardrail
        self.llm = llm

    def run_anwer(self, frage: str) -> Answer:
        """Nimmt eine Nutzerfrage und gibt eine belegte Antwort zurück."""

        # Relevante Chunks holen
        result = self.retrieval.run_retrieve(frage)

        # Keine Evidenz → direkt zurückgeben
        if not result.hat_evidenz:
            return Answer(
                antwort_text=self.guardrail.get_no_evidence_response(),
                quellen=[],
                hat_evidenz=False,
            )
        
        # Prompt bauen
        prompt = self.grounding.build_prompt(frage, result)

        # LLM Aufrufen
        antwort_text = self.llm.generate(prompt)

        # Antwort zurückgeben
        return Answer(
            antwort_text=antwort_text,
            quellen=[sc.chunk for sc in result.chunks],
            hat_evidenz=True,
        )