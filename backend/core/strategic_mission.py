"""
Strategic AI Core Backend
Strategic mission
"""


class StrategicMission:
    def __init__(self, question: str, goal=None, council=None, constraints: list = None):
        self.question = question
        self.goal = goal
        self.council = council
        self.constraints = list(constraints) if constraints else []

    def add_constraint(self, constraint: str) -> None:
        self.constraints.append(constraint)

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "goal": self._serialize(self.goal),
            "council": self._serialize(self.council),
            "constraints": list(self.constraints),
        }

    @staticmethod
    def _serialize(value):
        if hasattr(value, "to_dict"):
            return value.to_dict()
        return value
