"""
Strategic AI Core Backend
Consensus engine
"""


class ConsensusEngine:
    def find_consensus(self, analyses: dict) -> dict:
        agent_names = list(analyses.keys())

        agreements = []
        disagreements = []
        total_comparisons = 0

        for i in range(len(agent_names)):
            for j in range(i + 1, len(agent_names)):
                agent_a = agent_names[i]
                agent_b = agent_names[j]
                total_comparisons += 1

                summary_a = self._extract_summary(analyses[agent_a])
                summary_b = self._extract_summary(analyses[agent_b])

                pair = {"agents": [agent_a, agent_b]}
                if summary_a == summary_b:
                    agreements.append(pair)
                else:
                    disagreements.append(pair)

        confidence = len(agreements) / max(total_comparisons, 1)

        return {
            "agreements": agreements,
            "disagreements": disagreements,
            "confidence": confidence,
        }

    @staticmethod
    def _extract_summary(analysis):
        if isinstance(analysis, dict):
            return analysis.get("summary")
        return analysis
