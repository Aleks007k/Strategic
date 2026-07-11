"""
Strategic AI Core Backend
Mock LLM provider
"""

from engines.providers.base_provider import BaseProvider


class MockProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        agent_name = llm_input.get("agent")
        reasoning_context = llm_input.get("reasoning_context") or {}

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
