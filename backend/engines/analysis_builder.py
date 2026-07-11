"""
Strategic AI Core Backend
Analysis builder
"""


class AnalysisBuilder:
    def build(self, agent_name: str, reasoning_context: dict) -> dict:
        return {
            "agent": agent_name,
            "reasoning_context": reasoning_context,
        }
