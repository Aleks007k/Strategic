"""
Strategic AI Core Backend
Strategic session controller
"""

import json
from datetime import datetime

from core.orchestrator import Orchestrator
from core.context import UserContext
from engines.analysis_engine import AnalysisEngine
from engines.response_engine import ResponseEngine
from memory.memory_manager import MemoryManager
from memory.memory_classifier import MemoryClassifier
from language.language_manager import LanguageManager


class StrategicSession:
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.analysis_engine = AnalysisEngine()
        self.response_engine = ResponseEngine()
        self.memory_manager = MemoryManager()
        self.memory_classifier = MemoryClassifier()
        self.language_manager = LanguageManager()

    def run(self, question: str, language: str = None, context: UserContext = None) -> dict:
        if context is None:
            context = UserContext(language=self.language_manager.get_language(language))

        results = list(self.orchestrator.run_all(question, context=context).values())
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
