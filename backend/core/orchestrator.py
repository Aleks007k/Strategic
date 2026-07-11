"""
Strategic AI Core Backend
Agent orchestrator
"""


class Orchestrator:
    def __init__(self):
        self.agents = {}

    def register(self, agent):
        self.agents[agent.name] = agent

    def run(self, agent_name: str, *args, **kwargs):
        agent = self.agents.get(agent_name)
        if agent is None:
            raise ValueError(f"Agent '{agent_name}' is not registered")
        return agent.run(*args, **kwargs)

    def run_all(self, *args, **kwargs):
        return {name: agent.run(*args, **kwargs) for name, agent in self.agents.items()}
