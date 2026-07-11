"""
Strategic AI Core Backend
Response engine
"""

DEFAULT_LANGUAGE = "ru"

LABELS = {
    "ru": {
        "summary": "Итог",
        "perspectives": "Точки зрения",
        "risks": "Риски",
        "opportunities": "Возможности",
        "recommendations": "Рекомендации",
    },
    "en": {
        "summary": "Summary",
        "perspectives": "Perspectives",
        "risks": "Risks",
        "opportunities": "Opportunities",
        "recommendations": "Recommendations",
    },
}


class ResponseEngine:
    def generate(self, analysis: dict, context=None) -> str:
        language = self._resolve_language(analysis, context)
        labels = LABELS.get(language, LABELS[DEFAULT_LANGUAGE])
        tone, detail_level = self._resolve_preferences(context)

        if tone == "concise":
            return self._generate_concise(analysis, labels)
        if detail_level == "high":
            return self._generate_detailed(analysis, labels)
        return self._generate_concise(analysis, labels)

    def _generate_detailed(self, analysis: dict, labels: dict) -> str:
        lines = [f"{labels['summary']}: {analysis.get('summary', '')}"]

        lines.append(f"\n{labels['perspectives']}:")
        perspectives = analysis.get("perspectives", [])
        if perspectives:
            for perspective in perspectives:
                lines.append(f"- {perspective.get('agent')}: {perspective.get('summary')}")
        else:
            lines.append("-")

        lines.append(f"\n{labels['risks']}:")
        lines.extend(self._format_list(analysis.get("risks", [])))

        lines.append(f"\n{labels['opportunities']}:")
        lines.extend(self._format_list(analysis.get("opportunities", [])))

        lines.append(f"\n{labels['recommendations']}:")
        lines.extend(self._format_list(analysis.get("recommendations", [])))

        return "\n".join(lines)

    def _generate_concise(self, analysis: dict, labels: dict) -> str:
        recommendations = analysis.get("recommendations", [])
        lines = [
            f"{labels['summary']}: {analysis.get('summary', '')}",
            f"{labels['recommendations']}: {', '.join(recommendations) if recommendations else '-'}",
        ]
        return "\n".join(lines)

    @staticmethod
    def _format_list(items: list) -> list:
        return [f"- {item}" for item in items] if items else ["-"]

    @staticmethod
    def _resolve_preferences(context):
        if context is None:
            return None, None
        preferences = getattr(context, "preferences", None) or {}
        return preferences.get("tone"), preferences.get("detail_level")

    @staticmethod
    def _resolve_language(analysis: dict, context) -> str:
        if context is not None and getattr(context, "language", None):
            return context.language
        return analysis.get("language", DEFAULT_LANGUAGE)
