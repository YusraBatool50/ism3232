# fashion_bot.py
# Author: Yusra Batool

HANDOFF_WORDS = ["buy", "order", "return"]


class FashionHelper:
    """A fashion assistant using rules and a model."""

    def __init__(self, name, instructions, fashion_inventory, model):
        """Set up the helper with its tool, model, and history."""
        self.name = name
        self.instructions = instructions
        self.fashion_inventory = fashion_inventory
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user message and assistant reply."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use rules first, then ask the model."""
        text = user_message.lower()

        if self.needs_human(text):
            return (
                "I can't process orders or returns. Please speak to a store associate."
            )

        if "available" in text or "stock" in text or "have" in text:
            return self.stock_reply(user_message)

        return self.model_reply()

    def model_reply(self):
        """Ask the model or return a safe reply."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I can't answer that right now. Please try again."
        return reply

    def needs_human(self, text):
        """Check if a store associate is needed."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def stock_reply(self, user_message):
        """Use the inventory tool to check availability."""
        item = self.fashion_inventory.find_item(user_message)

        if item is None:
            return "Which item? I can check heels, dresses, handbags, or jackets."

        stock = self.fashion_inventory.stock_for(item)
        return f"Stock for {item}: {stock}."
