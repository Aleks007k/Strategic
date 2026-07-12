"""
Strategic AI Core Backend
Inter-agent review context
"""


class ReviewContext:
    def __init__(self):
        self.analyses = {}
        self.comments = {}

    def add_analysis(self, agent_name: str, analysis) -> None:
        self.analyses[agent_name] = analysis

    def add_comment(self, from_agent: str, to_agent: str, comment: str) -> None:
        self.comments.setdefault(to_agent, []).append({
            "from": from_agent,
            "comment": comment,
        })
