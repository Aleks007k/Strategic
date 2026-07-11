"""
Strategic AI Core Backend
Anthropic LLM provider
"""

from config import ANTHROPIC_API_KEY
from engines.providers.base_provider import BaseProvider


class AnthropicProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        if not ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. "
                "Set this environment variable to use the Anthropic provider."
            )

        raise NotImplementedError("Anthropic API integration pending")
