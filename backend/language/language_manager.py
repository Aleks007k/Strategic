"""
Strategic AI Core Backend
Language manager
"""

SUPPORTED_LANGUAGES = {"ru", "en"}
DEFAULT_LANGUAGE = "ru"


class LanguageManager:
    def get_language(self, selected: str = None) -> str:
        if selected in SUPPORTED_LANGUAGES:
            return selected
        return DEFAULT_LANGUAGE
