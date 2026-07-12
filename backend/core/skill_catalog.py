"""
Strategic AI Core Backend
Skill catalog
"""

from core.skill_registry import SkillRegistry
from core.skill_definition import SkillDefinition


class SkillCatalog:
    def __init__(self):
        self.registry = SkillRegistry()

    def add_skill(self, skill_definition: SkillDefinition) -> None:
        self.registry.register(skill_definition.name, skill_definition)

    def get_skill(self, name: str):
        return self.registry.get_skill(name)

    def list_skills(self) -> list:
        return self.registry.list_skills()

    def load_default_skills(self) -> None:
        defaults = [
            SkillDefinition(
                name="Macro Economics",
                description="Analyzes large-scale economic indicators, monetary policy, and growth trends.",
                category="economics",
                methodology="Macroeconomic indicator analysis",
                use_cases=["inflation forecasting", "policy impact assessment"],
                limitations=["depends on data quality", "not predictive of shocks"],
            ),
            SkillDefinition(
                name="Geopolitical Analysis",
                description="Assesses political, territorial, and international relations dynamics.",
                category="geopolitics",
                methodology="Structured geopolitical risk assessment",
                use_cases=["conflict risk evaluation", "trade policy analysis"],
                limitations=["high uncertainty", "requires current intelligence"],
            ),
            SkillDefinition(
                name="Technology Trends",
                description="Tracks emerging technologies and their strategic implications.",
                category="technology",
                methodology="Trend and adoption curve analysis",
                use_cases=["innovation forecasting", "competitive positioning"],
                limitations=["fast-changing landscape", "hype cycle bias"],
            ),
            SkillDefinition(
                name="Game Theory",
                description="Models strategic interactions between rational decision-makers.",
                category="strategy",
                methodology="Formal game-theoretic modeling",
                use_cases=["negotiation strategy", "competitive response modeling"],
                limitations=["assumes rational actors", "simplifies real-world complexity"],
            ),
            SkillDefinition(
                name="Scenario Planning",
                description="Builds structured future scenarios to test strategic decisions.",
                category="strategy",
                methodology="Multi-scenario forecasting",
                use_cases=["long-term planning", "risk contingency design"],
                limitations=["scenario selection bias", "cannot predict exact outcomes"],
            ),
            SkillDefinition(
                name="Risk Analysis",
                description="Identifies, evaluates, and prioritizes strategic and financial risks.",
                category="risk",
                methodology="Structured risk assessment framework",
                use_cases=["risk prioritization", "mitigation planning"],
                limitations=["relies on available information", "cannot eliminate uncertainty"],
            ),
            SkillDefinition(
                name="Crowd Psychology",
                description="Examines collective behavior patterns and sentiment dynamics.",
                category="behavioral",
                methodology="Behavioral and sentiment pattern analysis",
                use_cases=["market sentiment analysis", "public reaction forecasting"],
                limitations=["patterns can shift rapidly", "not individually predictive"],
            ),
        ]

        for skill in defaults:
            self.add_skill(skill)
