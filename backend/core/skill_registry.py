"""
Strategic AI Core Backend
Skill registry
"""


class SkillRegistry:
    def __init__(self):
        self.skills = {}

    def register(self, skill_name: str, skill_description: str) -> None:
        self.skills[skill_name] = skill_description

    def get_skill(self, skill_name: str):
        return self.skills.get(skill_name)

    def list_skills(self) -> list:
        return list(self.skills.keys())

    def to_dict(self) -> dict:
        return dict(self.skills)
