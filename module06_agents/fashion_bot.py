# fashion_bot.py
# Author: Yusra Batool

HANDOFF_WORDS = ["buy", "purchase", "return", "refund"]
MAX_TOOL_ROUNDS = 3


class FashionHelper:
    """A fashion assistant using rules, a model, and checked tools."""

    def __init__(self, name, instructions, tools, model):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user message and assistant reply."""
        self.history.append({"role": "user", "content": user_message})

        reply = self.choose_reply(user_message)

        self.history.append({"role": "assistant", "content": reply})

        return reply

    def choose_reply(self, user_message):
        """Use handoff rules first, then ask the model."""
        if self.needs_human(user_message.lower()):
            return (
                "I can't process purchases or returns. "
                "Please speak to a store associate."
            )

        return self.model_reply()

    def needs_human(self, text):
        """Check if a store associate is needed."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def model_reply(self):
        """Ask the model and run checked tools up to a limit."""
        rounds = 0

        while rounds < MAX_TOOL_ROUNDS:
            tool_list = self.tools.tool_list()

            decision = self.model.decide(self.instructions, self.history, tool_list)

            if decision is None:
                return "Sorry, I can't answer that right now. Please try again."

            if "text" in decision:
                return decision["text"]

            name = decision["tool"]
            arguments = decision["arguments"]

            result = self.tools.run(name, arguments, self.history)

            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )

            rounds += 1

        return "Sorry, I couldn't finish that. Please speak to a store associate."
