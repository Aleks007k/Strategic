"""
Strategic AI Core Backend
Analysis session
"""


class AnalysisSession:
    def __init__(
        self,
        mission=None,
        council=None,
        workflow_state=None,
        results: dict = None,
        status: str = None,
    ):
        self.mission = mission
        self.council = council
        self.workflow_state = workflow_state
        self.results = dict(results) if results else {}
        self.status = status

    def add_result(self, key, value) -> None:
        self.results[key] = value

    def update_status(self, status: str) -> None:
        self.status = status

    def to_dict(self) -> dict:
        return {
            "mission": self._serialize(self.mission),
            "council": self._serialize(self.council),
            "workflow_state": self._serialize(self.workflow_state),
            "results": {key: self._serialize(value) for key, value in self.results.items()},
            "status": self.status,
        }

    @staticmethod
    def _serialize(value):
        if hasattr(value, "to_dict"):
            return value.to_dict()
        return value
