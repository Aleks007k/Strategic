"""
Strategic AI Core Backend
Task planner
"""

KEYWORD_MAP = {
    "economics": ["economy", "inflation", "salary", "market", "finance", "money"],
    "geopolitics": ["war", "country", "europe", "politics", "migration"],
    "technology": ["ai", "software", "technology", "future"],
    "personal_strategy": ["career", "business", "income", "life", "plan"],
}

TASK_DESCRIPTIONS = {
    "economics": "Analyze economic factors",
    "geopolitics": "Analyze geopolitical risks",
    "technology": "Analyze technological trends",
    "personal_strategy": "Analyze personal strategic considerations",
}

DEFAULT_DOMAINS = ["economics", "geopolitics", "technology"]


class TaskPlanner:
    def plan(self, question: str) -> list:
        lowered = (question or "").lower()

        matched_domains = [
            domain
            for domain, keywords in KEYWORD_MAP.items()
            if any(keyword in lowered for keyword in keywords)
        ]

        if not matched_domains:
            matched_domains = DEFAULT_DOMAINS

        return [
            {"domain": domain, "task": TASK_DESCRIPTIONS[domain]}
            for domain in matched_domains
        ]
