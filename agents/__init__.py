class BaseAgent:
    def run(self, **kwargs):
        raise NotImplementedError("Each agent must implement run()")
