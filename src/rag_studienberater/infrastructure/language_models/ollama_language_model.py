# Imports
from langchain_ollama import ChatOllama
from ...domain.ports import LanguageModelPort


class OllamaLanguageModel(LanguageModelPort):

    def __init__(self, model: str, base_url: str):
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
        )

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        
        if not response.content:
            raise ValueError("LLM hat keine Antwort zurückgegeben.")
        
        return str(response.content)