"""
Strategic AI Core Backend
Information gap detector
"""


class InformationGap:
    def __init__(self, missing_information: list = None, questions: list = None):
        self.missing_information = list(missing_information) if missing_information else []
        self.questions = list(questions) if questions else []

    def add_missing_information(self, item) -> None:
        self.missing_information.append(item)

    def add_question(self, question) -> None:
        self.questions.append(question)

    def has_gaps(self) -> bool:
        return bool(self.missing_information) or bool(self.questions)

    def to_dict(self) -> dict:
        return {
            "missing_information": list(self.missing_information),
            "questions": list(self.questions),
        }
