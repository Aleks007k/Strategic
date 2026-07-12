"""
Strategic AI Core Backend
User clarification context
"""


class ClarificationContext:
    def __init__(self):
        self.questions = []
        self.answers = {}
        self.additional_information = {}

    def add_question(self, question) -> None:
        self.questions.append(question)

    def add_answer(self, question, answer) -> None:
        self.answers[question] = answer

    def add_information(self, key, value) -> None:
        self.additional_information[key] = value

    def to_dict(self) -> dict:
        return {
            "questions": list(self.questions),
            "answers": dict(self.answers),
            "additional_information": dict(self.additional_information),
        }
