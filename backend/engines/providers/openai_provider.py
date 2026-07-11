"""
Strategic AI Core Backend
OpenAI LLM provider
"""

from engines.providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        raise NotImplementedError(
            "OpenAI integration not implemented yet."
        )
