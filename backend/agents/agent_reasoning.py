"""
Strategic AI Core Backend
Shared agent reasoning helper
"""


class AgentReasoning:
    def build_analysis_context(self, analysis_context, prompt_context, knowledge_context, user_preferences) -> dict:
        return {
            "question": analysis_context.question if analysis_context else None,
            "instructions": prompt_context,
            "knowledge": knowledge_context,
            "recent_memory": analysis_context.recent_memory if analysis_context else None,
            "relevant_memory": analysis_context.relevant_memory if analysis_context else None,
            "goals": analysis_context.goals if analysis_context else None,
            "user_preferences": user_preferences,
        }
