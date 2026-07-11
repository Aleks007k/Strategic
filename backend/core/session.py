"""
Strategic AI Core Backend
Strategic session controller
"""

import json
from datetime import datetime

from core.orchestrator import Orchestrator
from engines.analysis_engine import AnalysisEngine
from memory.memory_manager import MemoryManager


class StrategicSession:
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.analysis_engine = AnalysisEngine()
        self.memory_manager = MemoryManager()

    def run(self, question: str) -> dict:
        results = [self.orchestrator.run(agent_name, question) for agent_name in self.orchestrator.agents]
        final_analysis = self.analysis_engine.synthesize(results)

        filename = f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.memory_manager.save_memory("insights", filename, json.dumps(final_analysis, indent=2))

        return final_analysis
