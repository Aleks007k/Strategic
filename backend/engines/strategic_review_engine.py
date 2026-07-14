"""
Strategic AI Core Backend
Strategic review engine
"""


class StrategicReviewEngine:
    def review(self, synthesis: dict, readiness: dict) -> dict:
        synthesis = synthesis if isinstance(synthesis, dict) else {}
        readiness = readiness if isinstance(readiness, dict) else {}

        readiness_reasons = readiness.get("reasons") or []
        experts_count = synthesis.get("experts_count") or 0

        review_reasons = []

        if "no_experts" in readiness_reasons or experts_count < 2:
            review_reasons.append("insufficient expert coverage")

        if "missing_confidence" in readiness_reasons:
            review_reasons.append("missing confidence")

        if "conflicting_factors_present" in readiness_reasons:
            review_reasons.append("conflicting factors")

        if "low_factor_agreement" in readiness_reasons:
            review_reasons.append("low agreement")

        review_status = "approved" if not review_reasons else "needs_review"

        return {
            "review_status": review_status,
            "review_reasons": review_reasons,
        }
