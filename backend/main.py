"""
Strategic AI Core Backend
Main entry point
"""

from datetime import datetime

from config import config
from core.orchestrator import Orchestrator
from agents.strategic_analyst import StrategicAnalyst
from agents.economic_analyst import EconomicAnalyst
from agents.technology_analyst import TechnologyAnalyst
from engines.analysis_engine import AnalysisEngine


def get_status():
    return {
        "project": config.get("project", {}).get("name", "Strategic"),
        "status": "running",
        "time": datetime.now().isoformat()
    }


def main():
    orchestrator = Orchestrator()
    orchestrator.register(StrategicAnalyst())
    orchestrator.register(EconomicAnalyst())
    orchestrator.register(TechnologyAnalyst())

    print(get_status())
    print(f"Registered agents: {list(orchestrator.agents.keys())}")

    question = "What should I focus on this quarter?"
    results = [orchestrator.run(agent_name, question) for agent_name in orchestrator.agents]
    for result in results:
        print(result)

    engine = AnalysisEngine()
    combined = engine.synthesize(results)
    print(combined)


if __name__ == "__main__":
    main()