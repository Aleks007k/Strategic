"""
Strategic AI Core Backend
Strategic session controller
"""

import json
from datetime import datetime

from core.orchestrator import Orchestrator
from engines.analysis_engine import AnalysisEngine
from memory.memory_manager import MemoryManager
from memory.memory_classifier import MemoryClassifier


class StrategicSession:
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.analysis_engine = AnalysisEngine()
        self.memory_manager = MemoryManager()
        self.memory_classifier = MemoryClassifier()

    def run(self, question: str) -> dict:
        results = [self.orchestrator.run(agent_name, question) for agent_name in self.orchestrator.agents]
        final_analysis = self.analysis_engine.synthesize(results)

        content = json.dumps(final_analysis, indent=2)
        category = self.memory_classifier.classify(content)
        filename = f"{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.memory_manager.save_memory(category, filename, content)

        return final_analysis
