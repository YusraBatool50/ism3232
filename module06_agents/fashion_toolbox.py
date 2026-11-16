# fashion_toolbox.py
# Author: Yusra Batool


class FashionToolbox:
    """Check every tool request before running it."""

    def __init__(self, fashion_inventory, fashion_queue):
        self.fashion_inventory = fashion_inventory
        self.fashion_queue = fashion_queue

    def tool_list(self):
        """Return the tools the model may request."""
        return [
            self.fashion_inventory.check_stock,
            self.fashion_queue.request_reservation,
        ]

    def run(self, name, arguments, history):
        """Check one tool request before running it."""
        if name == "check_stock":
            item = self.clean(arguments, "item")

            if item == "":
                return "The item is missing. Ask which item."

            if not self.client_said(history, item):
                return "The customer has not mentioned that item."

            return self.fashion_inventory.check_stock(item)

        if name == "request_reservation":
            item = self.clean(arguments, "item")
            customer = self.clean(arguments, "customer")

            if item == "" or customer == "":
                return "The item and customer name are both needed."

            if not self.client_said(history, item):
                return "The customer has not mentioned that item."

            if not self.client_said(history, customer):
                return "The customer has not given that name."

            return self.fashion_queue.request_reservation(item, customer)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return an argument without extra spaces."""
        return str(arguments.get(key, "")).strip()

    def client_said(self, history, text):
        """Check whether the customer typed this detail."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
