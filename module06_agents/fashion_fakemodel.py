# fake_model.py


class FakeModel:
    """A fake model that returns prepared decisions."""

    def __init__(self, decisions):
        self.decisions = decisions
        self.index = 0

    def decide(self, instructions, history, tools):
        if self.index >= len(self.decisions):
            return None

        decision = self.decisions[self.index]
        self.index += 1
        return decision
