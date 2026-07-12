"""
Strategic AI Core Backend
Reasoning package analysis engine
"""

from core.analysis_result import AnalysisResult


class AnalysisEngine:
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider

    def analyze(self, reasoning_package) -> dict:
        if self.llm_provider is not None:
            return self.llm_provider.generate_analysis(reasoning_package)

        if isinstance(reasoning_package, dict):
            agent_name = reasoning_package.get("agent")
        else:
            agent_name = getattr(reasoning_package, "agent", None)

        output = AnalysisResult().to_dict()
        output["agent"] = agent_name
        return output
