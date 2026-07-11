"""
Strategic AI Core Backend
LLM abstraction layer
"""

from config import llm_config
from engines.providers import PROVIDERS, MockProvider


class LLMEngine:
    def __init__(self):
        provider_name = llm_config.get("provider", "mock")
        provider_class = PROVIDERS.get(provider_name, MockProvider)
        self.provider = provider_class()

    def generate(self, reasoning_context: dict) -> dict:
        question = reasoning_context.get("question") if reasoning_context else None
        if question:
            summary = f"Mock LLM response for: {question}"
        else:
            summary = "Mock LLM response pending a question."

        return {
            "summary": summary,
            "key_factors": [],
            "risks": [],
            "opportunities": [],
            "recommendations": [],
        }

    def generate_analysis(self, llm_input: dict) -> dict:
        return self.provider.generate_analysis(llm_input)
