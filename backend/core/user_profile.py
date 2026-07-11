"""
Strategic AI Core Backend
User profile model
"""


class UserProfile:
    def __init__(self, user_id: str = None, language: str = "ru", preferences: dict = None):
        self.user_id = user_id
        self.language = language
        self.preferences = preferences or {}

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "language": self.language,
            "preferences": self.preferences,
        }
