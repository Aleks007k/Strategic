"""
Strategic AI Core Backend
Agent execution context
"""


class AgentExecution:
    def __init__(self, agent=None, mission=None, skills_used: list = None, instructions: str = None):
        self.agent = agent
        self.mission = mission
        self.skills_used = list(skills_used) if skills_used else []
        self.instructions = instructions

    def add_skill(self, skill) -> None:
        self.skills_used.append(skill)

    def to_dict(self) -> dict:
        return {
            "agent": self._serialize(self.agent),
            "mission": self._serialize(self.mission),
            "skills_used": [self._serialize(skill) for skill in self.skills_used],
            "instructions": self.instructions,
        }

    @staticmethod
    def _serialize(value):
        if hasattr(value, "to_dict"):
            return value.to_dict()
        return value
