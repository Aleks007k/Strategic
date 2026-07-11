"""
Strategic AI Core Backend
Strategic Analyst agent
"""

from agents.base_agent import BaseAgent
from agents.agent_reasoning import AgentReasoning
from engines.analysis_builder import AnalysisBuilder
from engines.llm_engine import LLMEngine
from knowledge.knowledge_loader import KnowledgeLoader
from prompts.prompt_loader import PromptLoader


class StrategicAnalyst(BaseAgent):
    name = "Strategic Analyst"

    def __init__(self):
        self.knowledge_loader = KnowledgeLoader()
        self.prompt_loader = PromptLoader()
        self.agent_reasoning = AgentReasoning()
        self.analysis_builder = AnalysisBuilder()
        self.llm_engine = LLMEngine()

    def run(self, question: str, context=None, analysis_context=None) -> dict:
        knowledge_context = self.knowledge_loader.load_domain("geopolitics")
        prompt_context = self.prompt_loader.load_prompt("strategic_analyst")
        user_preferences = context.preferences if context else {}
        reasoning_context = self.agent_reasoning.build_analysis_context(
            analysis_context, prompt_context, knowledge_context, user_preferences
        )
        llm_input = self.analysis_builder.build(self.name, reasoning_context)
        analysis = self.llm_engine.generate_analysis(llm_input)

        return {
            "agent": self.name,
            "question": question,
            "knowledge_context": knowledge_context,
            "prompt_context": prompt_context,
            "user_preferences": user_preferences,
            "analysis_context": {
                "question": analysis_context.question if analysis_context else None,
                "memory_context": analysis_context.memory_context if analysis_context else None,
                "knowledge_context": analysis_context.knowledge_context if analysis_context else None,
            },
            "reasoning_context": reasoning_context,
            "analysis": analysis,
        }
