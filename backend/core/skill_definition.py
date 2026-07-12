"""
Strategic AI Core Backend
Skill definition
"""


class SkillDefinition:
    def __init__(
        self,
        name: str,
        description: str = None,
        category: str = None,
        methodology: str = None,
        use_cases: list = None,
        limitations: list = None,
    ):
        self.name = name
        self.description = description
        self.category = category
        self.methodology = methodology
        self.use_cases = list(use_cases) if use_cases else []
        self.limitations = list(limitations) if limitations else []

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "methodology": self.methodology,
            "use_cases": list(self.use_cases),
            "limitations": list(self.limitations),
        }
