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
        "recommendations": "Рекомендации",
    },
    "en": {
        "summary": "Summary",
        "perspectives": "Perspectives",
        "risks": "Risks",
        "recommendations": "Recommendations",
    },
}


class ResponseEngine:
    def generate(self, analysis: dict, context=None) -> str:
        language = self._resolve_language(analysis, context)
        labels = LABELS.get(language, LABELS[DEFAULT_LANGUAGE])

        lines = [f"{labels['summary']}: {analysis.get('summary', '')}"]

        lines.append(f"\n{labels['perspectives']}:")
        perspectives = analysis.get("perspectives", [])
        if perspectives:
            for perspective in perspectives:
                lines.append(f"- {perspective.get('agent')}: {perspective.get('summary')}")
        else:
            lines.append("-")

        lines.append(f"\n{labels['risks']}:")
        risks = analysis.get("risks", [])
        if risks:
            for risk in risks:
                lines.append(f"- {risk}")
        else:
            lines.append("-")

        lines.append(f"\n{labels['recommendations']}:")
        recommendations = analysis.get("recommendations", [])
        if recommendations:
            for recommendation in recommendations:
                lines.append(f"- {recommendation}")
        else:
            lines.append("-")

        return "\n".join(lines)

    @staticmethod
    def _resolve_language(analysis: dict, context) -> str:
        if context is not None and getattr(context, "language", None):
            return context.language
        return analysis.get("language", DEFAULT_LANGUAGE)
