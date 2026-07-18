"""
Strategic AI Core Backend
Reasoning package analysis engine
"""

from core.analysis_result import AnalysisResult
from knowledge.knowledge_loader import KnowledgeLoader

# Mirrors the domain each legacy agent is hardcoded to load
# (StrategicAnalyst -> geopolitics, EconomicAnalyst -> economics,
# TechnologyAnalyst -> technology), applied to the new pipeline's
# default expert names.
EXPERT_DOMAIN_MAP = {
    "Economic Strategist": "economics",
    "Geopolitical Strategist": "geopolitics",
    "Technology Strategist": "technology",
}


class AnalysisEngine:
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider
        self.knowledge_loader = KnowledgeLoader()

    def analyze(self, reasoning_package) -> dict:
        if self.llm_provider is not None:
            agent_name = reasoning_package.get("agent")

            # Internal scaffold for the future Hypothesis Layer (see
            # docs/STRATEGIC_HYPOTHESIS_LAYER.md). Deterministic and empty
            # by default; not yet populated, not sent to the provider, and
            # not exposed in the returned result.
            hypotheses = [
                {
                    "statement": "",
                    "status": "unresolved",
                    "supporting_evidence": [],
                    "contradicting_evidence": [],
                }
            ]

            llm_input = {
                "agent": agent_name,
                "reasoning_context": {
                    "mission": reasoning_package.get("mission"),
                    "skills": reasoning_package.get("skills"),
                    "methodologies": reasoning_package.get("methodologies"),
                    "analysis_steps": reasoning_package.get("analysis_steps"),
                    "question": reasoning_package.get("mission", {}).get("question"),
                    "goals": reasoning_package.get("mission", {}).get("goal"),
                    "constraints": reasoning_package.get("mission", {}).get("constraints"),
                    "time_horizon": reasoning_package.get("time_horizon"),
                    "expert_scope": reasoning_package.get("expert_scope"),
                    "decision_type": reasoning_package.get("decision_type"),
                    "domain_knowledge": self._load_domain_knowledge(agent_name),
                },
            }
            result = self.llm_provider.generate_analysis(llm_input)
            result = result if isinstance(result, dict) else {}

            return {
                "agent": reasoning_package.get("agent"),
                "summary": result.get("summary"),
                "key_factors": result.get("key_factors", []),
                "risks": result.get("risks", []),
                "opportunities": result.get("opportunities", []),
                "assumptions": result.get("assumptions", []),
                "confidence": result.get("confidence"),
            }

        if isinstance(reasoning_package, dict):
            agent_name = reasoning_package.get("agent")
        else:
            agent_name = getattr(reasoning_package, "agent", None)

        output = AnalysisResult().to_dict()
        output["agent"] = agent_name
        return output

    def _load_domain_knowledge(self, agent_name):
        domain_name = EXPERT_DOMAIN_MAP.get(agent_name)
        if domain_name is None:
            return None

        try:
            return self.knowledge_loader.load_domain(domain_name)
        except OSError:
            return None
