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
        recent_memory=None,
        relevant_memory=None,
        goals: list = None,
        review_context=None,
    ):
        self.question = question
        self.user_context = user_context
        self.knowledge_context = knowledge_context
        self.recent_memory = recent_memory
        self.relevant_memory = relevant_memory
        self.goals = goals or []
        self.review_context = review_context

    @property
    def memory_context(self):
        return self.recent_memory

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "user_context": self.user_context,
            "knowledge_context": self.knowledge_context,
            "recent_memory": self.recent_memory,
            "relevant_memory": self.relevant_memory,
            "goals": self.goals,
            "review_context": self.review_context,
        }
