"""
Strategic AI Core Backend
User context
"""

from preferences.preferences_manager import PreferencesManager
from core.user_profile import UserProfile


class UserContext:
    def __init__(
        self,
        language: str = "ru",
        user_id: str = None,
        preferences: dict = None,
        profile: UserProfile = None,
    ):
        if profile is not None:
            user_id = profile.user_id
            language = profile.language
            preferences = profile.preferences

        self.language = language
        self.user_id = user_id

        if preferences is None and user_id is not None:
            preferences = PreferencesManager().load_preferences(user_id)

        self.preferences = preferences or {}
