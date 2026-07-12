"""
Strategic AI Core Backend
Analysis result
"""


class AnalysisResult:
    def __init__(
        self,
        summary: str = None,
        key_factors: list = None,
        risks: list = None,
        opportunities: list = None,
        assumptions: list = None,
        confidence: float = None,
    ):
        self.summary = summary
        self.key_factors = list(key_factors) if key_factors else []
        self.risks = list(risks) if risks else []
        self.opportunities = list(opportunities) if opportunities else []
        self.assumptions = list(assumptions) if assumptions else []
        self.confidence = confidence

    def to_dict(self) -> dict:
        return {
            "summary": self.summary,
            "key_factors": list(self.key_factors),
            "risks": list(self.risks),
            "opportunities": list(self.opportunities),
            "assumptions": list(self.assumptions),
            "confidence": self.confidence,
        }
