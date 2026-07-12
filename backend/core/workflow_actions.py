"""
Strategic AI Core Backend
Workflow action map
"""


class WorkflowActions:
    def __init__(self):
        self.actions = {}

    def register(self, stage: str, action) -> None:
        self.actions[stage] = action

    def get_action(self, stage: str):
        return self.actions.get(stage)

    def list_actions(self) -> list:
        return list(self.actions.keys())

    def to_dict(self) -> dict:
        return {stage: self._serialize(action) for stage, action in self.actions.items()}

    @staticmethod
    def _serialize(action):
        if hasattr(action, "to_dict"):
            return action.to_dict()
        if callable(action):
            return getattr(action, "__name__", str(action))
        return action
