"""
Strategic AI Core Backend
Reasoning preparation pipeline
"""

from core.agent_execution import AgentExecution


class ReasoningPipeline:
    def __init__(self, skill_execution_engine, methodology_planner, reasoning_builder):
        self.skill_execution_engine = skill_execution_engine
        self.methodology_planner = methodology_planner
        self.reasoning_builder = reasoning_builder

    def prepare(self, session):
        mission = session.mission
        council = mission.council if mission is not None else None
        experts = council.list_experts() if council is not None else []

        for expert in experts:
            skill_result = self.skill_execution_engine.execute(expert, mission)
            execution = AgentExecution(
                agent=expert,
                mission=mission,
                skills_used=skill_result.get("skills_used"),
            )
            methodology_plan = self.methodology_planner.build(execution)
            reasoning_package = self.reasoning_builder.build(execution, methodology_plan)
            session.add_result(expert.name, reasoning_package)

        return session
