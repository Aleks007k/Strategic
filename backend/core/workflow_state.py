"""
Strategic AI Core Backend
Workflow state tracker
"""


class WorkflowState:
    def __init__(self):
        self.current_stage = None
        self.completed_stages = []
        self.data = {}

    def advance(self, stage: str) -> None:
        self.completed_stages.append(stage)
        self.current_stage = stage

    def has_completed(self, stage: str) -> bool:
        return stage in self.completed_stages

    def to_dict(self) -> dict:
        return {
            "current_stage": self.current_stage,
            "completed_stages": self.completed_stages,
            "data": self.data,
        }
