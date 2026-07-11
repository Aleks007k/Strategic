"""
Strategic AI Core Backend
Analysis context builder
"""


class AnalysisContext:
    def __init__(
        self,
        question: str,
        user_context=None,
        knowledge_context=None,
        memory_context=None,
        goals: list = None,
    ):
        self.question = question
        self.user_context = user_context
        self.knowledge_context = knowledge_context
        self.memory_context = memory_context
        self.goals = goals or []

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "user_context": self.user_context,
            "knowledge_context": self.knowledge_context,
            "memory_context": self.memory_context,
            "goals": self.goals,
        }
