"""
Strategic AI Core Backend
Preferences manager
"""

import json
from pathlib import Path

PREFERENCES_DIR = Path(__file__).resolve().parent.parent.parent / "preferences"


class PreferencesManager:
    def save_preferences(self, user_id: str, preferences: dict) -> None:
        path = self._resolve_path(user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(preferences, f, indent=2)

    def load_preferences(self, user_id: str) -> dict:
        path = self._resolve_path(user_id)
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_goals(self, user_id: str, goals: list) -> None:
        preferences = self.load_preferences(user_id)
        preferences["goals"] = goals
        self.save_preferences(user_id, preferences)

    def load_goals(self, user_id: str) -> list:
        preferences = self.load_preferences(user_id)
        return preferences.get("goals", [])

    def _resolve_path(self, user_id: str) -> Path:
        return PREFERENCES_DIR / f"{user_id}.json"
