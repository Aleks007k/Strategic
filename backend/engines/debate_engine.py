"""
Strategic AI Core Backend
Debate engine
"""


class DebateEngine:
    def debate(self, arguments: dict, comments: dict) -> dict:
        comments = comments or {}
        agent_names = list(self._extract_arguments_map(arguments).keys())
        debates = {}

        for agent_name in agent_names:
            agent_comments = comments.get(agent_name, [])
            commenters = {entry.get("from") for entry in agent_comments}

            entries = []
            for other_agent in agent_names:
                if other_agent == agent_name:
                    continue
                result = "challenge" if other_agent in commenters else "support"
                entries.append({"against": other_agent, "result": result})

            debates[agent_name] = entries

        return {"debates": debates}

    @staticmethod
    def _extract_arguments_map(arguments) -> dict:
        if isinstance(arguments, dict) and "arguments" in arguments:
            return arguments["arguments"] or {}
        return arguments or {}
