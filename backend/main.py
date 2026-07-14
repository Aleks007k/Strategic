"""
Strategic AI Core Backend
Main entry point
"""

from datetime import datetime

from config import config
from core.orchestrator import Orchestrator
from core.session import StrategicSession
from core.context import UserContext
from core.user_context import UserContext as MemoryUserContext
from core.user_profile import UserProfile
from core.strategic_executor import StrategicExecutor
from core.information_manager import InformationManager
from core.reasoning_pipeline import ReasoningPipeline
from engines.input_analysis_engine import InputAnalysisEngine
from engines.skill_execution_engine import SkillExecutionEngine
from engines.methodology_planner import MethodologyPlanner
from engines.reasoning_builder import ReasoningBuilder
from engines.reasoning_analysis_engine import AnalysisEngine
from engines.strategic_synthesis_engine import StrategicSynthesisEngine
from engines.providers.mock_provider import MockProvider
from preferences.preferences_manager import PreferencesManager
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

    stored_memory = PreferencesManager().load_preferences(user_id)
    memory_context = MemoryUserContext(
        facts=stored_memory.get("facts"),
        preferences=stored_memory.get("preferences"),
        constraints=stored_memory.get("constraints"),
        previous_decisions=stored_memory.get("previous_decisions"),
        relevant_history=stored_memory.get("relevant_history"),
    )
    information_manager = InformationManager()
    strategic_executor = StrategicExecutor(
        reasoning_pipeline=ReasoningPipeline(SkillExecutionEngine(), MethodologyPlanner(), ReasoningBuilder()),
        analysis_engine=AnalysisEngine(
            llm_provider=MockProvider()
        ),
        user_context=memory_context,
        information_manager=information_manager,
    )

    executor_result = strategic_executor.execute(question)
    clarification = executor_result.get("workflow_state", {}).get("data", {}).get("clarification", {})
    for clarification_question in clarification.get("questions", []):
        print(clarification_question)
        answer = input(f"{clarification_question} ")
        information_manager.add_answer(clarification_question, answer)

    field_targets = {
        "facts": (memory_context.facts, memory_context.add_fact),
        "preferences": (memory_context.preferences, memory_context.add_preference),
        "constraints": (memory_context.constraints, memory_context.add_constraint),
        "previous_decisions": (memory_context.previous_decisions, memory_context.add_decision),
        "relevant_history": (memory_context.relevant_history, memory_context.add_history),
    }
    for answered_question, answered_value in information_manager.clarification_context.answers.items():
        field = InputAnalysisEngine.map_question_to_field(answered_question)
        target_list, add_to_field = field_targets.get(field, (None, None))
        if target_list is not None and answered_value not in target_list:
            add_to_field(answered_value)

    preferences_manager = PreferencesManager()
    updated_preferences = preferences_manager.load_preferences(user_id)
    updated_preferences.update(memory_context.to_dict())
    preferences_manager.save_preferences(user_id, updated_preferences)

    print("New pipeline output (test)")
    print(StrategicSynthesisEngine().format_response(executor_result.get("synthesis", {})))

    readiness = executor_result.get("readiness", {}) or {}
    print("")
    print("Readiness:")
    print(f"- Ready: {readiness.get('ready')}")
    print(f"- Needs review: {readiness.get('needs_review')}")
    reasons = readiness.get("reasons") or []
    print(f"- Reasons: {', '.join(reasons) if reasons else '-'}")

    session = StrategicSession(orchestrator)
    final_analysis = session.run(question, context=context)
    print(final_analysis)


if __name__ == "__main__":
    main()