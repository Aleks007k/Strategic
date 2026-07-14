"""
Strategic AI Core Backend
Strategic response localizer
"""

from language.localization_manager import LocalizationManager

DEFAULT_LANGUAGE = "ru"


class StrategicResponseLocalizer:
    def __init__(self):
        self.localization_manager = LocalizationManager()

    def localize(self, synthesis: dict, preferences: dict = None) -> str:
        synthesis = synthesis if isinstance(synthesis, dict) else {}
        preferences = preferences if isinstance(preferences, dict) else {}

        language = preferences.get("language") or DEFAULT_LANGUAGE
        tone = preferences.get("tone")
        detail_level = preferences.get("detail_level")

        labels = {
            "experts": self.localization_manager.get_text("response_experts", language),
            "perspectives": self.localization_manager.get_text("response_perspectives", language),
            "risks": self.localization_manager.get_text("response_risks", language),
            "opportunities": self.localization_manager.get_text("response_opportunities", language),
            "confidence": self.localization_manager.get_text("response_confidence", language),
        }

        if tone == "concise":
            return self._generate_concise(synthesis, labels)
        if detail_level == "high":
            return self._generate_detailed(synthesis, labels)
        return self._generate_concise(synthesis, labels)

    @staticmethod
    def _generate_concise(synthesis: dict, labels: dict) -> str:
        experts_count = synthesis.get("experts_count") or 0
        confidence = synthesis.get("confidence_summary")

        lines = [
            f"{labels['experts']}: {experts_count}",
            f"{labels['confidence']}: {confidence if confidence is not None else 'N/A'}",
        ]
        return "\n".join(lines)

    def _generate_detailed(self, synthesis: dict, labels: dict) -> str:
        experts_count = synthesis.get("experts_count") or 0
        confidence = synthesis.get("confidence_summary")

        lines = [f"{labels['experts']}: {experts_count}"]

        lines.append(f"\n{labels['perspectives']}:")
        perspectives = synthesis.get("perspectives") or []
        if perspectives:
            for perspective in perspectives:
                if isinstance(perspective, dict):
                    lines.append(f"- {perspective.get('agent')}: {perspective.get('summary')}")
        else:
            lines.append("-")

        lines.append(f"\n{labels['risks']}:")
        lines.extend(self._format_items(synthesis.get("combined_risks")))

        lines.append(f"\n{labels['opportunities']}:")
        lines.extend(self._format_items(synthesis.get("combined_opportunities")))

        lines.append(f"\n{labels['confidence']}: {confidence if confidence is not None else 'N/A'}")

        return "\n".join(lines)

    @staticmethod
    def _format_items(items) -> list:
        valid_items = [item for item in (items or []) if item is not None]
        return [f"- {item}" for item in valid_items] if valid_items else ["-"]
