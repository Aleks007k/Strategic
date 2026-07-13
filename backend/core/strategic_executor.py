"""
Strategic AI Core Backend
Strategic executor
"""

from core.analysis_session import AnalysisSession


class StrategicExecutor:
    def __init__(
        self,
        mission_builder=None,
        expert_selection_engine=None,
        reasoning_pipeline=None,
        strategic_synthesis_engine=None,
    ):
        self.mission_builder = mission_builder
        self.expert_selection_engine = expert_selection_engine
        self.reasoning_pipeline = reasoning_pipeline
        self.strategic_synthesis_engine = strategic_synthesis_engine

    def execute(self, question: str) -> dict:
        mission = None
        if self.mission_builder is not None:
            mission = self.mission_builder.build(question)

        selection = {"selected_experts": []}
        if self.expert_selection_engine is not None:
            selection = self.expert_selection_engine.select(question, [])

        session = AnalysisSession(mission=mission)
        if self.reasoning_pipeline is not None:
            session = self.reasoning_pipeline.prepare(session)

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

        return {
            "question": question,
            "mission": mission.to_dict() if hasattr(mission, "to_dict") else mission,
            "selection": selection,
            "session": session.to_dict(),
            "synthesis": synthesis,
        }
