"""
Strategic AI Core Backend
User profile model
"""

from preferences.preferences_manager import PreferencesManager


class UserProfile:
    def __init__(
        self,
        user_id: str = None,
        language: str = "ru",
        preferences: dict = None,
        goals: list = None,
    ):
        self.user_id = user_id
        self.language = language
        self.preferences = preferences or {}

        if goals is None and user_id is not None:
            goals = PreferencesManager().load_goals(user_id)

        self.goals = goals or []

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "language": self.language,
            "preferences": self.preferences,
            "goals": self.goals,
        }
