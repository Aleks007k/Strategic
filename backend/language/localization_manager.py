"""
Strategic AI Core Backend
Localization manager
"""

import json
from pathlib import Path

LOCALIZATION_DIR = Path(__file__).resolve().parent.parent.parent / "localization"

SUPPORTED_LANGUAGES = {"ru", "en"}
FALLBACK_TEXT = "Translation not available."


class LocalizationManager:
    def __init__(self):
        self.translations = {
            language: self._load(language) for language in SUPPORTED_LANGUAGES
        }

    def get_text(self, key: str, language: str = "ru") -> str:
        return self.translations.get(language, {}).get(key, FALLBACK_TEXT)

    @staticmethod
    def _load(language: str) -> dict:
        path = LOCALIZATION_DIR / f"{language}.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
