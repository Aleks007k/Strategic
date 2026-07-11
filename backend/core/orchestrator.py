"""
Strategic AI Core Backend
Agent orchestrator
"""


class Orchestrator:
    def __init__(self):
        self.agents = {}

    def register(self, agent):
        self.agents[agent.name] = agent

    def run(self, agent_name: str, question: str, context=None):
        agent = self.agents.get(agent_name)
        if agent is None:
            raise ValueError(f"Agent '{agent_name}' is not registered")
        return agent.run(question, context=context)

    def run_all(self, question: str, context=None):
        return {name: agent.run(question, context=context) for name, agent in self.agents.items()}
