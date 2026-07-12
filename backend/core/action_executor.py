"""
Strategic AI Core Backend
Workflow action executor
"""


class ActionExecutor:
    def __init__(self):
        self.handlers = {}

    def register(self, action_name: str, handler) -> None:
        self.handlers[action_name] = handler

    def execute(self, action_name: str, *args, **kwargs):
        handler = self.handlers.get(action_name)
        if handler is None or not callable(handler):
            return None

        return handler(*args, **kwargs)

    def list_actions(self) -> list:
        return list(self.handlers.keys())

    def to_dict(self) -> dict:
        return {action_name: self._serialize(handler) for action_name, handler in self.handlers.items()}

    @staticmethod
    def _serialize(handler):
        if hasattr(handler, "to_dict"):
            return handler.to_dict()
        if callable(handler):
            return getattr(handler, "__name__", str(handler))
        return handler
