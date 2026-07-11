"""
Strategic AI Core Backend
Ollama LLM provider
"""

from engines.providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        raise NotImplementedError(
            "Ollama integration not implemented yet."
        )
