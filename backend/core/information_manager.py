"""
Strategic AI Core Backend
Information manager
"""

from core.information_gap import InformationGap
from core.clarification_context import ClarificationContext


class InformationManager:
    def __init__(self, information_gap: InformationGap = None, clarification_context: ClarificationContext = None):
        self.information_gap = information_gap or InformationGap()
        self.clarification_context = clarification_context or ClarificationContext()

    def has_missing_information(self) -> bool:
        return self.information_gap.has_gaps()

    def add_question(self, question) -> None:
        self.information_gap.add_question(question)
        self.clarification_context.add_question(question)

    def add_answer(self, question, answer) -> None:
        self.clarification_context.add_answer(question, answer)

    def add_information(self, key, value) -> None:
        self.clarification_context.add_information(key, value)

    def get_context(self) -> dict:
        return self.clarification_context.to_dict()

    def to_dict(self) -> dict:
        return {
            "information_gap": self.information_gap.to_dict(),
            "clarification_context": self.clarification_context.to_dict(),
        }
