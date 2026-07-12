"""
Strategic AI Core Backend
Expert selection engine
"""

import re


class ExpertSelectionEngine:
    def select(self, question: str, experts: list) -> dict:
        if not question or not experts:
            return {"selected_experts": []}

        keywords = self._extract_keywords(question)
        if not keywords:
            return {"selected_experts": []}

        selected_experts = []

        for expert in experts:
            name = getattr(expert, "name", None)
            skills = getattr(expert, "skills", None) or []
            if not name:
                continue

            searchable_text = " ".join(skills).lower()
            if any(keyword in searchable_text for keyword in keywords):
                selected_experts.append(name)

        return {"selected_experts": selected_experts}

    @staticmethod
    def _extract_keywords(question: str) -> list:
        words = re.findall(r"\w+", question.lower())
        keywords = [word for word in words if len(word) >= 3]
        return list(dict.fromkeys(keywords))
