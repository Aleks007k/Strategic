"""
Strategic AI Core Backend
Decision engine
"""


class DecisionEngine:
    def decide(self, consensus: dict, arguments: dict, debates: dict) -> dict:
        confidence = (consensus or {}).get("confidence", 0)
        debates_map = self._extract_debates_map(debates)

        accepted = []
        rejected = []
        needs_review = []

        for agent_name, entries in debates_map.items():
            if confidence == 0:
                rejected.append(agent_name)
                continue

            results = [entry.get("result") for entry in entries]
            if any(result == "challenge" for result in results):
                needs_review.append(agent_name)
            else:
                accepted.append(agent_name)

        return {
            "accepted": accepted,
            "rejected": rejected,
            "needs_review": needs_review,
        }

    @staticmethod
    def _extract_debates_map(debates) -> dict:
        if isinstance(debates, dict) and "debates" in debates:
            return debates["debates"] or {}
        return debates or {}
