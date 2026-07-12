"""
Strategic AI Core Backend
Expert evaluation
"""


class ExpertEvaluation:
    def __init__(
        self,
        expert_name: str = None,
        domain_relevance: float = None,
        skill_match: float = None,
        confidence: float = None,
        historical_accuracy: float = None,
        overall_weight: float = None,
    ):
        self.expert_name = expert_name
        self.domain_relevance = domain_relevance
        self.skill_match = skill_match
        self.confidence = confidence
        self.historical_accuracy = historical_accuracy
        self.overall_weight = overall_weight

    def calculate_weight(self) -> float:
        factors = [
            self.domain_relevance,
            self.skill_match,
            self.confidence,
            self.historical_accuracy,
        ]
        available = [factor for factor in factors if factor is not None]

        self.overall_weight = sum(available) / len(available) if available else None
        return self.overall_weight

    def to_dict(self) -> dict:
        return {
            "expert_name": self.expert_name,
            "domain_relevance": self.domain_relevance,
            "skill_match": self.skill_match,
            "confidence": self.confidence,
            "historical_accuracy": self.historical_accuracy,
            "overall_weight": self.overall_weight,
        }
