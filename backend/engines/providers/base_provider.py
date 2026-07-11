"""
Strategic AI Core Backend
Base LLM provider interface
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def generate_analysis(self, llm_input: dict) -> dict:
        raise NotImplementedError
