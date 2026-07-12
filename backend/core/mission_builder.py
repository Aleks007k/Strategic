"""
Strategic AI Core Backend
Mission builder
"""

from core.strategic_mission import StrategicMission


class MissionBuilder:
    def build(self, question: str, goal=None, council=None, constraints: list = None) -> StrategicMission:
        return StrategicMission(
            question=question,
            goal=goal,
            council=council,
            constraints=constraints,
        )
