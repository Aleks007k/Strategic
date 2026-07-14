"""
Strategic AI Core Backend
Strategic workflow definition
"""

# Stages the new pipeline actually executes today.
IMPLEMENTED_STAGES = [
    "clarification",
    "planning",
    "agents",
    "consensus",
    "response",
]

# Stages named in the strategic reasoning model but not yet implemented
# by any component reachable from StrategicExecutor. Not valid advance_stage()
# targets until real implementations exist.
PLANNED_STAGES = [
    "arguments",
    "review",
    "debate",
    "decision",
    "probability",
]


class StrategicWorkflow:
    def get_pipeline(self) -> list:
        return list(IMPLEMENTED_STAGES)

    def get_planned_stages(self) -> list:
        return list(PLANNED_STAGES)

    def next_step(self, current_step: str):
        if current_step not in IMPLEMENTED_STAGES:
            return None

        index = IMPLEMENTED_STAGES.index(current_step)
        if index + 1 >= len(IMPLEMENTED_STAGES):
            return None

        return IMPLEMENTED_STAGES[index + 1]
