"""
Strategic AI Core Backend
Analysis synthesis engine
"""


class AnalysisEngine:
    def synthesize(self, agent_results: list) -> dict:
        perspectives = [
            {
                "agent": result.get("agent"),
                "summary": result.get("analysis", {}).get("summary"),
            }
            for result in agent_results
        ]

        recommendations = []
        for result in agent_results:
            recommendations.extend(result.get("analysis", {}).get("recommendations", []))

        return {
            "summary": f"Combined analysis from {len(agent_results)} agents.",
            "perspectives": perspectives,
            "risks": [],
            "recommendations": recommendations,
        }
