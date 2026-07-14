"""
Strategic AI Core Backend
Strategic session result
"""


class StrategicSessionResult:
    def __init__(
        self,
        question: str = None,
        mission=None,
        selected_experts: list = None,
        synthesis=None,
        readiness=None,
        response_text: str = None,
        workflow_state=None,
        timestamp: str = None,
        session_id: str = None,
    ):
        self.question = question
        self.mission = mission
        self.selected_experts = list(selected_experts) if selected_experts else []
        self.synthesis = synthesis
        self.readiness = readiness
        self.response_text = response_text
        self.workflow_state = workflow_state
        self.timestamp = timestamp
        self.session_id = session_id

    @classmethod
    def from_execute_result(cls, result: dict, timestamp: str = None, session_id: str = None) -> "StrategicSessionResult":
        result = result if isinstance(result, dict) else {}
        selection = result.get("selection") or {}

        return cls(
            question=result.get("question"),
            mission=result.get("mission"),
            selected_experts=selection.get("selected_experts", []),
            synthesis=result.get("synthesis"),
            readiness=result.get("readiness"),
            response_text=result.get("response_text"),
            workflow_state=result.get("workflow_state"),
            timestamp=timestamp,
            session_id=session_id,
        )

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "mission": self._serialize(self.mission),
            "selected_experts": list(self.selected_experts),
            "synthesis": self._serialize(self.synthesis),
            "readiness": self._serialize(self.readiness),
            "response_text": self.response_text,
            "workflow_state": self._serialize(self.workflow_state),
            "timestamp": self.timestamp,
            "session_id": self.session_id,
        }

    @staticmethod
    def _serialize(value):
        if hasattr(value, "to_dict"):
            return value.to_dict()
        return value
