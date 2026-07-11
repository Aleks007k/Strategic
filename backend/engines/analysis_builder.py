"""
Strategic AI Core Backend
Analysis builder
"""


class AnalysisBuilder:
    def build(self, agent_name: str, reasoning_context: dict) -> dict:
        question = reasoning_context.get("question")
        user_preferences = reasoning_context.get("user_preferences") or {}
        focus_areas = user_preferences.get("focus_areas") or []

        if question:
            summary = f"{agent_name} analysis for: {question}"
        else:
            summary = f"{agent_name} analysis pending a question."

        return {
            "agent": agent_name,
            "summary": summary,
            "key_factors": list(focus_areas),
            "risks": [],
            "opportunities": [],
            "recommendations": [],
        }
