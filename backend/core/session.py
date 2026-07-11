"""
Strategic AI Core Backend
Strategic session controller
"""

import json
from datetime import datetime

from core.orchestrator import Orchestrator
from core.context import UserContext
from core.analysis_context import AnalysisContext
from core.task_planner import TaskPlanner
from engines.analysis_engine import AnalysisEngine
from engines.response_engine import ResponseEngine
from engines.llm_engine import LLMEngine
from memory.memory_manager import MemoryManager
from memory.memory_classifier import MemoryClassifier
from memory.memory_retriever import MemoryRetriever
from knowledge.knowledge_loader import KnowledgeLoader
from language.language_manager import LanguageManager


class StrategicSession:
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.analysis_engine = AnalysisEngine()
        self.response_engine = ResponseEngine()
        self.llm_engine = LLMEngine()
        self.memory_manager = MemoryManager()
        self.memory_classifier = MemoryClassifier()
        self.memory_retriever = MemoryRetriever()
        self.knowledge_loader = KnowledgeLoader()
        self.language_manager = LanguageManager()
        self.task_planner = TaskPlanner()

    def run(self, question: str, language: str = None, context: UserContext = None) -> dict:
        if context is None:
            context = UserContext(language=self.language_manager.get_language(language))

        task_plan = self.task_planner.plan(question)

        recent_memory = self.memory_retriever.get_recent_memories()
        relevant_memory = self.memory_retriever.get_relevant_memories(question)
        domain_knowledge = {
            "economics": self.knowledge_loader.load_domain("economics"),
            "geopolitics": self.knowledge_loader.load_domain("geopolitics"),
            "technology": self.knowledge_loader.load_domain("technology"),
        }
        analysis_context = AnalysisContext(
            question=question,
            user_context=context,
            knowledge_context=domain_knowledge,
            recent_memory=recent_memory,
            relevant_memory=relevant_memory,
            goals=context.goals,
        )
        analysis_context.task_plan = task_plan

        results = list(
            self.orchestrator.run_all(
                analysis_context.question,
                context=analysis_context.user_context,
                analysis_context=analysis_context,
            ).values()
        )
        final_analysis = self.analysis_engine.synthesize(results)
        final_analysis["language"] = context.language
        final_analysis["user_preferences"] = {
            "tone": context.preferences.get("tone"),
            "detail_level": context.preferences.get("detail_level"),
            "focus_areas": context.preferences.get("focus_areas"),
        }
        final_analysis["response_text"] = self.response_engine.generate(final_analysis, context=context)

        content = json.dumps(final_analysis, indent=2)
        category = self.memory_classifier.classify(content)
        filename = f"{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.memory_manager.save_memory(category, filename, content)

        return final_analysis
