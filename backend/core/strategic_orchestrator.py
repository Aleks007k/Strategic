"""
Strategic AI Core Backend
Strategic orchestrator
"""

from core.strategic_workflow import StrategicWorkflow
from core.workflow_state import WorkflowState


class StrategicOrchestrator:
    def __init__(self, workflow: StrategicWorkflow = None):
        self.workflow = workflow or StrategicWorkflow()
        self.session = None

    def start(self, session) -> None:
        self.session = session

        if getattr(session, "workflow_state", None) is None:
            session.workflow_state = WorkflowState()

        pipeline = self.workflow.get_pipeline()
        if pipeline:
            self.advance_stage(pipeline[0])

    def get_current_stage(self):
        if self.session is None or getattr(self.session, "workflow_state", None) is None:
            return None
        return self.session.workflow_state.current_stage

    def advance_stage(self, stage: str) -> None:
        if self.session is None or stage not in self.workflow.get_pipeline():
            return

        if getattr(self.session, "workflow_state", None) is None:
            self.session.workflow_state = WorkflowState()

        self.session.workflow_state.advance(stage)
