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
