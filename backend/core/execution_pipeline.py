"""
Strategic AI Core Backend
Strategic execution pipeline
"""

from core.agent_execution import AgentExecution


class ExecutionPipeline:
    def __init__(self, skill_execution_engine):
        self.skill_execution_engine = skill_execution_engine

    def run(self, session):
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
            session.add_result(expert.name, execution)

        return session
