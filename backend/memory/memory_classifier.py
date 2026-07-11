"""
Strategic AI Core Backend
Memory classifier
"""

DECISION_KEYWORDS = ["decide", "decided", "decision", "chose", "choice", "plan to"]
INSIGHT_KEYWORDS = ["insight", "realized", "pattern", "trend", "learned", "discovered"]


class MemoryClassifier:
    def classify(self, text: str) -> str:
        lowered = text.lower()

        if any(keyword in lowered for keyword in DECISION_KEYWORDS):
            return "decisions"

        if any(keyword in lowered for keyword in INSIGHT_KEYWORDS):
            return "insights"

        return "conversations"
