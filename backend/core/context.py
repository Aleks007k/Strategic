"""
Strategic AI Core Backend
User context
"""

from preferences.preferences_manager import PreferencesManager


class UserContext:
    def __init__(self, language: str = "ru", user_id: str = None, preferences: dict = None):
        self.language = language
        self.user_id = user_id

        if preferences is None and user_id is not None:
            preferences = PreferencesManager().load_preferences(user_id)

        self.preferences = preferences or {}
