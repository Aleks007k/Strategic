"""
Strategic AI Core Backend
Strategic workflow definition
"""

PIPELINE = [
    "clarification",
    "planning",
    "agents",
    "arguments",
    "review",
    "debate",
    "consensus",
    "decision",
    "probability",
    "response",
]


class StrategicWorkflow:
    def get_pipeline(self) -> list:
        return list(PIPELINE)

    def next_step(self, current_step: str):
        if current_step not in PIPELINE:
            return None

        index = PIPELINE.index(current_step)
        if index + 1 >= len(PIPELINE):
            return None

        return PIPELINE[index + 1]
