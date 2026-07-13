"""
Strategic AI Core Backend
Strategic synthesis engine
"""


class StrategicSynthesisEngine:
    def synthesize(self, analysis_results: list) -> dict:
        results = analysis_results or []

        perspectives = []
        combined_risks = []
        combined_opportunities = []
        confidence_values = []
        factor_counts = {}
        valid_expert_count = 0

        for result in results:
            if not isinstance(result, dict):
                continue
            valid_expert_count += 1

            perspectives.append({
                "agent": result.get("agent"),
                "summary": result.get("summary"),
                "confidence": result.get("confidence"),
            })
            combined_risks.extend(result.get("risks") or [])
            combined_opportunities.extend(result.get("opportunities") or [])

            confidence = result.get("confidence")
            if isinstance(confidence, (int, float)) and not isinstance(confidence, bool):
                confidence_values.append(confidence)

            seen_factors = set()
            for factor in (result.get("key_factors") or []):
                if factor in seen_factors:
                    continue
                seen_factors.add(factor)
                factor_counts[factor] = factor_counts.get(factor, 0) + 1

        confidence_summary = sum(confidence_values) / len(confidence_values) if confidence_values else None

        common_factors = [factor for factor, count in factor_counts.items() if count >= 2]
        if valid_expert_count >= 2:
            conflicting_factors = [factor for factor, count in factor_counts.items() if count == 1]
        else:
            conflicting_factors = []

        factor_agreement = [
            {"factor": factor, "agreement_score": count / valid_expert_count}
            for factor, count in factor_counts.items()
        ] if valid_expert_count > 0 else []

        return {
            "experts_count": len(results),
            "perspectives": perspectives,
            "common_factors": common_factors,
            "conflicting_factors": conflicting_factors,
            "combined_risks": combined_risks,
            "combined_opportunities": combined_opportunities,
            "confidence_summary": confidence_summary,
            "factor_agreement": factor_agreement,
        }
