"""
Strategic AI Core Backend
Mock LLM provider
"""

from engines.providers.base_provider import BaseProvider


class MockProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        agent_name = llm_input.get("agent")
        reasoning_context = llm_input.get("reasoning_context") or {}

        question = reasoning_context.get("question")
        user_preferences = reasoning_context.get("user_preferences") or {}
        focus_areas = user_preferences.get("focus_areas") or []
        skills = reasoning_context.get("skills") or []
        goals = reasoning_context.get("goals")
        constraints = reasoning_context.get("constraints") or []

        if question:
            summary = f"{agent_name} analysis for: {question}"
        else:
            summary = f"{agent_name} analysis pending a question."

        key_factors = []
        for factor in list(focus_areas) + list(skills):
            if factor not in key_factors:
                key_factors.append(factor)

        goal_label = self._describe_goal(goals)
        if goal_label and goal_label not in key_factors:
            key_factors.append(goal_label)

        risks = [f"Risk: {factor} may not develop as expected." for factor in key_factors]
        opportunities = [f"Opportunity: {factor} could exceed expectations." for factor in key_factors]

        for constraint in constraints:
            risks.append(f"Risk: constraint '{constraint}' may limit available options.")

        assumptions = [f"Assumes constraint '{constraint}' remains unchanged." for constraint in constraints]
        if question:
            assumptions.append(f"Assumes conditions relevant to '{question}' remain stable.")
        if not assumptions:
            assumptions.append("Assumes no significant unexpected changes occur.")

        confidence = 0.5
        if key_factors:
            confidence += 0.15
        if constraints:
            confidence += 0.15
        if goal_label:
            confidence += 0.1
        confidence = round(min(confidence, 0.9), 2)

        return {
            "agent": agent_name,
            "summary": summary,
            "key_factors": key_factors,
            "risks": risks,
            "opportunities": opportunities,
            "recommendations": [],
            "assumptions": assumptions,
            "confidence": confidence,
        }

    @staticmethod
    def _describe_goal(goals):
        if isinstance(goals, dict):
            return goals.get("name")
        if isinstance(goals, list) and goals:
            first = goals[0]
            if isinstance(first, dict):
                return first.get("name") or first.get("description")
            return str(first)
        if isinstance(goals, str):
            return goals
        return None
