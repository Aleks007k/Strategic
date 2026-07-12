"""
Strategic AI Core Backend
Inter-agent review context
"""

from engines.consensus_engine import ConsensusEngine
from engines.review_engine import ReviewEngine
from engines.argument_engine import ArgumentEngine
from engines.debate_engine import DebateEngine


class ReviewContext:
    def __init__(self):
        self.analyses = {}
        self.comments = {}
        self.consensus = None
        self.arguments = None
        self.debates = None

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

    def build_reviews(self) -> dict:
        engine = ReviewEngine()
        result = engine.review(self.analyses)
        for to_agent, entries in result["comments"].items():
            for entry in entries:
                self.add_comment(entry["from"], to_agent, entry["comment"])
        return result

    def build_arguments(self) -> dict:
        engine = ArgumentEngine()
        self.arguments = engine.build_arguments(self.analyses)
        return self.arguments

    def build_debates(self) -> dict:
        engine = DebateEngine()
        self.debates = engine.debate(self.arguments, self.comments)
        return self.debates

    def to_dict(self) -> dict:
        return {
            "analyses": self.analyses,
            "comments": self.comments,
            "consensus": self.consensus,
            "arguments": self.arguments,
            "debates": self.debates,
        }
