"""
Strategic AI Core Backend
Reasoning builder
"""


class ReasoningBuilder:
    def build(self, agent_execution, methodology_plan) -> dict:
        mission = agent_execution.mission
        if hasattr(mission, "to_dict"):
            mission = mission.to_dict()

        return {
            "agent": agent_execution.agent.name,
            "mission": mission,
            "skills": list(agent_execution.skills_used),
            "methodologies": list(methodology_plan["methodologies"]),
            "analysis_steps": list(methodology_plan["analysis_steps"]),
        }
