"""
Strategic AI Core Backend
LLM abstraction layer
"""

from engines.llm_router import LLMRouter
from engines.providers import PROVIDERS, MockProvider
from engines.usage_tracker import UsageTracker


class LLMEngine:
    def __init__(self):
        self.router = LLMRouter()
        self.usage_tracker = UsageTracker()
        self.provider_name = self.router.select_provider()
        provider_class = PROVIDERS.get(self.provider_name, MockProvider)
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
        try:
            return self.provider.generate_analysis(llm_input)
        except RuntimeError as primary_error:
            for fallback_name in self.router.get_provider_chain():
                if fallback_name == self.provider_name:
                    continue
                fallback_class = PROVIDERS.get(fallback_name)
                if fallback_class is None:
                    continue
                try:
                    return fallback_class().generate_analysis(llm_input)
                except RuntimeError:
                    continue
            raise primary_error
