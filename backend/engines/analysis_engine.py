"""
Strategic AI Core Backend
Analysis synthesis engine
"""

from engines.output_validator import OutputValidator


class AnalysisEngine:
    def __init__(self):
        self.output_validator = OutputValidator()

    def synthesize(self, agent_results: list) -> dict:
        perspectives = []
        for result in agent_results:
            analysis = result.get("analysis", {})
            validation = self.output_validator.validate(analysis)
            perspectives.append({
                "agent": result.get("agent"),
                "summary": analysis.get("summary"),
                "valid": validation["valid"],
                "missing_fields": validation["missing_fields"],
            })

        risks = self._collect(agent_results, "risks")
        opportunities = self._collect(agent_results, "opportunities")
        recommendations = self._collect(agent_results, "recommendations")

        return {
            "summary": f"Combined analysis from {len(agent_results)} agents.",
            "perspectives": perspectives,
            "risks": risks,
            "opportunities": opportunities,
            "recommendations": recommendations,
            "strategic_view": self._build_strategic_view(agent_results, risks, opportunities, recommendations),
        }

    @staticmethod
    def _collect(agent_results: list, field: str) -> list:
        collected = []
        for result in agent_results:
            collected.extend(result.get("analysis", {}).get(field, []))
        return collected

    @staticmethod
    def _build_strategic_view(agent_results: list, risks: list, opportunities: list, recommendations: list) -> str:
        return (
            f"{len(agent_results)} perspectives combined: "
            f"{len(risks)} risk(s), {len(opportunities)} opportunity(ies), "
            f"{len(recommendations)} recommendation(s) identified."
        )
