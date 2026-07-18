"""
Strategic AI Core Backend
Reasoning package analysis engine
"""

import re

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
            mission = reasoning_package.get("mission", {})
            question = mission.get("question")
            goal = mission.get("goal")
            constraints = [
                c for c in mission.get("constraints", [])
                if isinstance(c, str) and c
            ]
            skills_list = [
                s for s in reasoning_package.get("skills", [])
                if isinstance(s, str) and s
            ]
            domain_knowledge = self._load_domain_knowledge(agent_name)

            # Internal scaffold for the future Hypothesis Layer (see
            # docs/STRATEGIC_HYPOTHESIS_LAYER.md). Deterministic; not yet
            # resolved, not sent to the provider, and not exposed in the
            # returned result.
            null_contradicting = []
            null_contradicting.extend(f"Specific constraint present: '{c}'." for c in constraints)
            null_contradicting.extend(f"Specific skill/lens present: '{s}'." for s in skills_list)
            if isinstance(goal, dict) and goal.get("name"):
                null_contradicting.append(f"Specific goal present: '{goal.get('name')}'.")
            null_supporting = [] if null_contradicting else [
                "No constraints, skills, or goal were specified, "
                "consistent with an undifferentiated baseline situation."
            ]

            hypotheses = [
                {
                    "statement": (
                        f"The situation described by '{question}' "
                        "does not differ materially from the current baseline; no unusual action is required."
                    ),
                    "status": self._evaluate_status(
                        null_supporting, null_contradicting, allow_contradiction_to_reject=False
                    ),
                    "supporting_evidence": null_supporting,
                    "contradicting_evidence": null_contradicting,
                }
            ]

            for constraint in constraints:
                constraint_supporting = self._find_supporting_evidence(constraint, question, domain_knowledge)
                constraint_contradicting = []
                hypotheses.append({
                    "statement": (
                        f"The outcome is primarily constrained by '{constraint}', and the situation "
                        "should be understood through this limiting factor rather than the baseline alone."
                    ),
                    "status": self._evaluate_status(constraint_supporting, constraint_contradicting),
                    "supporting_evidence": constraint_supporting,
                    "contradicting_evidence": constraint_contradicting,
                })

            for skill in skills_list:
                skill_supporting = self._find_supporting_evidence(skill, question, domain_knowledge)
                skill_contradicting = []
                hypotheses.append({
                    "statement": (
                        f"The expert perspective is primarily shaped by '{skill}', and the situation "
                        "should be examined through this analytical lens rather than the baseline alone."
                    ),
                    "status": self._evaluate_status(skill_supporting, skill_contradicting),
                    "supporting_evidence": skill_supporting,
                    "contradicting_evidence": skill_contradicting,
                })

            dominant_hypothesis, closest_rival_hypothesis = self._rank_hypotheses(hypotheses)

            # Internal scaffold for the future Causal Reasoning Layer (see
            # docs/STRATEGIC_HYPOTHESIS_LAYER.md). Deterministic; not yet
            # consulted by evidence/ranking, not sent to the provider, and
            # not exposed in the returned result.
            causal_graphs = [self._build_causal_graph(hypothesis) for hypothesis in hypotheses]

            llm_input = {
                "agent": agent_name,
                "reasoning_context": {
                    "mission": reasoning_package.get("mission"),
                    "skills": reasoning_package.get("skills"),
                    "methodologies": reasoning_package.get("methodologies"),
                    "analysis_steps": reasoning_package.get("analysis_steps"),
                    "question": question,
                    "goals": goal,
                    "constraints": mission.get("constraints"),
                    "time_horizon": reasoning_package.get("time_horizon"),
                    "expert_scope": reasoning_package.get("expert_scope"),
                    "decision_type": reasoning_package.get("decision_type"),
                    "domain_knowledge": domain_knowledge,
                },
            }
            result = self.llm_provider.generate_analysis(llm_input)
            result = result if isinstance(result, dict) else {}

            assumptions = list(result.get("assumptions") or [])
            if (
                dominant_hypothesis is not None
                and closest_rival_hypothesis is not None
                and dominant_hypothesis.get("status") == "surviving"
            ):
                hedge = (
                    f'Assumes: "{dominant_hypothesis.get("statement")}" '
                    f'rather than "{closest_rival_hypothesis.get("statement")}".'
                )
                if hedge not in assumptions:
                    assumptions.append(hedge)

            return {
                "agent": reasoning_package.get("agent"),
                "summary": result.get("summary"),
                "key_factors": result.get("key_factors", []),
                "risks": result.get("risks", []),
                "opportunities": result.get("opportunities", []),
                "assumptions": assumptions,
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

    @staticmethod
    def _evaluate_status(supporting_evidence, contradicting_evidence, allow_contradiction_to_reject=True) -> str:
        has_support = bool(supporting_evidence)
        has_contradiction = bool(contradicting_evidence)

        if allow_contradiction_to_reject and has_contradiction:
            return "rejected"
        if has_support and not has_contradiction:
            return "surviving"
        return "unresolved"

    @staticmethod
    def _score_hypothesis(hypothesis) -> float:
        status = hypothesis.get("status")
        supporting = hypothesis.get("supporting_evidence") or []
        contradicting = hypothesis.get("contradicting_evidence") or []

        status_weight = 1 if status == "surviving" else 0
        return status_weight + len(supporting) - len(contradicting)

    @classmethod
    def _rank_hypotheses(cls, hypotheses):
        candidates = [
            (index, hypothesis)
            for index, hypothesis in enumerate(hypotheses)
            if hypothesis.get("status") != "rejected"
        ]
        ranked = sorted(candidates, key=lambda pair: (-cls._score_hypothesis(pair[1]), pair[0]))

        dominant = ranked[0][1] if len(ranked) >= 1 else None
        closest_rival = ranked[1][1] if len(ranked) >= 2 else None
        return dominant, closest_rival

    @staticmethod
    def _build_causal_graph(hypothesis) -> dict:
        statement = hypothesis.get("statement")
        supporting = hypothesis.get("supporting_evidence") or []
        contradicting = hypothesis.get("contradicting_evidence") or []

        nodes = [statement]
        nodes.extend(supporting)
        nodes.extend(contradicting)

        edges = [
            {"from": evidence, "to": statement, "relation": "supports"}
            for evidence in supporting
        ]
        edges.extend(
            {"from": evidence, "to": statement, "relation": "contradicts"}
            for evidence in contradicting
        )

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def _extract_keywords(text) -> list:
        if not isinstance(text, str):
            return []
        words = re.findall(r"\w+", text.lower())
        keywords = [word for word in words if len(word) >= 3]
        return list(dict.fromkeys(keywords))

    @classmethod
    def _find_supporting_evidence(cls, subject, question, domain_knowledge) -> list:
        domain_text = domain_knowledge.lower() if isinstance(domain_knowledge, str) else ""
        question_text = question.lower() if isinstance(question, str) else ""

        evidence = []
        for keyword in cls._extract_keywords(subject):
            if domain_text and keyword in domain_text:
                evidence.append(f"Domain knowledge references '{keyword}'.")
            if question_text and keyword in question_text:
                evidence.append(f"The question directly references '{keyword}'.")

        return evidence
