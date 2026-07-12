"""
Strategic AI Core Backend
Skill registry
"""


class SkillRegistry:
    def __init__(self):
        self.skills = {}

    def register(self, skill_name: str, skill_description) -> None:
        self.skills[skill_name] = skill_description

    def get_skill(self, skill_name: str):
        return self.skills.get(skill_name)

    def list_skills(self) -> list:
        return list(self.skills.keys())

    def to_dict(self) -> dict:
        return {
            name: (skill.to_dict() if hasattr(skill, "to_dict") else skill)
            for name, skill in self.skills.items()
        }
