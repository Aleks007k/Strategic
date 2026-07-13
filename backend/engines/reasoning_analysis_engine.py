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
            llm_input = {
                "agent": reasoning_package.get("agent"),
                "reasoning_context": {
                    "mission": reasoning_package.get("mission"),
                    "skills": reasoning_package.get("skills"),
                    "methodologies": reasoning_package.get("methodologies"),
                    "analysis_steps": reasoning_package.get("analysis_steps"),
                },
            }
            return self.llm_provider.generate_analysis(llm_input)

        if isinstance(reasoning_package, dict):
            agent_name = reasoning_package.get("agent")
        else:
            agent_name = getattr(reasoning_package, "agent", None)

        output = AnalysisResult().to_dict()
        output["agent"] = agent_name
        return output
