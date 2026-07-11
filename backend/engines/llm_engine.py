"""
Strategic AI Core Backend
LLM abstraction layer
"""


class LLMEngine:
    def generate(self, reasoning_context: dict) -> dict:
        question = reasoning_context.get("question") if reasoning_context else None
        if question:
            summary = f"Mock LLM response for: {question}"
        else:
            summary = "Mock LLM response pending a question."

        return {
            "summary": summary,
            "key_factors": [],
            "risks": [],
            "opportunities": [],
            "recommendations": [],
        }

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
