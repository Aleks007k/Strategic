"""
Strategic AI Core Backend
Main entry point
"""

from datetime import datetime

from config import config
from core.orchestrator import Orchestrator
from core.session import StrategicSession
from core.context import UserContext
from core.user_profile import UserProfile
from agents.strategic_analyst import StrategicAnalyst
from agents.economic_analyst import EconomicAnalyst
from agents.technology_analyst import TechnologyAnalyst
from language.localization_manager import LocalizationManager
from language.language_manager import LanguageManager


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

    localization = LocalizationManager()
    language_manager = LanguageManager()

    print(localization.get_text("welcome_message"))
    language = language_manager.get_language(input(localization.get_text("language_prompt")))
    question = input(localization.get_text("question_prompt", language))

    user_id = "default_user"
    loaded_context = UserContext(language=language, user_id=user_id)
    profile = UserProfile(user_id=user_id, language=language, preferences=loaded_context.preferences)
    context = UserContext(profile=profile)

    session = StrategicSession(orchestrator)
    final_analysis = session.run(question, context=context)
    print(final_analysis)


if __name__ == "__main__":
    main()