"""
Strategic AI Core Backend
Strategic executor
"""

from core.analysis_session import AnalysisSession
from core.expert_catalog import ExpertCatalog
from core.council import Council
from core.strategic_workflow import StrategicWorkflow
from core.workflow_state import WorkflowState
from core.strategic_orchestrator import StrategicOrchestrator


class StrategicExecutor:
    def __init__(
        self,
        mission_builder=None,
        expert_selection_engine=None,
        reasoning_pipeline=None,
        strategic_synthesis_engine=None,
        input_analysis_engine=None,
    ):
        self.mission_builder = mission_builder
        self.expert_selection_engine = expert_selection_engine
        self.reasoning_pipeline = reasoning_pipeline
        self.strategic_synthesis_engine = strategic_synthesis_engine
        self.input_analysis_engine = input_analysis_engine

        # TODO: ExpertCatalog is a temporary expert source for wiring purposes.
        # It will later be replaced by a generic expert provider.
        self.expert_catalog = ExpertCatalog()
        self.expert_catalog.load_default_experts()

        self.strategic_orchestrator = StrategicOrchestrator(workflow=StrategicWorkflow())

    def execute(self, question: str) -> dict:
        session = AnalysisSession()
        session.workflow_state = WorkflowState()
        self.strategic_orchestrator.session = session

        if self.input_analysis_engine is not None:
            analysis_result = self.input_analysis_engine.analyze(question)
            information_gap = analysis_result.get("information_gap")
            session.workflow_state.data["input_analysis"] = {
                "question": analysis_result.get("question"),
                "context": analysis_result.get("context"),
                "goal": analysis_result.get("goal"),
                "information_gap": information_gap.to_dict() if hasattr(information_gap, "to_dict") else information_gap,
            }
            self.strategic_orchestrator.advance_stage("clarification")

        selection = {"selected_experts": []}
        council = Council()

        if self.expert_selection_engine is not None:
            candidates = [
                self.expert_catalog.get_expert(name)
                for name in self.expert_catalog.list_experts()
            ]
            selection = self.expert_selection_engine.select(question, candidates)

            for expert_name in selection.get("selected_experts", []):
                expert = self.expert_catalog.get_expert(expert_name)
                if expert is not None:
                    council.add_expert(expert)

        mission = None
        if self.mission_builder is not None:
            mission = self.mission_builder.build(question, council=council)
            session.mission = mission
            self.strategic_orchestrator.advance_stage("planning")

        if self.reasoning_pipeline is not None:
            session = self.reasoning_pipeline.prepare(session)
            self.strategic_orchestrator.advance_stage("agents")

        synthesis = {
            "experts_count": 0,
            "perspectives": [],
            "common_factors": [],
            "conflicting_factors": [],
            "combined_risks": [],
            "combined_opportunities": [],
            "confidence_summary": None,
        }
        if self.strategic_synthesis_engine is not None:
            synthesis = self.strategic_synthesis_engine.synthesize(list(session.results.values()))
            self.strategic_orchestrator.advance_stage("consensus")

        return {
            "question": question,
            "mission": mission.to_dict() if hasattr(mission, "to_dict") else mission,
            "selection": selection,
            "session": session.to_dict(),
            "synthesis": synthesis,
            "workflow_state": session.workflow_state.to_dict(),
        }
