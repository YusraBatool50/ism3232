# fashion_tool.py
# Author: Yusra Batool


class FashionInventory:
    """A tool that knows which fashion items are in stock."""

    def __init__(self, items):
        """Store the fashion items this tool can look up."""
        self.items = items

    def find_item(self, text):
        """Return the first known item mentioned in text, or None."""
        for item in self.items:
            if item in text.lower():
                return item
        return None

    def stock_for(self, item):
        """Return the stock for one item, or None if unknown."""
        if item in self.items:
            return self.items[item]
        return None
