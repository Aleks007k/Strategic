"""
Strategic AI Core Backend
Review engine
"""


class ReviewEngine:
    def review(self, analyses: dict) -> dict:
        agent_names = list(analyses.keys())
        comments = {}

        for i in range(len(agent_names)):
            for j in range(i + 1, len(agent_names)):
                agent_a = agent_names[i]
                agent_b = agent_names[j]

                summary_a = self._extract_summary(analyses[agent_a])
                summary_b = self._extract_summary(analyses[agent_b])

                if summary_a != summary_b:
                    comments.setdefault(agent_b, []).append({
                        "from": agent_a,
                        "comment": f"Summary differs from {agent_a}.",
                    })
                    comments.setdefault(agent_a, []).append({
                        "from": agent_b,
                        "comment": f"Summary differs from {agent_b}.",
                    })

        return {"comments": comments}

    @staticmethod
    def _extract_summary(analysis):
        if isinstance(analysis, dict):
            return analysis.get("summary")
        return analysis
