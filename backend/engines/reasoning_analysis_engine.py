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
                    "question": reasoning_package.get("mission", {}).get("question"),
                    "goals": reasoning_package.get("mission", {}).get("goal"),
                    "constraints": reasoning_package.get("mission", {}).get("constraints"),
                    "time_horizon": reasoning_package.get("time_horizon"),
                    "expert_scope": reasoning_package.get("expert_scope"),
                    "decision_type": reasoning_package.get("decision_type"),
                },
            }
            result = self.llm_provider.generate_analysis(llm_input)
            result = result if isinstance(result, dict) else {}

            return {
                "agent": reasoning_package.get("agent"),
                "summary": result.get("summary"),
                "key_factors": result.get("key_factors", []),
                "risks": result.get("risks", []),
                "opportunities": result.get("opportunities", []),
                "assumptions": result.get("assumptions", []),
                "confidence": result.get("confidence"),
            }

        if isinstance(reasoning_package, dict):
            agent_name = reasoning_package.get("agent")
        else:
            agent_name = getattr(reasoning_package, "agent", None)

        output = AnalysisResult().to_dict()
        output["agent"] = agent_name
        return output
