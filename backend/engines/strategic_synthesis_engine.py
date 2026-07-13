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
        for result in results:
            if not isinstance(result, dict):
                continue
            perspectives.append({
                "agent": result.get("agent"),
                "summary": result.get("summary"),
                "confidence": result.get("confidence"),
            })
            combined_risks.extend(result.get("risks") or [])
            combined_opportunities.extend(result.get("opportunities") or [])

        return {
            "experts_count": len(results),
            "perspectives": perspectives,
            "common_factors": [],
            "conflicting_factors": [],
            "combined_risks": combined_risks,
            "combined_opportunities": combined_opportunities,
            "confidence_summary": None,
        }
