"""
Strategic AI Core Backend
Inter-agent review context
"""

from engines.consensus_engine import ConsensusEngine


class ReviewContext:
    def __init__(self):
        self.analyses = {}
        self.comments = {}
        self.consensus = None

    def add_analysis(self, agent_name: str, analysis) -> None:
        self.analyses[agent_name] = analysis

    def add_comment(self, from_agent: str, to_agent: str, comment: str) -> None:
        self.comments.setdefault(to_agent, []).append({
            "from": from_agent,
            "comment": comment,
        })

    def build_consensus(self) -> dict:
        engine = ConsensusEngine()
        self.consensus = engine.find_consensus(self.analyses)
        return self.consensus

    def to_dict(self) -> dict:
        return {
            "analyses": self.analyses,
            "comments": self.comments,
            "consensus": self.consensus,
        }
