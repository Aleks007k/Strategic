"""
Strategic AI Core Backend
Main entry point
"""

from datetime import datetime

from config import config
from core.orchestrator import Orchestrator
from agents.strategic_analyst import StrategicAnalyst


def get_status():
    return {
        "project": config.get("project", {}).get("name", "Strategic"),
        "status": "running",
        "time": datetime.now().isoformat()
    }


def main():
    orchestrator = Orchestrator()
    orchestrator.register(StrategicAnalyst())

    print(get_status())
    print(f"Registered agents: {list(orchestrator.agents.keys())}")

    result = orchestrator.run("Strategic Analyst", "What should I focus on this quarter?")
    print(result)


if __name__ == "__main__":
    main()