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
            "memory": analysis_context.memory_context if analysis_context else None,
            "user_preferences": user_preferences,
        }
