"""
Strategic AI Core Backend
Task planner
"""


class TaskPlanner:
    def plan(self, question: str) -> list:
        return [
            {"domain": "economics", "task": "Analyze economic factors"},
            {"domain": "geopolitics", "task": "Analyze geopolitical risks"},
            {"domain": "technology", "task": "Analyze technological trends"},
        ]
