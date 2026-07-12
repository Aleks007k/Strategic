"""
Strategic AI Core Backend
Council builder
"""


class Council:
    def __init__(self, purpose: str = None):
        self.experts = []
        self.purpose = purpose

    def add_expert(self, expert) -> None:
        name = getattr(expert, "name", None)
        if name is not None and any(getattr(existing, "name", None) == name for existing in self.experts):
            return
        self.experts.append(expert)

    def remove_expert(self, name: str) -> None:
        self.experts = [expert for expert in self.experts if getattr(expert, "name", None) != name]

    def list_experts(self) -> list:
        return list(self.experts)

    def to_dict(self) -> dict:
        return {
            "purpose": self.purpose,
            "experts": [
                expert.to_dict() if hasattr(expert, "to_dict") else expert
                for expert in self.experts
            ],
        }
