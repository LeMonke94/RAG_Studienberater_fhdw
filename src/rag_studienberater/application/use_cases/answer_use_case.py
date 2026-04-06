# Imports
from ...domain.models import Answer, Query
from ...domain.ports import LanguageModelPort
from ..services import GroundingService, GuardrailService
from .retrieval_use_case import RetrievalUseCase


class AnswerUseCase:

    def __init__(
            self,
            retrieval_use_case: RetrievalUseCase,
            grounding_service: GroundingService,
            guardrail_service: GuardrailService,
            llm: LanguageModelPort
        ):
        self.retrieval_use_case = retrieval_use_case
        self.grounding_service = grounding_service
        self.guardrail_service = guardrail_service
        self.language_model = llm

    def execute(self, question: str) -> Answer:
        """Nimmt eine Nutzerfrage an und gibt eine belegte Antwort zurück."""
        if not self.guardrail_service.is_question_valid(question):
            return Answer(
                text=self.guardrail_service.get_invalid_question_response(),
                sources=[],
                has_evidence=False,
            )

        query = Query(question=question)
        result = self.retrieval_use_case.execute(query)

        if not self.guardrail_service.has_sufficient_evidence(result):
            return Answer(
                text=self.guardrail_service.get_no_evidence_response(),
                sources=[],
                has_evidence=False,
            )

        filtered = self.guardrail_service.filter_chunks(result)
        prompt = self.grounding_service.build_prompt(query, filtered)
        answer_text = self.language_model.generate(prompt)

        return Answer(
            text=answer_text,
            sources=filtered.scored_chunks,
            has_evidence=True,
        )
