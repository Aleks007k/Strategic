"""
Strategic AI Core Backend
User memory context
"""


class UserContext:
    def __init__(
        self,
        facts: list = None,
        preferences: list = None,
        constraints: list = None,
        previous_decisions: list = None,
        relevant_history: list = None,
    ):
        self.facts = list(facts) if facts else []
        self.preferences = list(preferences) if preferences else []
        self.constraints = list(constraints) if constraints else []
        self.previous_decisions = list(previous_decisions) if previous_decisions else []
        self.relevant_history = list(relevant_history) if relevant_history else []

    def add_fact(self, fact) -> None:
        self.facts.append(fact)

    def add_preference(self, preference) -> None:
        self.preferences.append(preference)

    def add_constraint(self, constraint) -> None:
        self.constraints.append(constraint)

    def add_decision(self, decision) -> None:
        self.previous_decisions.append(decision)

    def add_history(self, history_item) -> None:
        self.relevant_history.append(history_item)

    def to_dict(self) -> dict:
        return {
            "facts": list(self.facts),
            "preferences": list(self.preferences),
            "constraints": list(self.constraints),
            "previous_decisions": list(self.previous_decisions),
            "relevant_history": list(self.relevant_history),
        }
