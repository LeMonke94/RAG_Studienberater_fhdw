# Imports
from langchain_ollama import ChatOllama
from app.shared.domain.ports import LLMPort

# Ollama Adapter für LLMPort
class OllamaClient(LLMPort):

    def __init__(self, model: str = 'qwen2.5:7b'):
        self.llm = ChatOllama(model=model)

    # Prompt an das LLM
    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(input=prompt)
        return response.content