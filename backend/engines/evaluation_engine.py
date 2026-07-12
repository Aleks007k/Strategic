"""
Strategic AI Core Backend
Evaluation engine
"""


class EvaluationEngine:
    def evaluate(self, consensus: dict, decision: dict, review_context) -> dict:
        issues = []

        if not consensus:
            return {
                "ready": False,
                "issues": issues,
                "next_action": "collect_information",
            }

        confidence = consensus.get("confidence", 0)
        disagreements = consensus.get("disagreements", [])

        if disagreements:
            issues.append("Disagreements found among agents.")

        if confidence == 0:
            return {
                "ready": False,
                "issues": issues,
                "next_action": "review",
            }

        return {
            "ready": True,
            "issues": issues,
            "next_action": "continue",
        }
