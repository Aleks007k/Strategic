"""
Strategic AI Core Backend
Strategic goal
"""


class StrategicGoal:
    def __init__(self, name: str, description: str = None, priority: str = None, criteria: list = None):
        self.name = name
        self.description = description
        self.priority = priority
        self.criteria = list(criteria) if criteria else []

    def add_criterion(self, criterion: str) -> None:
        self.criteria.append(criterion)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "criteria": list(self.criteria),
        }
