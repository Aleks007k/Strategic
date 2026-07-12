"""
Strategic AI Core Backend
Expert profile catalog
"""

from core.agent_profile import AgentProfile
from core.skill_catalog import SkillCatalog


class ExpertCatalog:
    def __init__(self):
        self.experts = {}

    def add_expert(self, profile: AgentProfile) -> None:
        self.experts[profile.name] = profile

    def get_expert(self, name: str):
        return self.experts.get(name)

    def list_experts(self) -> list:
        return list(self.experts.keys())

    def load_default_experts(self) -> None:
        skill_catalog = SkillCatalog()
        skill_catalog.load_default_skills()

        experts = [
            self._build_expert(
                skill_catalog,
                name="Economic Strategist",
                role="Economic analysis and forecasting",
                description="Evaluates economic conditions and forecasts strategic economic implications.",
                skill_names=["Macro Economics", "Risk Analysis", "Crowd Psychology"],
            ),
            self._build_expert(
                skill_catalog,
                name="Geopolitical Strategist",
                role="Geopolitical risk and international relations",
                description="Assesses geopolitical dynamics and their strategic implications.",
                skill_names=["Geopolitical Analysis", "Game Theory", "Scenario Planning"],
            ),
            self._build_expert(
                skill_catalog,
                name="Technology Strategist",
                role="Technology trend analysis",
                description="Tracks emerging technology and its strategic impact.",
                skill_names=["Technology Trends", "Scenario Planning", "Risk Analysis"],
            ),
        ]

        for expert in experts:
            self.add_expert(expert)

    @staticmethod
    def _build_expert(
        skill_catalog: SkillCatalog,
        name: str,
        role: str,
        description: str,
        skill_names: list,
    ) -> AgentProfile:
        valid_skill_names = [
            skill_name
            for skill_name in skill_names
            if skill_catalog.get_skill(skill_name) is not None
        ]
        return AgentProfile(name=name, role=role, description=description, skills=valid_skill_names)
