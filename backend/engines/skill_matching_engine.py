"""
Strategic AI Core Backend
Skill matching engine
"""

import re


class SkillMatchingEngine:
    def match(self, question: str, available_skills: list) -> dict:
        if not question or not available_skills:
            return {"matched_skills": []}

        keywords = self._extract_keywords(question)
        if not keywords:
            return {"matched_skills": []}

        matched_skills = []

        for skill in available_skills:
            name, searchable_text = self._extract_fields(skill)
            if not name:
                continue

            if any(keyword in searchable_text for keyword in keywords):
                matched_skills.append(name)

        return {"matched_skills": matched_skills}

    @staticmethod
    def _extract_keywords(question: str) -> list:
        words = re.findall(r"\w+", question.lower())
        keywords = [word for word in words if len(word) >= 3]
        return list(dict.fromkeys(keywords))

    @staticmethod
    def _extract_fields(skill):
        if isinstance(skill, str):
            return skill, skill.lower()

        name = getattr(skill, "name", None)
        description = getattr(skill, "description", None) or ""
        use_cases = getattr(skill, "use_cases", None) or []

        searchable_text = " ".join([name or "", description, " ".join(use_cases)]).lower()
        return name, searchable_text
