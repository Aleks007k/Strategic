"""
Strategic AI Core Backend
Base agent interface
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    name: str = "base_agent"

    @abstractmethod
    def run(self, *args, **kwargs):
        """Execute the agent's task and return a result."""
        raise NotImplementedError
