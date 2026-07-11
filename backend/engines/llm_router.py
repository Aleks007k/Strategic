"""
Strategic AI Core Backend
LLM routing layer
"""

from config import llm_config

DEFAULT_PROVIDER = "mock"


class LLMRouter:
    def select_provider(self, task_type: str = None) -> str:
        return llm_config.get("provider", DEFAULT_PROVIDER)
