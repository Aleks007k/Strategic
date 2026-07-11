"""
Strategic AI Core Backend
Anthropic LLM provider
"""

from engines.providers.base_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        raise NotImplementedError(
            "Anthropic integration not implemented yet."
        )
