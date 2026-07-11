"""
Strategic AI Core Backend
LLM routing layer
"""

from config import llm_config

DEFAULT_PROVIDER = "mock"
DEFAULT_PROVIDER_CHAIN = ["ollama", "mock"]


class LLMRouter:
    def select_provider(self, task_type: str = None) -> str:
        return llm_config.get("provider", DEFAULT_PROVIDER)

    def get_provider_chain(self) -> list:
        return llm_config.get("fallback_providers", DEFAULT_PROVIDER_CHAIN)
