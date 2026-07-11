"""
Strategic AI Core Backend
Agent output validator
"""

REQUIRED_FIELDS = [
    "agent",
    "summary",
    "key_factors",
    "risks",
    "opportunities",
    "recommendations",
]


class OutputValidator:
    def validate(self, analysis: dict) -> dict:
        missing_fields = [field for field in REQUIRED_FIELDS if field not in analysis]

        return {
            "valid": len(missing_fields) == 0,
            "missing_fields": missing_fields,
        }
