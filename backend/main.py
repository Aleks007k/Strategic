"""
Strategic AI Core Backend
Main entry point
"""

from datetime import datetime

from config import config
from core.orchestrator import Orchestrator
from core.session import StrategicSession
from agents.strategic_analyst import StrategicAnalyst
from agents.economic_analyst import EconomicAnalyst
from agents.technology_analyst import TechnologyAnalyst


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

    print("Welcome to Strategic - your personal strategic intelligence assistant.")
    language = input("Choose language (ru/en) [default: ru]: ")
    question = input("Enter your question: ")
    session = StrategicSession(orchestrator)
    final_analysis = session.run(question, language=language)
    print(final_analysis)


if __name__ == "__main__":
    main()