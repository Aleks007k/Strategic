"""
Strategic AI Core Backend
Agent profile
"""


class AgentProfile:
    def __init__(self, name: str, role: str = None, description: str = None, skills: list = None):
        self.name = name
        self.role = role
        self.description = description
        self.skills = []
        for skill in (skills or []):
            self.add_skill(skill)

    def add_skill(self, skill_name: str) -> None:
        if skill_name not in self.skills:
            self.skills.append(skill_name)

    def has_skill(self, skill_name: str) -> bool:
        return skill_name in self.skills

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "skills": list(self.skills),
        }
