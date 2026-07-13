"""
Strategic AI Core Backend
Input analysis engine
"""

from core.information_gap import InformationGap

REQUIRED_INFORMATION = [
    "budget",
    "timeframe",
    "risk tolerance",
    "priorities",
    "success criteria",
]

CONTEXT_FIELDS = [
    "facts",
    "preferences",
    "constraints",
    "previous_decisions",
    "relevant_history",
]


class InputAnalysisEngine:
    def analyze(self, question: str, context=None, goal=None) -> dict:
        information_gap = InformationGap()
        known_text = self._build_known_text(context)

        for item in REQUIRED_INFORMATION:
            if item not in known_text:
                information_gap.add_missing_information(item)

        return {
            "question": question,
            "context": context,
            "goal": goal,
            "information_gap": information_gap,
        }

    @staticmethod
    def _build_known_text(context) -> str:
        if not isinstance(context, dict):
            return ""

        values = []
        for field in CONTEXT_FIELDS:
            values.extend(context.get(field) or [])

        return " ".join(str(value) for value in values).lower()
