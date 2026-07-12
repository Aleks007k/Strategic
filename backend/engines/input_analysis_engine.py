"""
Strategic AI Core Backend
Input analysis engine
"""

from core.information_gap import InformationGap


class InputAnalysisEngine:
    def analyze(self, question: str, context=None, goal=None) -> dict:
        information_gap = InformationGap()

        return {
            "question": question,
            "context": context,
            "goal": goal,
            "information_gap": information_gap,
        }
