# fashion_tool.py
# Author: Yusra Batool


class FashionInventory:
    """A tool that knows which fashion items are in stock."""

    def __init__(self, items):
        self.items = items
        self.reservations = []

    def find_item(self, text):
        """Return the first known item mentioned in text."""
        for item in self.items:
            if item in text.lower():
                return item
        return None

    def stock_for(self, item):
        """Return stock for one item."""
        if item in self.items:
            return self.items[item]
        return None

    def check_stock(self, item):
        """Check whether a fashion item is available.

        Args:
            item: The fashion item, like heels or jackets.
        """
        found = self.find_item(item)
        if found is None:
            return "Item not found. I can check heels, jackets, dresses, or handbags."
        return f"Stock for {found}: {self.stock_for(found)}."

    def add_reservation(self, item, customer):
        """Record a reservation after approval."""
        self.reservations.append({"item": item, "customer": customer})
