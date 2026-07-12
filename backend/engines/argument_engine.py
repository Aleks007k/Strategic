"""
Strategic AI Core Backend
Argument engine
"""


class ArgumentEngine:
    def build_arguments(self, analyses: dict) -> dict:
        arguments = {}

        for agent_name, analysis in analyses.items():
            agent_arguments = []

            summary = self._extract_field(analysis, "summary")
            if summary:
                agent_arguments.append(f"Primary conclusion: {summary}")

            key_factors = self._extract_field(analysis, "key_factors") or []
            for key_factor in key_factors:
                agent_arguments.append(f"Key factor considered: {key_factor}")

            arguments[agent_name] = agent_arguments

        return {"arguments": arguments}

    @staticmethod
    def _extract_field(analysis, field):
        if isinstance(analysis, dict):
            return analysis.get(field)
        return None
