"""
Strategic AI Core Backend
Economic Analyst agent
"""

from agents.base_agent import BaseAgent
from knowledge.knowledge_loader import KnowledgeLoader
from prompts.prompt_loader import PromptLoader


class EconomicAnalyst(BaseAgent):
    name = "Economic Analyst"

    def __init__(self):
        self.knowledge_loader = KnowledgeLoader()
        self.prompt_loader = PromptLoader()

    def run(self, question: str, context=None) -> dict:
        knowledge_context = self.knowledge_loader.load_domain("economics")
        prompt_context = self.prompt_loader.load_prompt("economic_analyst")
        user_preferences = context.preferences if context else {}

        return {
            "agent": self.name,
            "question": question,
            "knowledge_context": knowledge_context,
            "prompt_context": prompt_context,
            "user_preferences": user_preferences,
            "analysis": {
                "summary": "Analysis not yet implemented.",
                "economic_factors": [],
                "risks": [],
                "opportunities": [],
            },
        }
