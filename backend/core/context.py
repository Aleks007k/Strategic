"""
Strategic AI Core Backend
User context
"""


class UserContext:
    def __init__(self, language: str = "ru", user_id: str = None, preferences: dict = None):
        self.language = language
        self.user_id = user_id
        self.preferences = preferences or {}
